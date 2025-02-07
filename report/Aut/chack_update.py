import hashlib
import os
import queue
import threading
import time
from functools import wraps
from tkinter import messagebox

import requests

from .logger import logger, APPDATA

temp_dir = os.path.join(APPDATA, 'temp')


def run_in_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result_queue = queue.Queue()

        def thread_target():
            result = func(*args, **kwargs)
            result_queue.put(result)

        thread = threading.Thread(target=thread_target)
        thread.daemon = True  # 设置为守护线程
        thread.start()
        return result_queue, thread

    return wrapper


def test_conn():
    try:
        start_time = time.time()
        requests.get("https://api.github.com/")
        github_time = time.time() - start_time
        start_time = time.time()
        v2 = requests.get("https://gitee.com/api/v5/repos/qwe2412322029").status_code == 200
        gitee_time = time.time() - start_time
        print(f"gitee={gitee_time * 1000:.0f}ms,github={github_time * 1000:.0f}ms")
        if github_time > gitee_time and v2:
            print("use gitee")
            return False
        else:
            print("use github")
            return True
    except Exception as e:
        raise Exception(f"无法连接到任何服务 {e}")


def get_update_info():
    try:
        if test_conn():
            url = "https://api.github.com/repos/2412322029/seeme/releases/latest"
        else:
            url = "https://gitee.com/api/v5/repos/qwe2412322029/seeme/releases/latest"
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
            return {
                "version": tag_name,
                "published_at": published_at,
                "body": body,
                "assets": my_assets
            }
        else:
            messagebox.showerror("错误", f"检查更新失败，\n"
                                         f"{url=}\n状态码: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("错误", f"检查更新失败: {e}")


@run_in_thread
def download_file(name, url, save_dir, progress_callback=None, when_ok=None):
    logger.info(f"download {url}")
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, name)
    temp_path = save_path + ".tmp"  # 临时文件路径
    try:
        # response = requests.get(url, stream=True)
        # response.raise_for_status()
        # total_size = int(response.headers.get('content-length', 0))
        # with open(temp_path, 'wb') as file:
        #     current_size = 0
        #     for chunk in response.iter_content(chunk_size=8192):
        #         if chunk:
        #             file.write(chunk)
        #             current_size += len(chunk)
        #             if progress_callback:
        #                 progress_callback(current_size, total_size)
        # os.rename(temp_path, save_path)
        print(f"开始模拟下载：{url}")
        total_size = 1024 * 1024 * 10
        current_size = 0
        while current_size < total_size:
            chunk_size = min(8192, total_size - current_size)
            current_size += chunk_size
            if progress_callback:
                progress_callback(current_size, total_size)
            time.sleep(0.02)
        print("文件下载完成")

        msg = f"文件 {name} 已成功下载到 {save_path}"
        logger.info(msg)
        if when_ok:
            when_ok()
    except Exception as e:
        msg = f"下载文件 {name} 时出错: {e}"
        messagebox.showerror("err", msg)
        logger.error(msg)


@run_in_thread
def check_file_integrity(zip_file: str, sum_file, progress_callback=None, t=None, do_next=None):
    msg = ""
    try:
        with open(sum_file, 'r') as f:
            expected_hash = f.read().strip()
    except FileNotFoundError:
        msg = f"错误：文件 {sum_file} 未找到"
    except Exception as e:
        msg = f"读取文件 {sum_file} 时出错: {e}"
    finally:
        if t:
            t.config(text=f"{msg}")
    try:
        hash_function = hashlib.sha256()
        current_size = 0
        total_size = os.path.getsize(zip_file)
        with open(zip_file, 'rb') as f:
            while chunk := f.read(8192):
                current_size += len(chunk)
                if progress_callback:
                    progress_callback(current_size, total_size)
                hash_function.update(chunk)
        actual_hash = hash_function.hexdigest()
        if actual_hash == expected_hash:
            msg = f"文件 {zip_file.split('\\')[-1]} 的完整性检查通过！"
            # here is ok
            if do_next:
                do_next()  # 解压文件，覆盖
        else:
            msg = f"文件 {zip_file.split('\\')[-1]} 的完整性检查失败！\n实际的哈希值: {actual_hash} 期望的哈希值: {expected_hash}"
    except FileNotFoundError:
        msg = f"错误：文件 {zip_file.split('\\')[-1]} 未找到"
    except Exception as e:
        msg = f"计算文件 {zip_file.split('\\')[-1]} 的哈希值时出错: {e}"
    finally:
        if t:
            t.config(text=f"{msg}")


if __name__ == '__main__':
    print(get_update_info())

    # def callback(current_size, total_size):
    #     percent = (current_size / total_size) * 100
    #     print(f"下载进度: {percent:.2f}%", end="\r")
    #
    #
    # e, m = download_file('report_gui.dist.0.1.1.zip',
    #                      'https://github.com/2412322029/seeme/releases/download/v0.1.1/report_gui.dist.0.1.1.zip',
    #                      f"{temp_dir}",
    #                      progress_callback=callback)
    # print(e, m)

    # ok, msg = check_file_integrity(os.path.join(temp_dir, "report_gui.dist.0.1.1.zip"),
    #                                os.path.join(temp_dir, "report_gui.dist.0.1.1.zip.sha256.txt"))
    # print(msg)
