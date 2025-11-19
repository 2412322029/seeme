import re

from flask import jsonify, request

from util.config import SECRET_KEY
from util.rediscache import r

from . import api_bp


@api_bp.route("/c/<mmd>", methods=["GET"])
def paste(mmd):
    try:
        if not re.fullmatch(r"[A-Za-z]{3}", mmd):
            return jsonify({"error": "mmd must be exactly 3 letters"}), 400
        raw = r.get("paste:" + mmd)
        if raw is None:
            return jsonify({"key": mmd, "data": ""}), 200
        data = raw.decode("utf-8") if isinstance(raw, bytes) else raw
        return jsonify({"key": mmd, "data": data}), 200
    except Exception as e:
        return jsonify({"error": "服务器内部错误", "detail": str(e)}), 500


@api_bp.route("/c/<mmd>", methods=["POST"])
def paste_post(mmd):
    try:
        if not re.fullmatch(r"[A-Za-z]{3}", mmd):
            return jsonify({"error": "mmd must be exactly 3 letters"}), 400
        payload = request.get_json(force=True, silent=True)
        if not payload or "data" not in payload:
            return jsonify({"error": "Missing 'data' in JSON body"}), 400
        data = payload.get("data", "")
        if not data:
            return jsonify({"error": "data is empty"}), 400
        if not isinstance(data, (str, bytes, bytearray)):
            data = str(data)
        size = len(data.encode("utf-8")) if isinstance(data, str) else len(data)
        if size > 8 * 1024:
            return jsonify({"error": "data exceeds 8KB limit"}), 400
        r.set("paste:" + mmd, data)
        return jsonify({"status": "ok", "key": mmd}), 200
    except Exception as e:
        return jsonify({"error": "服务器内部错误", "detail": str(e)}), 500


@api_bp.route("/all_pastes_keys", methods=["GET"])
def all_pastes_keys():
    if request.headers.get("API-KEY") != SECRET_KEY:
        return jsonify({"error": "Invalid API key"}), 403
    try:
        keys = r.keys("paste:*")
        keys = [key.decode("utf-8").split("paste:")[1] if isinstance(key, bytes) else key.split("paste:")[1] for key in keys]
        return jsonify({"keys": keys}), 200
    except Exception as e:
        return jsonify({"error": "服务器内部错误", "detail": str(e)}), 500
