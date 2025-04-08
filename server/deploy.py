import http.client
import json
import os
import re
import shutil
import subprocess
import time
import traceback

from dotenv import load_dotenv
from fabric import Connection

# 加载.env文件中的配置
load_dotenv()

REMOTE_HOST = os.getenv('REMOTE_HOST')  # 远程服务器IP或域名
REMOTE_USER = os.getenv('REMOTE_USER')  # 远程服务器用户名
REMOTE_PORT = int(os.getenv('REMOTE_PORT', 22))  # SSH端口，默认为22
REMOTE_DIR = os.getenv('REMOTE_DIR')  # 远程服务器目标目录
Frontend_DIR = os.getenv('Frontend_DIR')  # 前端目录

def build_frontend_with_copy():
    """
    构建前端应用
    """
    # 清理templates目录下的html文件以及子目录assets下的css和js文件
    TEMPLATES_DIR = './templates'
    print("Cleaning templates directory...")
    # 删除templates目录下的所有.html文件
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith('.html'):
                os.remove(os.path.join(root, file))
        # 删除子目录assets下的所有.css和.js文件
        if 'assets' in dirs:
            assets_dir = os.path.join(root, 'assets')
            for asset_root, _, asset_files in os.walk(assets_dir):
                for asset_file in asset_files:
                    if asset_file.endswith(('.css', '.js')):
                        os.remove(os.path.join(asset_root, asset_file))
    print("Building frontend application...")
    os.system(f'cd {Frontend_DIR} && npm run build')
    print("Frontend application built successfully.")
    # 将Frontend_DIR/dist目录的内容复制到templates目录
    print("Copying dist content to templates directory...")
    dist_dir = os.path.join(Frontend_DIR, 'dist')
    if not os.path.exists(dist_dir):
        print(f"Error: {dist_dir} does not exist.")
        return
    # 复制dist目录下的所有内容到templates
    for item in os.listdir(dist_dir):
        src = os.path.join(dist_dir, item)
        dst = os.path.join(TEMPLATES_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)
    print("Content copied successfully.")

def update_deployment_info(DEPLOY_TIME, GIT_HASH):
    """
    使用正则表达式更新 main.py 中的部署时间和 Git 哈希值
    """
    filename = 'main.py'
    with open(filename, 'r', encoding='utf8') as file:
        content = file.read()
    content = re.sub(r'"deploy_time": ".*?",', f'"deploy_time": "{DEPLOY_TIME}",', content)
    content = re.sub(r'"git_hash": ".*?"', f'"git_hash": "{GIT_HASH}"', content)
    with open(filename, 'w', encoding='utf8') as file:
        file.write(content)
    print("Deployment info updated successfully.")

# 本地文件类型
FILE_TYPES = ['.py', '.js', '.html', '.css']

def upload_files():
    with Connection(host=REMOTE_HOST, user=REMOTE_USER, port=REMOTE_PORT) as conn:
        conn.run(f"mkdir -p {REMOTE_DIR}")
        # 删除远程目录下的 html, css 和 js 文件
        print("Deleting existing html, css and js files in remote directory...")
        if conn.run(f"rm -f {REMOTE_DIR}/templates/assets/*.css {REMOTE_DIR}/templates/assets/*.js {REMOTE_DIR}/templates/index.html"):
            print("Deleted existing files successfully.")
        else:   
            print("Failed to delete existing files.")
        # 上传.目录中的文件
        for filename in os.listdir('.'):
            if os.path.isfile(filename):
                if any(filename.endswith(ext) for ext in FILE_TYPES):
                    print(f"Uploading {filename} to {REMOTE_DIR}/{filename}...", end=' ')
                    conn.put(filename, REMOTE_DIR)
                    print(f"Uploaded {filename} successfully.")
        # 上传util目录中的文件
        for filename in os.listdir('./util'):
            if os.path.isfile(filename):
                if any(filename.endswith(ext) for ext in FILE_TYPES):
                    print(f"Uploading {filename} to {REMOTE_DIR}/{filename}...", end=' ')
                    conn.put(filename, REMOTE_DIR)
                    print(f"Uploaded {filename} successfully.")
        # 上传 templates/index.html
        local_index_path = "templates/index.html"
        remote_index_path = f"{REMOTE_DIR}/templates/"
        if os.path.isfile(local_index_path):
            print(f"Uploading {local_index_path} to {remote_index_path}...", end=' ')
            conn.put(local_index_path, remote_index_path)
            print(f"Uploaded index.html successfully.")

        # 上传 templates/assets 下的 .css 和 .js 文件
        local_assets_path = "templates/assets"
        remote_assets_path = f"{REMOTE_DIR}/templates/assets"
        for filename in os.listdir(local_assets_path):
            local_file_path = fr"{local_assets_path}\{filename}"
            remote_file_path = fr"{remote_assets_path}/{filename}"
            if os.path.isfile(local_file_path) and any(filename.endswith(ext) for ext in FILE_TYPES):
                print(f"Uploading {local_file_path} to {remote_file_path}...", end=' ')
                conn.put(local_file_path, remote_file_path)
                print(f"Uploaded {filename} successfully.")

        # 更改远程目录的所有权
        print("Changing ownership of remote directory...")
        if conn.sudo(f"chown -R www-data:www-data {REMOTE_DIR}").ok:
            print("Ownership changed successfully.")
        else:
            print("Failed to change ownership.")
         # 重新加载 uWSGI 应用
        print("Reloading uWSGI application...")
        if conn.run(f"uwsgi --reload {REMOTE_DIR}/app.pid").ok:
            print("uWSGI application reloaded successfully.")
        else:
            print("Failed to reload uWSGI application.")
    print("All specified files have been uploaded.")


def verify_deployment_info(DEPLOY_TIME, GIT_HASH):
    try:
        # 创建 HTTP 连接
        conn = http.client.HTTPConnection("https://i.not404.cc", port=443)
        conn.request("GET", "/get_deployment_info")
        response = conn.getresponse()
        
        if response.status == 200:
            data = response.read()
            remote_info = json.loads(data.decode("utf-8"))
            if remote_info.get("deploy_time") == DEPLOY_TIME and remote_info.get("git_hash") == GIT_HASH:
                print("Deployment info verified successfully.")
            else:
                print("Deployment info verification failed.")
                print(f"Expected: {DEPLOY_TIME}, {GIT_HASH}")
                print(f"Actual: {remote_info.get('deploy_time')}, {remote_info.get('git_hash')}")
            return remote_info
        else:
            print(f"Failed to access remote server: {response.status} {response.reason}")
    except Exception as e:
        print(f"Error accessing remote server: {e}")
    finally:
        conn.close()

def main():
    try:
        if input("build the frontend application? (y/n): ").lower() == 'y':
            build_frontend_with_copy()
        if input("upload files to the remote server? (y/n): ").lower() == 'y':
            DEPLOY_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            GIT_HASH = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
            update_deployment_info(DEPLOY_TIME, GIT_HASH)
            upload_files()
            print("wait for the server to restart...")
            time.sleep(5)
            verify_deployment_info(DEPLOY_TIME, GIT_HASH)
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
