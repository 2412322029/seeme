import json
import secrets

from flask import jsonify, request
from util.config import SECRET_KEY
from util.rediscache import key_to_ts, r

from . import api_bp


@api_bp.route("/get_pub_info", methods=["GET"])
def get_pub_info():
    try:
        name = request.args.get("name")
        if not 0 < len(str(name)) < 20 or not r.get(f"user_secret:{name}"):
            return jsonify({"error": "Invalid name"}), 409
        all_info = r.hgetall(f"public_info:{name}")
        result = {}
        for k, v in all_info.items():
            key = k.decode("utf-8") if isinstance(k, bytes) else k
            value = v.decode("utf-8") if isinstance(v, bytes) else v
            result[key] = json.loads(value)
        return jsonify({"data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/set_pub_info", methods=["POST"])
def set_pub_info():
    try:
        key = request.headers.get("API-KEY")
        name = request.json.get("name")
        info = request.json.get("info")
        if not 0 < len(str(name)) < 20 or not r.get(f"user_secret:{name}") or not key or key != r.get(f"user_secret:{name}").decode("utf-8"):
            return jsonify({"error": "Invalid key or name"}), 409
        if not info or len(info) > 10000:
            return jsonify({"error": "info is requseted and must be less than 10000 characters"}), 410
        report_time = info.get("report_time")
        if not report_time:
            return jsonify({"error": "report_time is requseted in info"}), 411
        r.hset(f"public_info:{name}", f"{report_time}", json.dumps(info))
        all_keys = r.hkeys(f"public_info:{name}")
        if len(all_keys) > 100:
            sorted_keys = sorted(all_keys, key=lambda x: key_to_ts(x.decode("utf-8")))
            keys_to_delete = sorted_keys[:-100]
            for k in keys_to_delete:
                r.hdel(f"public_info:{name}", k)
        return jsonify({"status": "ok", "message": "Public info updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/request_secret", methods=["POST"])
def request_secret():
    try:
        key = request.headers.get("API-KEY")
        name = request.form.get("name") or request.json.get("name")
        if r.get(f"user_secret:{name}") is not None:
            return jsonify({"error": "name already exists"}), 409
        if not 0 < len(str(name)) < 20:
            return jsonify({"error": "name is requseted,>0,<20"}), 410
        if key != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403
        else:
            s = f"user-{name}-{secrets.token_hex(16)}"
            r.set(f"user_secret:{name}", f"{s}")
            return jsonify({"secret_key": f"{s}", "message": "Secret key created successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/del_secret", methods=["DELETE", "POST"])
def del_secret():
    try:
        key = request.headers.get("API-KEY")
        name = request.form.get("name") or request.json.get("name")
        if r.get(f"user_secret:{name}") is None:
            return jsonify({"error": "name not exists"}), 409
        if key != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403
        else:
            r.delete(f"user_secret:{name}")
            r.delete(f"public_info:{name}")
            return jsonify({"status": "ok", "message": "Deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/get_all_request_secret", methods=["GET"])
def get_all_request_secret():
    try:
        if request.headers.get("API-KEY") != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403
        all_secrets = r.keys("user_secret:*")
        result = {}
        for secret in all_secrets:
            name = secret.decode("utf-8").split(":", 1)[1]
            result[name] = r.get(secret).decode("utf-8")
        return jsonify({"data": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
