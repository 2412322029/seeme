import json
import os
import re
import time
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from flask import Flask, Response, render_template, request, jsonify, send_from_directory

from util.ai import completion_api, del_cache
from util.config import SECRET_KEY, cfg
from util.mcinfo import mcinfo, mclatency
from util.rediscache import (put_data, get_1type_data, get_limit, get_all_types, r,
                             get_all_types_data, set_limit, del_data, set_data, get_data)
from util.steamapi import steam_info, steam_friend_list, steam_friend_info

app = Flask(__name__)
UPLOAD_ICON_FOLDER = os.path.join(os.path.dirname(__file__), "templates/exe_icon")
os.makedirs(UPLOAD_ICON_FOLDER, exist_ok=True)


# @app.before_request
# def force_https():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 允许所有域
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, API-KEY'
    return response


def is_valid_address(address: str) -> bool:
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+):([0-9]{1,5})$'
    return re.match(pattern, address) is not None


@app.route('/get_mcinfo/<address>')
def get_mcinfo(address: str):
    if is_valid_address(address):
        return jsonify(mcinfo(address)), 200
    else:
        return jsonify({"error": f"{address} <host:port> 错误的地址"}), 400


@app.route('/get_mclatency/<address>')
def get_mclatency(address: str):
    if is_valid_address(address):
        return jsonify(mclatency(address)), 200
    else:
        return jsonify({"error": f"{address} <host:port> 错误的地址"}), 400


@app.route('/')
def index():
    access_count = get_data("access_count")
    try:
        access_count = int(access_count)
    except ValueError:
        access_count = 0
    access_count = access_count + 1
    set_data("access_count", str(access_count))
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
    access_count = get_data("access_count")
    try:
        access_count = int(access_count)
    except ValueError:
        access_count = 0
    deployment_info = {
        "access_count": access_count,
        "deploy_time": "2025-03-15 14:03:12",
        "git_hash": "4967ae1"
    }
    return jsonify(deployment_info), 200


@app.route('/ai_summary', methods=['GET'])
def ai_summary():
    return Response(completion_api(), mimetype="text/event-stream")


@app.route('/del_ai_cache', methods=['GET'])
def del_ai_cache():
    try:
        return f'已删除{del_cache()}条'
    except Exception as e:
        return str(e)


@app.route('/del_xlog_cache', methods=['GET'])
def del_xlog_cache():
    try:
        return f'已删除{r.delete("xlog")}'
    except Exception as e:
        return str(e)


@app.route('/proxy_xlog', methods=['GET'])
def proxy_xlog():
    p = os.path.join(os.path.dirname(__file__), "data.json")
    with open(p, "r", encoding="utf8") as f:
        return Response(f.read(), mimetype='application/json')
    # if r.exists("xlog"):
    #     return jsonify(json.loads(r.get("xlog"))), 200
    # response = requests.get(url="https://xlog.not404.cc/api/pages?characterId=50877&type=post&"
    #                           "type=portfolio&visibility=published&useStat=true&limit=18&sortType=latest", timeout=10)
    # if response.status_code == 200:
    #     r.set("xlog", json.dumps(response.json()), ex=3600 * 24)
    # da = response.json()
    # if da.get('count', 0) == 0:
    #     print("ff")
    #     return jsonify(json.loads(data)), 200
    # else:
    #     return response.json()


@app.route('/proxy', methods=['GET'])
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({'error': 'Target URL is required'}), 400

    # 验证 URL 格式
    parsed_url = urlparse(target_url)
    if parsed_url.scheme not in ['http', 'https']:
        return jsonify({'error': 'Invalid URL scheme'}), 400

    target_domain = parsed_url.netloc
    headers = dict(request.headers)
    headers['Host'] = target_domain
    headers['Accept-Encoding'] = 'identity'  # 禁用 gzip 编码，避免处理压缩内容
    if target_domain == 'api.bgm.tv':
        tk = str(cfg.get("bgm", {}).get("Auth", ""))
        headers.update({
            'Authorization': 'Bearer ' + tk
        })
    # 获取原始请求的查询参数（包括 url 参数和其他参数）
    query_params = parse_qs(request.query_string.decode('utf-8'))
    query_params.pop('url', None)
    # 将剩余的参数重新编码为查询字符串
    additional_query_string = urlencode(query_params, doseq=True)
    if additional_query_string:
        target_url = urlunparse(parsed_url._replace(query=additional_query_string))
    try:
        response = requests.get(url=target_url, headers=headers, stream=True, timeout=10)
        resp = Response(response.iter_content(chunk_size=1024), status=response.status_code)
        # 过滤掉跳到跳头部
        hop_by_hop_headers = [
            'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization',
            'te', 'trailer', 'transfer-encoding', 'upgrade'
        ]
        for header, value in response.headers.items():
            if header.lower() not in hop_by_hop_headers:
                resp.headers[header] = value
        return resp
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
    # from wsgiref.simple_server import make_server

    # httpd = make_server('0.0.0.0', 5000, app)
    # print('Serving HTTP on port 5000...')
    # try:
    #    httpd.serve_forever()
    # except KeyboardInterrupt:
    #    print("stop ")
    #    httpd.server_close()
