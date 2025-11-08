import re
import time
import json
from flask import request, jsonify
import requests
from . import api_bp
from util.config import cfg, SECRET_KEY
from util.ip import locateip
from util.rediscache import r, del_data, get_1type_data


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
    loc = locateip(client_ip)
    location = (
        "未知"
        if not loc
        else f"{loc.get('country', '未知')} {loc.get('subdiv', '')} {loc.get('city', '')}"
    )
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
        return jsonify({"status": "ok", "entry": entry}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"error": "unexpected server error"}), 500


@api_bp.route("/get_messages", methods=["GET"])
def get_messages():
    try:
        return get_1type_data("message")
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
            return jsonify({"message": f"Removed {removed_count} item(s) from message"}), 200
        else:
            return jsonify({"message": "No items found with the specified report_time"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
