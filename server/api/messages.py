import json
import re
import time

import requests
from flask import jsonify, request
from util.config import SECRET_KEY, cfg
from util.ip import ip_api
from util.notification import notify
from util.rediscache import del_data, key_to_ts, r

from . import api_bp


@api_bp.route("/leave_message", methods=["POST"])
def leave_message_route():
    recaptcha_cfg = cfg.get("recaptcha", {}) or {}
    secret = recaptcha_cfg.get("secret", "")
    if not secret:
        return jsonify({"error": "未配置 recaptcha.secret"}), 400
    token = (
        request.form.get("g-recaptcha-response")
        or (request.get_json(silent=True) or {}).get("recaptcha_token")
        or request.headers.get("Recaptcha-Token")
    )
    if not token:
        return jsonify({"error": "recaptcha token missing"}), 400
    data = request.get_json(force=True, silent=True) or request.form or {}
    name = (data.get("name") or "匿名").strip()
    content = (data.get("content") or "").strip()
    email = (data.get("email") or "").strip()
    if not content:
        return jsonify({"error": "content is required"}), 400
    if len(content) > 2000:
        return jsonify({"error": "content too long (max 2000 chars)"}), 400
    if len(name) > 100:
        return jsonify({"error": "name too long (max 100 chars)"}), 400
    if email and len(email) > 200:
        return jsonify({"error": "email too long (max 200 chars)"}), 400
    if email and not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return jsonify({"error": "invalid email"}), 400
    report_time = time.time()
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    if client_ip:
        client_ip = client_ip.split(",")[0].strip()
    user_agent = request.headers.get("User-Agent")
    location = ip_api(client_ip)
    try:
        resp = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret, "response": token, "remoteip": client_ip},
            timeout=5,
        )
        resp.raise_for_status()
        vr = resp.json()
    except Exception as e:
        return jsonify({"error": "recaptcha verification error", "detail": str(e)}), 500

    if not vr.get("success"):
        return jsonify({"error": "recaptcha verification failed", "detail": vr}), 403
    try:
        entry = {
            "name": name,
            "content": content,
            "email": email,
            "user_agent": user_agent,
            "location": location,
            "report_time": report_time,
        }
        r.hset("message", entry["report_time"], json.dumps(entry))
        content = f"""
        name: {name} \nEmail:{email}\n
        client_ip: {client_ip}\n Location: {location}\n UA: {user_agent}\n 
        Content: {content}
        """
        notify("网站新留言", content=content, type="markdown")
        return jsonify({"status": "ok", "entry": entry}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "unexpected server error"}), 500


@api_bp.route("/get_messages", methods=["GET"])
def get_messages():
    try:
        try:
            page = int(request.args.get("page", 1))
            limit = int(request.args.get("limit", 20))
        except Exception:
            return jsonify({"error": "invalid pagination parameters"}), 400
        if page < 1 or limit < 1:
            return jsonify({"error": "page and limit must be positive integers"}), 400
        MAX_LIMIT = 100
        if limit > MAX_LIMIT:
            limit = MAX_LIMIT
        order = (request.args.get("order", "") or "").lower()
        items = r.hgetall("message") or {}
        if isinstance(items, dict):
            normalized_items = {}
            for k, v in items.items():
                nk = k.decode() if isinstance(k, bytes) else k
                normalized_items[nk] = v
        else:
            normalized_items = items
        sorted_items = sorted(
            normalized_items.items(),
            key=lambda x: key_to_ts(x[0]) or 0,
            reverse=order == "desc",
        )

        total = len(sorted_items)
        start = (page - 1) * limit
        end = start + limit
        page_slice = sorted_items[start:end]

        results = []
        for k, v in page_slice:
            try:
                obj = json.loads(v)
            except Exception:
                obj = v
            results.append(obj)

        total_pages = (total + limit - 1) // limit if total > 0 else 0
        return (
            jsonify(
                {
                    "message": results,
                    "total": total,
                    "page": page,
                    "limit": limit,
                    "total_pages": total_pages,
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/del_message", methods=["POST"])
def del_message():
    key = request.headers.get("API-KEY")
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key"}), 403
    try:
        data = request.get_json(force=True, silent=True) or {}
        report_time = data.get("report_time")
        if report_time is None:
            return jsonify({"error": "report_time is required"}), 400
        try:
            report_time = float(report_time)
        except Exception:
            return jsonify({"error": "invalid report_time"}), 400

        removed_count = del_data("message", report_time)
        if removed_count > 0:
            return jsonify(
                {"message": f"Removed {removed_count} item(s) from message"}
            ), 200
        else:
            return jsonify(
                {"message": "No items found with the specified report_time"}
            ), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
