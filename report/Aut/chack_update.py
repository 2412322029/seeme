import hashlib
import os
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import wraps
from tkinter import messagebox

import requests

from .config import cfg, setting_config
from .logger import logger, APPDATA, __version__
from .process_mgr import kill_process, pid_file, aut_pid_file, read_pid, is_process_running

temp_dir = os.path.join(APPDATA, 'temp')

# 创建一个线程池
executor = ThreadPoolExecutor(max_workers=10, thread_name_prefix="ThreadPool")


def run_in_thread(func, callback=None):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def thread_target():
            # print(f"Func:{func.__name__}({args=}, {kwargs=}) run in {threading.current_thread().__str__()}")
            return func(*args, **kwargs)

        future = executor.submit(thread_target)
        if callback:
            future.add_done_callback(callback)
        return future

    return wrapper


@run_in_thread
def test_conn():
    try:
        start_time = time.time()
        requests.get("https://api.github.com/")
        github_time = time.time() - start_time
        start_time = time.time()
        requests.get("https://gitee.com/api/v5/repos/qwe2412322029")
        gitee_time = time.time() - start_time
        messagebox.showinfo("测试连接", f"gitee {gitee_time * 1000:.0f}ms\ngithub {github_time * 1000:.0f}ms")
    except Exception as e:
        messagebox.showerror("测试连接", f"无法连接到任何服务 {e}")


