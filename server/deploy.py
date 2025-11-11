import os
import re
import subprocess
import time
import traceback
import requests

from dotenv import load_dotenv
from fabric import Connection
from sum import compare_sum_txt
from pathlib import Path

# 加载.env文件中的配置
load_dotenv()

REMOTE_HOST = os.getenv("REMOTE_HOST")  # 远程服务器IP或域名
REMOTE_USER = os.getenv("REMOTE_USER")  # 远程服务器用户名
REMOTE_PORT = int(os.getenv("REMOTE_PORT", 22))  # SSH端口，默认为22
REMOTE_DIR = os.getenv("REMOTE_DIR")  # 远程服务器目标目录
FRONTEND_DIR = os.getenv("FRONTEND_DIR")  # 前端目录
REMOTE_FRONTEND_DIR = os.getenv("REMOTE_FRONTEND_DIR")  # 远程前端目录
verify_url = os.getenv("verify_url")  # 验证URL
# 示例.env文件内容
# REMOTE_HOST=xxx.xxx.xxx.xxx
# REMOTE_USER=root
# REMOTE_PORT=22
# REMOTE_DIR=/var/www/seeme
# FRONTEND_DIR=D:\24123\code\js\seeme-frontend
# PYPATH=/var/www/seeme/.venv/bin/python3
# verify_url=https://i.not404.cc/api/get_deployment_info
# REMOTE_FRONTEND_DIR=/var/www/seeme/templates


def build_frontend_with_copy():
    """
    构建前端应用
    """
    # 清理templates目录下的html文件以及子目录assets下的css和js文件
    TEMPLATES_DIR = REMOTE_FRONTEND_DIR
    print("Cleaning templates directory...")
    # 删除templates目录下的所有.html文件
    for root, dirs, files in os.walk(TEMPLATES_DIR):
        for file in files:
            if file.endswith(".html"):
                os.remove(os.path.join(root, file))
        # 删除子目录assets下的所有.css和.js文件
        if "assets" in dirs:
            assets_dir = os.path.join(root, "assets")
            for asset_root, _, asset_files in os.walk(assets_dir):
                for asset_file in asset_files:
                    if asset_file.endswith((".css", ".js")):
                        os.remove(os.path.join(asset_root, asset_file))
    print("Building frontend application...")
    os.system(f"cd {FRONTEND_DIR} && npm run build")
    print("Frontend application built successfully.")


def update_deployment_info(DEPLOY_TIME, GIT_HASH):
    """
    使用正则表达式更新 api/misc.py 中的部署时间和 Git 哈希值
    """
    filename = Path("api") / "misc.py"
    with open(filename, "r", encoding="utf8") as file:
        content = file.read()
    content = re.sub(
        r'"deploy_time": ".*?",', f'"deploy_time": "{DEPLOY_TIME}",', content
    )
    content = re.sub(r'"git_hash": ".*?"', f'"git_hash": "{GIT_HASH}"', content)
    with open(filename, "w", encoding="utf8") as file:
        file.write(content)
    print("Deployment info updated successfully.")


# 本地文件类型
FILE_TYPES = [".py", ".js", ".html", ".css"]


def upload_frontend_files():
    with Connection(host=REMOTE_HOST, user=REMOTE_USER, port=REMOTE_PORT) as conn:
        conn.run(f"mkdir -p {REMOTE_DIR}")
        # 删除远程目录下的 html, css 和 js 文件
        print("Deleting existing html, css and js files in remote directory...")
        if conn.run(
            f"rm -f {REMOTE_FRONTEND_DIR}/assets/*.css {REMOTE_FRONTEND_DIR}/assets/*.js {REMOTE_FRONTEND_DIR}/index.html"
        ):
            print("Deleted existing files successfully.")
        else:
            print("Failed to delete existing files.")
            # 上传 templates/index.html
        dist_dir = os.path.join(FRONTEND_DIR, "dist")
        if not os.path.exists(dist_dir):
            print(f"Error: {dist_dir} does not exist.")
            return
        local_index_path = f"{dist_dir}/index.html"
        remote_index_path = f"{REMOTE_FRONTEND_DIR}/"
        if os.path.isfile(local_index_path):
            print(f"Uploading {local_index_path} to {remote_index_path}...", end=" ")
            conn.put(local_index_path, remote_index_path)
            print("Uploaded index.html successfully.")

        # 上传 templates/assets 下的 .css 和 .js 文件
        local_assets_path = f"{dist_dir}/assets"
        remote_assets_path = f"{REMOTE_FRONTEND_DIR}/assets"
        for filename in os.listdir(local_assets_path):
            local_file_path = rf"{local_assets_path}\{filename}"
            remote_file_path = rf"{remote_assets_path}/{filename}"
            if os.path.isfile(local_file_path) and any(
                filename.endswith(ext) for ext in FILE_TYPES
            ):
                print(f"Uploading {local_file_path} to {remote_file_path}...", end=" ")
                conn.put(local_file_path, remote_file_path)
                print(f"Uploaded {filename} successfully.")


