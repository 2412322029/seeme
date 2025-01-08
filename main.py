import json
import os
import re
import toml
from flask import Flask, render_template, request
from urllib.parse import unquote

from mcinfo import mcinfo, mclatency

app = Flask(__name__)

data_file = 'data.json'
Data_limit = 6


def load_secret_key():
    try:
        return toml.load("config.toml").get("SECRET_KEY")
    except Exception:
        print("config.toml 文件不存在或 SECRET_KEY 未定义。")
        with open('config.toml', 'w') as f:
            f.write("# SECRET_KEY = 'your SECRET_KEY'\n")
        print("config.toml 文件已创建，在config.toml中设置SECRET_KEY")
        exit()


SECRET_KEY = load_secret_key()


def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {"pc": [], "browser": [], "phone": []}


def save_data(d):
    with open(data_file, 'w') as f:
        json.dump(d, f, indent=4)


data = load_data()


def limit(d: list):
    if len(d) > Data_limit:
        del d[:-Data_limit]


def is_valid_address(address: str) -> bool:
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([0-9]{1,5})$'
    return re.match(pattern, address) is not None


@app.route('/get_mcinfo/<address>')
def get_mcinfo(address: str):
    if is_valid_address(address):
        return mcinfo(address)
    else:
        return f"{address} <host:port> 错误的地址"


@app.route('/get_mclatency/<address>')
def get_mclatency(address: str):
    if is_valid_address(address):
        return mclatency(address)
    else:
        return f"{address} <host:port> 错误的地址"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/info', methods=['GET'])
def pcinfo():
    try:
        key = request.args.get("key")
        if key == SECRET_KEY:
            info_type = request.args.get('type')
            report_time = request.args.get("report_time")
            match info_type:
                case "pc":
                    running_exe = unquote(request.args.get("running_exe"))
                    data["pc"].append({"running_exe": running_exe, "report_time": report_time})
                    limit(data["pc"])
                case "browser":
                    title = request.args.get("title")
                    url = request.args.get("url")
                    data["browser"].append({"title": title, "url": url, "report_time": report_time})
                    limit(data["browser"])
                case "phone":
                    apps = request.args.get("app")
                    battery_level = request.args.get("battery_level")
                    wifi_ssid = request.args.get("wifi_ssid")
                    data["phone"].append({"app": apps, "battery_level": battery_level,
                                          "wifi_ssid": wifi_ssid, "report_time": report_time})
                    limit(data["phone"])
                case _:
                    return "unknown type"
            return "ok"
        else:
            return "error key"
    except Exception as e:
        return str(e)


@app.route('/get_info', methods=['GET'])
def get_pcinfo():
    return data


@app.teardown_request
def teardown_request(response_or_error):
    save_data(data)
    return response_or_error


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
