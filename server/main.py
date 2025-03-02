import json
import os
import re
import time

from flask import Flask, render_template, request, jsonify, send_from_directory

from config import SECRET_KEY
from mcinfo import mcinfo, mclatency
from rediscache import put_data, get_1type_data, get_limit, get_all_types, get_all_types_data, set_limit, del_data, \
    set_data, get_data
from steamapi import steam_info, steam_friend_list, steam_friend_info

app = Flask(__name__)
UPLOAD_ICON_FOLDER = os.path.join(os.path.dirname(__file__), "templates/exe_icon")
os.makedirs(UPLOAD_ICON_FOLDER, exist_ok=True)


# TODO
# @app.before_request
# def force_https():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


def is_valid_address(address: str) -> bool:
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([0-9]{1,5})$'
    return re.match(pattern, address) is not None


@app.route('/get_mcinfo/<address>')
def get_mcinfo(address: str):
    if is_valid_address(address):
        return mcinfo(address)
    else:
        return jsonify({"error": f"{address} <host:port> 错误的地址"}), 400


@app.route('/get_mclatency/<address>')
def get_mclatency(address: str):
    if is_valid_address(address):
        return mclatency(address)
    else:
        return jsonify({"error": f"{address} <host:port> 错误的地址"}), 400


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<path:filename>')
def template_proxy(filename):
    template_dir = os.path.join(app.root_path, 'templates')
    return send_from_directory(template_dir, filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html')


@app.route('/set_info', methods=['POST'])
def set_info():
    try:
        key = request.headers.get('API-KEY')
        if key != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403
        info_type = request.form.get('type') or request.json.get('type')
        report_time = request.form.get("report_time") or request.json.get('report_time')
        match info_type:
            case "pc":
                running_exe = request.json.get("running_exe")
                exe_name = request.json.get("exe_name")
                other = request.json.get("other")
                set_data("activity_window", json.dumps(other))
                put_data("pc", {"running_exe": running_exe, "exe_name": exe_name, "report_time": report_time})
            case "browser":
                title = request.form.get("title")
                url = request.form.get("url")
                put_data("browser", {"title": title, "url": url, "report_time": report_time})
            case "phone":
                apps = request.json.get("app")
                battery_level = request.json.get("battery_level")
                wifi_ssid = request.json.get("wifi_ssid")
                put_data("phone", {"app": apps, "battery_level": battery_level,
                                   "wifi_ssid": wifi_ssid, "report_time": report_time})
            case _:
                return jsonify({"error": f"unknown type {info_type}"}), 400
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_info', methods=['GET'])
def get_info():
    t = request.args.get("type")
    if t in get_all_types():
        return get_1type_data(t)
    else:
        return get_all_types_data()


@app.route('/del_info', methods=['POST'])
def del_info():
    key = request.headers.get('API-KEY')
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key"}), 403
    info_type = request.json.get('type')
    report_time = request.json.get('report_time')
    if info_type in get_all_types():
        removed_count = del_data(info_type, report_time)
        if removed_count > 0:
            return jsonify({"message": f"Removed {removed_count} item(s) from {info_type}"}), 200
        else:
            return jsonify({"message": "No items found with the specified report_time"}), 404
    else:
        return jsonify({"message": "Type not found"}), 404


def validate_limit(value, name):
    try:
        value = int(value)
        if value < 1 or value > 100:
            return f"{name} limit must be between 1 and 100"
    except ValueError:
        return f"{name} limit must be an integer"
    return None


@app.route('/set_limit', methods=['POST'])
def set_limit_api():
    key = request.headers.get('API-KEY')
    if key != SECRET_KEY:
        return jsonify({"message": "Invalid key"}), 403
    new_limits = request.get_json()
    if not new_limits:
        return jsonify({"message": "No data provided"}), 400
    errors = []
    for t, value in new_limits.items():
        if t in get_all_types():
            error = validate_limit(value, t)
            if error:
                errors.append(error)
            else:
                set_limit(t, int(value))
        else:
            errors.append("unknown type")

    if errors:
        return jsonify({"message": errors}), 400
    return jsonify(get_limit()), 200


@app.route('/get_limit', methods=['GET'])
def get_limit_api():
    return jsonify(get_limit()), 200


@app.route('/get_all_types', methods=['GET'])
def get_all_types_api():
    return jsonify(get_all_types()), 200


@app.route('/get_activity_window', methods=['GET'])
def get_activity_window():
    return jsonify(json.loads(get_data("activity_window"))), 200


@app.route('/upload_exeIcon', methods=['POST'])
def upload_exeIcon():
    key = request.headers.get('API-KEY')
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key"}), 403
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No selected files"}), 400
    saved_files = []
    for file in files:
        if file.filename == '':
            continue
        if file and file.filename.lower().endswith('.png'):
            filename = file.filename
            file_path = os.path.join(UPLOAD_ICON_FOLDER, filename)
            file.save(file_path)
            saved_files.append(filename)
        else:
            return jsonify({"error": "Invalid file type only support .png"}), 400
    return jsonify({"message": "File uploaded successfully", "filename": saved_files}), 200


@app.route('/get_allIcon', methods=['GET'])
def get_allIcon():
    try:
        all_entries = os.listdir(UPLOAD_ICON_FOLDER)
        filenames = [entry.split(".png")[0] for entry in all_entries if
                     os.path.isfile(os.path.join(UPLOAD_ICON_FOLDER, entry))]
        return jsonify(filenames), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_steam_info', methods=['GET'])
def get_steam_info():
    try:
        return jsonify(steam_info()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_steam_friend_list', methods=['GET'])
def get_steam_friend_list():
    try:
        return jsonify(steam_friend_list(t=time.time())), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_steam_friend_info', methods=['GET'])
def get_steam_friend_info():
    try:
        return jsonify(steam_friend_info()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_deployment_info', methods=['GET'])
def get_deployment_info():
    deployment_info = {
        "deploy_time": "2025-03-02 13:18:37",
        "git_hash": "6c2f79c"
    }
    return jsonify(deployment_info), 200


# @app.teardown_request
# def teardown_request(response_or_error):
#     save_data(data)
#     save_cfg()
#     return response_or_error


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
