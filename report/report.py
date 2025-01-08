import signal
import time
from urllib.parse import quote

import pygetwindow as gw
import requests
from datetime import datetime
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import argparse
import ctypes

parser = argparse.ArgumentParser(description='''定时报告程序，使用pythonw在后台运行(第一次用python前台运行查看是否没问题)
如 python(w) report.py run -u http://127.0.0.1/pcinfo -k '密钥'
''')
subparsers = parser.add_subparsers(dest='command', help='可用的命令')
parser_status = subparsers.add_parser('status', help='查询进程状态')
parser_kill = subparsers.add_parser('kill', help='杀死进程')
parser_run = subparsers.add_parser('run', help='运行定时报告程序')
parser_run.add_argument('-k', '--key', required=True, help='密钥')
parser_run.add_argument('-u', '--url', required=True, help='api接口, 如: "http://127.0.0.1/info"')
parser_run.add_argument('-c', '--cycle_time', help='报告周期(单位秒)', default=600)

args = parser.parse_args()
if not args.command:
    print("add -h to help")
FORMAT = "%(asctime)-15s [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("main")
if not os.path.exists("log"):
    os.makedirs("log")

# 创建文件日志处理程序
file_handler = TimedRotatingFileHandler("log/report.log", when="midnight", interval=1, backupCount=10, encoding="utf-8")
file_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(file_handler)

kernel32 = ctypes.windll.kernel32


# 获取进程句柄
def GetProcessHandle(pid):
    PROCESS_QUERY_INFORMATION = 0x0400
    handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)
    return handle


# 检查进程是否存在
def is_process_running(pid):
    handle = GetProcessHandle(pid)
    if handle:
        kernel32.CloseHandle(handle)
        return True
    else:
        return False


def read_pid():
    try:
        with open(".pid", 'r') as f:
            pid = int(f.read())
        return pid
    except FileNotFoundError:
        print("没有找到进程ID文件.")


def check_process():
    try:
        pid = read_pid()
        print(f"进程ID: {pid}")
        if is_process_running(pid):
            print(f"进程正在运行")
            return True
        else:
            print("进程已停止.")
            return False
    except (FileNotFoundError, ValueError):
        print("没有找到进程ID文件或进程不存在.")
        return False


def kill_process():
    # 杀死进程
    try:
        pid = read_pid()
        if is_process_running(pid):
            os.kill(pid, signal.SIGTERM)
            print(f"进程 pid={pid} 已被杀死.")
        else:
            print(f"进程 {pid} 不存在.")
    except Exception as e:
        print(f"杀死进程时出错: {e}")


def get_active_window_title():
    active_window = gw.getActiveWindow()
    if active_window:
        if "Google Chrome" in active_window.title:
            return "Google Chrome"
        if active_window.title == "LockingWindow" or active_window.title == "就像你看到的图像一样？选择以下选项":
            return "锁屏"
        return active_window.title
    else:
        return "桌面"


# 发送数据到Flask API
def send_data_to_api(running_exe, report_time):
    try:
        url = args.url
        payload = {
            'key': args.key,
            'type': 'pc',
            'running_exe': quote(running_exe),  # 进行URL编码
            'report_time': report_time
        }
        response = requests.get(url, params=payload)
        msg = response.text
    except Exception as e:
        msg = str(e)
    return msg


# 主程序
def main():
    print("start...5")
    time.sleep(5)
    while True:
        title = get_active_window_title()
        times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = send_data_to_api(title, times)
        logger.info(f"{title}  {result[:20]}")
        time.sleep(args.cycle_time)


if __name__ == "__main__":

    if args.command == 'run':
        p = read_pid()
        if is_process_running(p):
            print(f"进程 pid={p} 已经在运行勿重复执行。如果这不是本程序（查看任务管理器搜索python），删除.pid文件后重试")
            exit(0)
        # 保存进程ID到文件
        with open('.pid', 'w') as f:
            f.write(str(os.getpid()))
        main()
    elif args.command == 'status':
        check_process()
    elif args.command == 'kill':
        kill_process()
