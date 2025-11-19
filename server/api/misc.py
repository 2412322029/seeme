import json
import os
import re
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from flask import Response, jsonify, request

from util.ai import completion_api, del_cache
from util.config import SECRET_KEY, cfg
from util.mcinfo import mcinfo
from util.rediscache import get_data, r, set_data

from . import api_bp

deployfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".deploy.json")
if not os.path.exists(deployfile):
    with open(deployfile, "w", encoding="utf-8") as f:
        json.dump({"deploy_time": f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}", "git_hash": ""}, f)
with open(deployfile, "r", encoding="utf-8") as f:
    deployment_info_data = json.load(f)


def is_valid_address(address: str) -> bool:
    pattern = r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([0-9]{1,5})$"
    return re.match(pattern, address) is not None


@api_bp.route("/get_mcinfo/<type>/<address>", methods=["GET"])
def get_mcinfo(type: str, address: str):
    type = type.lower()
    if type not in ("auto", "java", "bedrock"):
        return {"error": "类型错误，应为 auto/java/bedrock 之一"}
    if is_valid_address(address):
        return jsonify(mcinfo(address, protocol=type)), 200
    else:
        return jsonify({"error": f"{address} <host:port> 错误的地址"}), 400


@api_bp.route("/get_deployment_info", methods=["GET"])
def get_deployment_info():
    access_count = get_data("access_count")
    try:
        access_count = int(access_count)
    except Exception:
        access_count = 0
    deployment_info = {
        "access_count": access_count,
        "deploy_time": deployment_info_data.get("deploy_time", "unknown"),
        "git_hash": deployment_info_data.get("git_hash", "unknown"),
    }
    access_count = access_count + 1
    set_data("access_count", str(access_count))
    return jsonify(deployment_info), 200


@api_bp.route("/ai_summary", methods=["GET"])
def ai_summary():
    return Response(completion_api(), mimetype="text/event-stream")


@api_bp.route("/del_ai_cache", methods=["GET"])
def del_ai_cache():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key in request args"}), 403
    try:
        return f"已删除{del_cache()}条"
    except Exception as e:
        return str(e)


@api_bp.route("/del_xlog_cache", methods=["GET"])
def del_xlog_cache():
    key = request.args.get("key")
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key in request args"}), 403
    try:
        return f"已删除{r.delete('xlog')}"
    except Exception as e:
        return str(e)


@api_bp.route("/proxy_xlog", methods=["GET"])
def proxy_xlog():
    if r.exists("xlog"):
        resp = jsonify(json.loads(r.get("xlog")))
        resp.headers["X-Cache"] = "HIT"
        return resp, 200
    try:
        response = requests.get(
            url="https://xlog.not404.cc/api/pages?characterId=50877&type=post&type=portfolio&visibility=published&useStat=true&limit=18&sortType=latest",
            timeout=10,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    if response.status_code == 200:
        if not response.json().get("count") == 0:
            r.set("xlog", json.dumps(response.json()), ex=3600 * 24)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500
    return response.json()


@api_bp.route("/proxy", methods=["GET"])
def proxy():
    target_url = request.args.get("url")
    if not target_url:
        return jsonify({"error": "Target URL is required"}), 400

    parsed_url = urlparse(target_url)
    if parsed_url.scheme not in ["http", "https"]:
        return jsonify({"error": "Invalid URL scheme"}), 400

    target_domain = parsed_url.netloc
    headers = dict(request.headers)
    headers["Host"] = target_domain
    headers["Accept-Encoding"] = "identity"
    if target_domain == "api.bgm.tv":
        headers.update({"Authorization": "Bearer " + str(cfg.get("bgm", {}).get("Auth", ""))})
    query_params = parse_qs(request.query_string.decode("utf-8"))
    query_params.pop("url", None)
    additional_query_string = urlencode(query_params, doseq=True)
    if additional_query_string:
        target_url = urlunparse(parsed_url._replace(query=additional_query_string))
    try:
        response = requests.get(url=target_url, headers=headers, stream=True, timeout=10)
        resp = Response(response.iter_content(chunk_size=1024), status=response.status_code)
        hop_by_hop_headers = [
            "connection",
            "keep-alive",
            "proxy-authenticate",
            "proxy-authorization",
            "te",
            "trailer",
            "transfer-encoding",
            "upgrade",
        ]
        for header, value in response.headers.items():
            if header.lower() not in hop_by_hop_headers:
                resp.headers[header] = value
        return resp
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
