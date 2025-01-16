import pygetwindow as gw

import os
import time
import signal
import ctypes
import logging
import requests
import argparse
import subprocess
from urllib.parse import quote
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

script_dir = os.path.dirname(os.path.abspath(__file__))
retry_times = 1
# 尝试从环境变量中获取密钥和URL
report_key = os.getenv('REPORT_KEY')
report_url = os.getenv('REPORT_URL')

parser = argparse.ArgumentParser(description='''定时报告程序，使用pythonw在后台运行(第一次用python前台运行查看是否没问题)
如 python(w) report.py run -u http://127.0.0.1/pcinfo -k '密钥'
''')
subparsers = parser.add_subparsers(dest='command', help='可用的命令')
parser_status = subparsers.add_parser('status', help='查询进程状态')
parser_log = subparsers.add_parser('log', help='查看最新日志')
parser_kill = subparsers.add_parser('kill', help='杀死进程')
parser_run = subparsers.add_parser('run', help='运行定时报告程序')
parser_run.add_argument('-k', '--key', required=report_key is None, help='密钥')
parser_run.add_argument('-u', '--url', required=report_url is None, help='api接口, 如: "http://127.0.0.1/info"')
parser_run.add_argument('--test', action='store_true', help='测试api')
parser_run.add_argument('-c', '--cycle_time', help='报告周期(单位秒)', default=600)

args = parser.parse_args()
if not args.command:
    print("add -h to help")

FORMAT = "%(asctime)-15s [%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger("main")
log_dir = os.path.join(script_dir, 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logfile = os.path.join(log_dir, 'report.log')
# 创建文件日志处理程序
file_handler = TimedRotatingFileHandler(logfile, when="midnight", interval=1,
                                        backupCount=10, encoding="utf-8")
file_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(file_handler)

kernel32 = ctypes.windll.kernel32


# 获取进程句柄
def GetProcessHandle(pid):
    handle = kernel32.OpenProcess(0x0400, False, pid)
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
        with open(os.path.join(script_dir, '.pid'), 'r') as fi:
            pid = int(fi.read())
        return pid
    except FileNotFoundError:
        print("没有找到进程ID文件.")


def check_process():
    try:
        pid = read_pid()
        print(f"进程ID: {pid}")
        if is_process_running(pid):
            print(f"进程正在运行")
            cmdline_result = subprocess.run(
                ['wmic', 'process', 'where', f'ProcessId={pid}', 'get', 'CommandLine', '/value'],
                capture_output=True, text=True, check=True
            )
            cmdline = cmdline_result.stdout.strip().split('=')[1] if '=' in cmdline_result.stdout else 'N/A'
            memusage_result = subprocess.run(
                ['wmic', 'process', 'where', f'ProcessId={pid}', 'get', 'WorkingSetSize', '/value'],
                capture_output=True, text=True, check=True
            )
            memusage = int(memusage_result.stdout.strip().split('=')[1]) if '=' in memusage_result.stdout else 0
            memusage_mb = memusage // 1024 ** 2
            print(f"工作集内存使用: {memusage_mb} MB")
            print(f"命令行参数: {cmdline}")
        else:
            print("进程已停止.")
    except (FileNotFoundError, ValueError):
        print("没有找到进程ID文件或进程不存在.")


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


def get_active_window_title() -> str:
    active_window = gw.getActiveWindow()
    if active_window:
        # if "Google Chrome" in active_window.title:
        #     return "Google Chrome"
        if active_window.title == "LockingWindow" or active_window.title == "就像你看到的图像一样？选择以下选项":
            return "锁屏"
        if not active_window.title:
            time.sleep(1)
            active_window = gw.getActiveWindow()
        return active_window.title
    else:
        return "桌面"


# 发送数据到Flask API
def send_data_to_api(running_exe, report_time):
    global retry_times
    url = args.url
    payload = {
        'key': args.key,
        'type': 'pc',
        'running_exe': quote(running_exe),  # 进行URL编码
        'report_time': report_time
    }
    try:
        response = requests.get(url, params=payload)
        msg = response.text
        if "error key" in msg:
            logger.error(f"{url=},{str(payload)=},key={args.key} error key")
        else:
            logger.info(f"{running_exe}  {msg}")
    except Exception as e:
        msg = str(e)
        logger.error(f"{url=},{str(payload)=},{msg=}")
        if retry_times:
            logger.info(f"{retry_times=}")
            send_data_to_api(running_exe, report_time)
            retry_times -= 1


def logcat():
    red = '\033[91m'
    end = '\033[0m'
    if not os.path.exists(logfile):
        print(f"文件 {logfile} 不存在")
        return
    print(f"{logfile=}")
    with open(logfile, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "[INFO]" not in line:
                print(f"{red}{line}{end}")
            else:
                print(line)


# 主程序
def main():
    print("start...5")
    time.sleep(5)
    while True:
        title = get_active_window_title()
        times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_data_to_api(title, times)
        time.sleep(args.cycle_time)


if __name__ == "__main__":

    if args.command == 'run':
        logger.info("start".center(50, '-'))
        logger.info(f"环境变量 {report_url=},{report_key=}".center(50, ' '))
        logger.info(f"{args.url=},{args.key=}".center(50, ' '))
        if args.test:
            # time.sleep(1)
            title_t = get_active_window_title()
            time_t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_data_to_api(title_t, time_t)
            exit(0)
        p = read_pid()
        if is_process_running(p):
            print(f"进程 pid={p} 已经在运行勿重复执行。如果这不是本程序（查看任务管理器搜索python），删除.pid文件后重试")
            check_process()
            exit(0)
        # 保存进程ID到文件
        with open(os.path.join(script_dir, '.pid'), 'w') as f:
            f.write(str(os.getpid()))
        main()
    elif args.command == 'status':
        check_process()
    elif args.command == 'kill':
        kill_process()
    elif args.command == 'log':
        logcat()