@run_in_thread
def get_update_info(update_source, s, alert=True):
    try:
        if update_source == "github":
            url = "https://api.github.com/repos/2412322029/seeme/releases/latest"
        elif update_source == "gitee":
            url = "https://gitee.com/api/v5/repos/qwe2412322029/seeme/releases/latest"
        else:
            logger.error("unknown update source")
            return
        print(f"使用更新源: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            tag_name = data.get("tag_name", "未知版本").split("v")[1]
            published_at = data.get("published_at", "未知发布时间")
            body = data.get("body", "无更新说明")
            assets = data.get("assets", [])
            print("更新信息")
            print(f"版本号: {tag_name}")
            print(f"发布时间: {published_at}")
            print(f"更新说明: {body}")
            my_assets = []
            for asset in assets:
                asset_name = asset.get("name", "")
                asset_url = asset.get("browser_download_url", "")
                my_assets.append({"name": asset_name, "url": asset_url})
            info = {
                "version": tag_name,
                "published_at": published_at,
                "body": body,
                "assets": my_assets
            }
            cfg.set("DEFAULT", "last_update_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            setting_config(cfg)
            if not s:
                return info
            else:
                s.update_info = info
                if __version__ >= info["version"] and alert:
                    messagebox.showinfo(f"info", f"{__version__}是最新版。{__version__} ->"
                                                 f" {info["version"]}\n{info["body"]}")
                if __version__ < info["version"]:
                    messagebox.askquestion(f"有新版本!", f"{__version__} ->"
                                                         f" {info["version"]}\n{info["body"]}")
                    s.info_label.config(text=f"{info["version"]} is new ,"
                                             f" Click to download", state="normal", cursor="hand2")
        else:
            messagebox.showerror("错误", f"检查更新失败，\n"
                                         f"{url=}\n状态码: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("错误", f"检查更新失败: {e}")


def b2mb(b):
    return f"{b / (1024 * 1024):.2f}"


@run_in_thread
def download_file(name, url, save_dir, s=None, do_next=None):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, name)
    temp_path = save_path + ".tmp"  # 临时文件路径
    if os.path.isfile(save_path):
        s.download_text.config(text=f"{name} already exists in temp, skip download")
        time.sleep(1)
        if do_next:
            do_next()
        return
    try:
        logger.info(f"download {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        with open(temp_path, 'wb') as file:
            current_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    current_size += len(chunk)
                    if s:
                        s.download_progress["value"] = (current_size / total_size) * 100
                        s.about_row.update_idletasks()
                        bf = f"{(current_size / total_size) * 100:.1f}%"
                        s.download_text.config(
                            text=f"下载{name} {b2mb(current_size)}MB / {b2mb(total_size)}MB {bf}")
        os.rename(temp_path, save_path)
        # print(f"开始模拟下载：{url}")
        # total_size = 1024 * 1024 * 10
        # current_size = 0
        # while current_size < total_size:
        #     chunk_size = min(8192, total_size - current_size)
        #     current_size += chunk_size
        #     if s:
        #         s.download_progress["value"] = (current_size / total_size) * 100
        #         s.about_row.update_idletasks()
        #         bf = f"{(current_size / total_size) * 100:.1f}%"
        #         s.download_text.config(text=f"下载{name} {b2mb(current_size)}MB / {b2mb(total_size)}MB {bf}")
        #     time.sleep(0.02)
        # print("文件下载完成")

        msg = f"文件 {name} 已成功下载到 {save_path}"
        logger.info(msg)
        time.sleep(2)
        if do_next:
            do_next()
    except Exception as e:
        msg = f"下载文件 {name} 时出错: {e}"
        if s:
            s.is_download = False
        messagebox.showerror("err", msg)
        logger.error(msg)


@run_in_thread
def check_file_integrity(zip_file: str, sum_file, s=None, do_next=None):
    msg = ""
    try:
        with open(sum_file, 'r') as f:
            expected_hash = f.read().strip()
    except FileNotFoundError:
        msg = f"错误：文件 {sum_file} 未找到"

    except Exception as e:
        msg = f"读取文件 {sum_file} 时出错: {e}"
    finally:
        if s:
            s.download_text.config(text=f"{msg}")
            s.is_download = False
    try:
        hash_function = hashlib.sha256()
        current_size = 0
        total_size = os.path.getsize(zip_file)
        with open(zip_file, 'rb') as f:
            while chunk := f.read(8192):
                current_size += len(chunk)
                if s:
                    s.download_progress["value"] = (current_size / total_size) * 100
                    s.about_row.update_idletasks()
                    bf = f"{(current_size / total_size) * 100:.1f}%"
                    s.download_text.config(text=f"校验zip完整性{b2mb(current_size)}MB / {b2mb(total_size)}MB {bf}")
                hash_function.update(chunk)
        actual_hash = hash_function.hexdigest()
        if actual_hash == expected_hash:
            msg = f"文件 {zip_file.split('\\')[-1]} 的完整性检查通过！"
            s and s.download_text.config(text=f"{msg}")
            time.sleep(2)
            unzip_file(zip_file, s=s)
        else:
            msg = f"文件 {zip_file.split('\\')[-1]} 的完整性检查失败！\n实际的哈希值: {actual_hash} 期望的哈希值: {expected_hash}"
            logger.error(msg)
            s and s.download_text.config(text=f"{msg}")
    except FileNotFoundError:
        msg = f"错误：文件 {zip_file.split('\\')[-1]} 未找到"
        logger.error(msg)
        s and s.download_text.config(text=f"{msg}")
    except Exception as e:
        msg = f"计算文件 {zip_file.split('\\')[-1]} 的哈希值时出错: {e}"
        logger.error(msg)
        s and s.download_text.config(text=f"{msg}")


def unzip_file(zip_file: str, s):
    try:
        extract_to = os.path.dirname(zip_file)
        total_size = os.path.getsize(zip_file)
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_info_list = zip_ref.infolist()
            current_size = 0
            print(f"开始解压 {zip_file} 到 {extract_to}...")
            for zip_info in zip_info_list:
                zip_ref.extract(zip_info, path=extract_to)
                current_size += zip_info.file_size
                if s:
                    s.download_progress["value"] = (current_size / total_size) * 100
                    s.about_row.update_idletasks()
                    bf = f"{(current_size / total_size) * 100:.1f}%"
                    s.download_text.config(text=f"正在解压 {b2mb(current_size)}MB / {b2mb(total_size)}MB {bf}")
        if s:
            s.is_download = False
            s.download_text.config(text="解压完成！")
        print("解压完成！")
        if is_process_running(read_pid(pid_file)):
            m = kill_process(pid_file)
            s and s.download_text.config(text=m)
            time.sleep(2)
        if is_process_running(read_pid(aut_pid_file)):
            m = kill_process(aut_pid_file)
            s and s.download_text.config(text=m)
            time.sleep(2)
        s and s.download_text.config(text="run update.exe, exit after")
        time.sleep(2)
        if sys.argv[0].endswith(".py"):
            messagebox.showinfo("dev", "源码运行，无需覆盖")
            return
        exe_local = os.path.dirname(sys.argv[0])
        cmd = (f'{os.path.join(exe_local, "update.exe")}'
               f' {os.path.join(extract_to, "report_gui.dist")} {exe_local} {os.getpid()}')
        cmd += " && pause"
        logger.info(cmd)
        os.system(cmd)
        # run update.exe
        # Usage: update <source_dir> <target_dir> <pid>
    except Exception as e:
        if s:
            s.is_download = False
            s.download_text.config(text=f"解压发生错误: {e}")

    # ok, msg = check_file_integrity(os.path.join(temp_dir, "report_gui.dist.0.1.1.zip"),
    #                                os.path.join(temp_dir, "report_gui.dist.0.1.1.zip.sha256.txt"))
    # print(msg)
