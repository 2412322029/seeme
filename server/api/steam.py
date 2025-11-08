import time
from flask import jsonify
from . import api_bp
from util.steamapi import steam_info, steam_friend_list, steam_friend_info


@api_bp.route("/get_steam_info", methods=["GET"])
def get_steam_info():
    try:
        return jsonify(steam_info()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/get_steam_friend_list", methods=["GET"])
def get_steam_friend_list():
    try:
        return jsonify(steam_friend_list(t=time.time())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route("/get_steam_friend_info", methods=["GET"])
def get_steam_friend_info():
    try:
        return jsonify(steam_friend_info()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
