import os
import signal

import psutil

from .logger import APPDATA

pause_file = os.path.join(APPDATA, "report.pause")  # 暂停flag文件路径
pid_file = os.path.join(APPDATA, "report.pid")  # 保存进程pid
icon_dir = os.path.join(APPDATA, "exe_icon")  # exe icon 路径
sqlite_file = os.path.join(APPDATA, "app_usage.db")
aut_pid_file = os.path.join(APPDATA, "aut.pid")  # 保存进程pid
os.makedirs(icon_dir, exist_ok=True)


def read_pid(pf):
    try:
        with open(pf, "r") as fi:
            pid = int(fi.read())
        return pid
    except FileNotFoundError:
        # print("没有找到进程ID文件.")
        return None
    except ValueError:
        print("进程ID文件内容无效.")
        return None


def is_process_running(pid):
    try:
        if pid is None:
            return False
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False


def kill_process(pf):
    # 杀死进程
    msg = ""
    try:
        pid = read_pid(pf)
        if is_process_running(pid):
            os.kill(pid, signal.SIGTERM)
            msg = f"进程 pid={pid} 已被杀死."
            return msg
        else:
            msg = f"进程 {pid} 不存在."
            return msg
    except Exception as e:
        msg = f"杀死进程时出错: {e}"
        return msg
    finally:
        print(msg)
