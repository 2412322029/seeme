import json
import os
import re
import toml
from flask import Flask, render_template, request, jsonify, send_from_directory
from mcinfo import mcinfo, mclatency

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, 'data.json')
cfg_path = os.path.join(script_dir, "config.toml")
if not os.path.exists(cfg_path):
    raise FileNotFoundError("config.toml not found")
cfg = toml.load(cfg_path)
Data_limit_pc = cfg.get("Data_limit_pc", 6)
Data_limit_browser = cfg.get("Data_limit_browser", 6)
Data_limit_phone = cfg.get("Data_limit_phone", 6)
SECRET_KEY = cfg.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found")


def save_cfg():
    with open(cfg_path, 'w') as f:
        toml.dump({
            "SECRET_KEY": SECRET_KEY,
            "Data_limit_pc": Data_limit_pc,
            "Data_limit_browser": Data_limit_browser,
            "Data_limit_phone": Data_limit_phone,
        }, f)


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"pc": [], "browser": [], "phone": []}


def save_data(d):
    with open(data_file, 'w') as f:
        json.dump(d, f, indent=4)


data = load_data()


def limit(d: list, dl: int):
    if len(d) > dl:
        del d[:-dl]


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


@app.route('/set_info', methods=['POST'])
def set_info():
    try:
        key = request.headers.get('API-KEY')
        if key != SECRET_KEY:
            return jsonify({"error": "Invalid key"}), 403
        info_type = request.form.get('type')
        report_time = request.form.get("report_time")
        match info_type:
            case "pc":
                running_exe = request.form.get("running_exe")
                data["pc"].append({"running_exe": running_exe, "report_time": report_time})
                limit(data["pc"], Data_limit_pc)
            case "browser":
                title = request.form.get("title")
                url = request.form.get("url")
                data["browser"].append({"title": title, "url": url, "report_time": report_time})
                limit(data["browser"], Data_limit_browser)
            case "phone":
                apps = request.form.get("app")
                battery_level = request.form.get("battery_level")
                wifi_ssid = request.form.get("wifi_ssid")
                data["phone"].append({"app": apps, "battery_level": battery_level,
                                      "wifi_ssid": wifi_ssid, "report_time": report_time})
                limit(data["phone"], Data_limit_phone)
            case _:
                return jsonify({"error": "unknown type"}), 400
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_info', methods=['GET'])
def get_info():
    t = request.args.get("type")
    if t in ["pc", "browser", "phone"]:
        return {t: data[t]}
    else:
        return data


@app.route('/del_info', methods=['POST'])
def del_info():
    key = request.headers.get('API-KEY')
    if key != SECRET_KEY:
        return jsonify({"error": "Invalid key"}), 403
    info_type = request.json.get('type')
    report_time = request.json.get('report_time')
    if info_type in data:
        initial_count = len(data[info_type])
        removed_items = [item for item in data[info_type] if item['report_time'] == report_time]
        data[info_type] = [item for item in data[info_type] if item['report_time'] != report_time]
        removed_count = initial_count - len(data[info_type])
        if removed_count > 0:
            save_data(data)
            return jsonify(
                {"message": f"Removed {removed_count} item(s) from {info_type}", "item": f"{removed_items}"}), 200
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
def set_limit():
    global Data_limit_pc, Data_limit_phone, Data_limit_browser
    key = request.headers.get('API-KEY')
    if key != SECRET_KEY:
        return jsonify({"message": "Invalid key"}), 403

    new_limits = request.get_json()
    if not new_limits:
        return jsonify({"message": "No data provided"}), 400

    errors = []
    for device, value in new_limits.items():
        if device in ['pc', 'browser', 'phone']:
            error = validate_limit(value, device)
            if error:
                errors.append(error)
            else:
                globals()[f"Data_limit_{device}"] = int(value)
        else:
            errors.append("unknown type")

    if errors:
        return jsonify({"message": errors}), 400
    save_cfg()
    return jsonify({
        'pc': Data_limit_pc,
        'browser': Data_limit_browser,
        'phone': Data_limit_phone
    }), 200


@app.route('/get_limit', methods=['GET'])
def get_limit():
    return jsonify({
        'pc': Data_limit_pc,
        'browser': Data_limit_browser,
        'phone': Data_limit_phone
    }), 200


@app.teardown_request
def teardown_request(response_or_error):
    save_data(data)
    save_cfg()
    return response_or_error


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