def upload_files():
    with Connection(host=REMOTE_HOST, user=REMOTE_USER, port=REMOTE_PORT) as conn:
        conn.run(f"mkdir -p {REMOTE_DIR}")
        try:
            only_local, only_remote, different = compare_sum_txt()
            if only_local is None:
                print("Comparison of checksums failed. Aborting upload.")
                return
        except Exception as e:
            print(f"Error computing checksum differences: {e}")
            traceback.print_exc()
            return

        # 上传本地有但远程没有的文件，或者本地和远程hash不同的文件
        files_to_upload = set(only_local).union(set(different))
        if not files_to_upload:
            print("No files to upload.")
        else:
            input(
                "\n".join(files_to_upload)
                + "\nPress Enter to continue uploading the following files:"
            )
        for relative_path in files_to_upload:
            local_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), relative_path
            )
            if not os.path.exists(local_path):
                print(f"Local file does not exist, skipping: {local_path}")
                continue
            if os.path.isdir(local_path):
                print(f"Local path is a directory, skipping: {local_path}")
                continue

            remote_path = f"{REMOTE_DIR}/{relative_path.replace(os.sep, '/')}"
            remote_dir = os.path.dirname(remote_path)

            # 远程路径中包含单引号时需要转义
            remote_dir_escaped = remote_dir.replace("'", "'\"'\"'")

            print(f"Uploading {local_path} to {remote_path}...", end=" ")
            try:
                mkdir_res = conn.run(
                    f"mkdir -p '{remote_dir_escaped}'", hide=True, warn=True
                )
                if not mkdir_res.ok:
                    print(
                        f"\nWarning: failed to create remote dir {remote_dir} (continuing)."
                    )
            except Exception as e:
                print(f"\nError creating remote directory {remote_dir}: {e}")
            # 尝试继续上传，可能会失败
            # 尝试上传，最多重试3次
            success = False
            for attempt in range(1, 4):
                try:
                    conn.put(local_path, remote_path)
                    print("√")
                    success = True
                    break
                except Exception as e:
                    print(f"\nUpload attempt {attempt} failed for {relative_path}: {e}")
                    if attempt < 3:
                        time.sleep(1)
                    else:
                        traceback.print_exc()
            if not success:
                print(f"Failed to upload {relative_path} after retries.")
            continue

        # 更改远程目录的所有权
        print("Changing ownership of remote directory...")
        if conn.sudo(f"chown -R www-data:www-data {REMOTE_DIR}").ok:
            print("Ownership changed successfully.")
        else:
            print("Failed to change ownership.")
        # Ensure restart script exists and run it with sudo, quoting the path to handle spaces/special chars
        print("Executing restart script...")
        conn.sudo(
            f"bash -l -c 'cd {REMOTE_DIR}; source .venv/bin/activate; ./restart.sh'"
        )
        # os.system(f"ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} 'sudo bash -l -c \"{restart_path}\"'")
    print("All specified files have been uploaded.")


def verify_deployment_info(DEPLOY_TIME, GIT_HASH):
    try:
        url = f"{verify_url}"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            remote_info = resp.json()
            if (
                remote_info.get("deploy_time") == DEPLOY_TIME
                and remote_info.get("git_hash") == GIT_HASH
            ):
                print("Deployment info verified successfully.")
            else:
                print("Deployment info verification failed.")
                print(f"Expected: {DEPLOY_TIME}, {GIT_HASH}")
                print(
                    f"Actual: {remote_info.get('deploy_time')}, {remote_info.get('git_hash')}"
                )
            return remote_info
        else:
            print(f"Failed to access remote server: {resp.status_code} {resp.reason}")
    except Exception as e:
        print(f"Error accessing remote server: {e}")
    return None


def main():
    # ...
    try:
        if input("build the frontend application? (y/n): ").lower() == "y":
            build_frontend_with_copy()
            if (
                input("upload frontend files to the remote server? (y/n): ").lower()
                == "y"
            ):
                upload_frontend_files()
        if input("upload files to the remote server? (y/n): ").lower() == "y":
            DEPLOY_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            GIT_HASH = (
                subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                .decode("utf-8")
                .strip()
            )
            update_deployment_info(DEPLOY_TIME, GIT_HASH)
            upload_files()
            # print("去手动开启服务器吧~ pgrep -f gunicorn,  gunicorn -c gunicorn.conf.py main:app -D")
            print("wait for the server to restart...")
            time.sleep(5)
            verify_deployment_info(DEPLOY_TIME, GIT_HASH)
    except Exception as e:
        print(f"An error occurred during deployment: {e}")
        traceback.print_exc()
        exit(1)


def er(r):
    if r.ok:
        print("command executed successfully.")
    else:
        print(f"command failed {r}.")
    if getattr(r, "stdout", None):
        print("stdout:", r.stdout.strip())
    if getattr(r, "stderr", None):
        print("stderr:", r.stderr.strip())


if __name__ == "__main__":
    main()
    #  os.system(f"ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST} '/var/www/seeme/restart.sh'")
    #  os.system(f"ssh -p {REMOTE_PORT} {REMOTE_USER}@{REMOTE_HOST}  \
    #            \"bash -l -c 'source /var/www/seeme/.venv/bin/activate;cd /var/www/seeme/; gunicorn -c gunicorn.conf.py main:app'\"")
# gunicorn -c /var/www/seeme/gunicorn.conf.py main:app -D
