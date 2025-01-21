import os
import time
import signal
import logging
import requests
import argparse
import subprocess
from pprint import pprint
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

try:
    from PIL import Image  # pip install pillow
    import psutil  # pip install psutil
    import win32process  # pip install pywin32
    import win32gui
    import win32ui
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module Not Found. pip install pillow,psutil,pywin32")

script_dir = os.path.dirname(os.path.abspath(__file__))
ICON_FOLDER = os.path.join(script_dir, "exe_icon")
ServerIcon = []
retry_times = 1
os.makedirs(ICON_FOLDER, exist_ok=True)
# 尝试从环境变量中获取密钥和URL
report_key = os.getenv('REPORT_KEY')
report_url = os.getenv('REPORT_URL')


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue


parser = argparse.ArgumentParser(description='''定时报告程序，可以从环境变量中获取 REPORT_KEY 和 REPORT_URL
''')
subparsers = parser.add_subparsers(dest='command', help='可用的命令')
parser_status = subparsers.add_parser('status', help='查询进程状态')
parser_log = subparsers.add_parser('log', help='查看最新日志')
parser_kill = subparsers.add_parser('kill', help='杀死进程')

parent_key_parser = argparse.ArgumentParser(add_help=False)
parent_key_parser.add_argument('-k', '--key', required=report_key is None, help='密钥')
parent_url_parser = argparse.ArgumentParser(add_help=False)
parent_url_parser.add_argument('-u', '--url', required=report_url is None, help='api接口, 如: http://127.0.0.1')

parser_run = subparsers.add_parser('run', help='运行定时报告程序(使用pythonw可在后台运行)',
                                   parents=[parent_key_parser, parent_url_parser])
parser_run.add_argument('--test', action='store_true', help='测试api')
parser_run.add_argument('-c', '--cycle_time', type=positive_int, help='报告周期(单位秒)', default=600)
# 服务器端命令
parser_get = subparsers.add_parser('getlimit', help='获取服务器限制值', parents=[parent_url_parser])
parser_get_info = subparsers.add_parser('getinfo', help='获取服务器数据', parents=[parent_url_parser])
parser_get_info.add_argument('-t', '--type', help='数据类型如 pc phone..')

parser_del_info = subparsers.add_parser('delinfo', help='删除服务器数据',
                                        parents=[parent_key_parser, parent_url_parser])
parser_del_info.add_argument('-t', '--type', required=True, help='要删除数据的类型，如 pc phone..')
parser_del_info.add_argument('-rt', '--report_time', required=True, help='要删除数据的时间')


class LimitAction(argparse.Action):
    def __call__(self, pa, namespace, values, option_string=None):
        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        limits = getattr(namespace, self.dest)

        if len(values) % 2 != 0:
            raise argparse.ArgumentError(self, "--type-number 后面参数必须成对出现(type and number)")
        for i in range(0, len(values), 2):
            limit_type = values[i]
            try:
                limit_number = int(values[i + 1])
                if limit_number < 0 or limit_number > 100:
                    raise argparse.ArgumentError(self, f"限制行数必须在0到100之间: {limit_number}")
            except ValueError:
                raise argparse.ArgumentError(self, f"限制行数必须是整数: {values[i + 1]}")
            limits.append((limit_type, limit_number))
        setattr(namespace, self.dest, limits)


parser_set = subparsers.add_parser('setlimit', help='设置服务器数据最大个数',
                                   parents=[parent_key_parser, parent_url_parser])
parser_set.add_argument('-tn', '--type-number', nargs='+', action=LimitAction, required=True,
                        dest='limits', help="限制类型 'pc', 'browser', 'phone' 和对应的限制行数")

args = parser.parse_args()
# 确保 args.key 和 args.url 存在
if not hasattr(args, 'key'):
    args.key = None
if not hasattr(args, 'url'):
    args.url = None
if not args.command:
    print("add -h to help")
if report_key and not args.key:
    args.key = report_key
    if args.command not in ["log", "kill"]:
        print(f"-k/--key ?,使用环境变量 report_key='{report_key[:6]}*******'")
if report_url and not args.url:
    args.url = report_url
    if args.command not in ["log", "kill"]:
        print(f"-u/--url ?,使用环境变量 {report_url=}")

FORMAT = "%(asctime)-15s [%(levelname)s] [%(funcName)s:%(lineno)d] %(message)s"
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


# 获取进程句柄
# 检查进程是否存在
def is_process_running(pid):
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False


# 读取进程ID文件
def read_pid():
    pid_file_path = os.path.join(script_dir, '.pid')
    try:
        with open(pid_file_path, 'r') as fi:
            pid = int(fi.read())
        return pid
    except FileNotFoundError:
        print("没有找到进程ID文件.")
        return None
    except ValueError:
        print("进程ID文件内容无效.")
        return None


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


def get_allIcon():
    try:
        all_entries = os.listdir(ICON_FOLDER)
        filenames = [entry.split(".png")[0] for entry in all_entries if
                     os.path.isfile(os.path.join(ICON_FOLDER, entry))]
        return filenames
    except Exception as e:
        logger.error(f"{e}")
        return []


def save_exe_icon(exe_path, exe_name: str):
    if os.path.exists(f"{ICON_FOLDER}/{exe_name}.png"):
        return True
    try:
        large, _ = win32gui.ExtractIconEx(exe_path, 0)
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        if large:
            hdc.DrawIcon((0, 0), large[0])
            win32gui.DestroyIcon(large[0])
        else:
            return False
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGBA',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRA', 0, 1)
        img.save(f"{ICON_FOLDER}/{exe_name}.png", format="PNG")
        logger.info(f"{exe_name}.png save successfully!")
        return True
    except Exception as e:
        logger.error(str(e))
        return False


def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    exe_name = psutil.Process(pid).name()
    exe_path = psutil.Process(pid).exe()
    title = win32gui.GetWindowText(hwnd)
    hicon = save_exe_icon(exe_path, exe_name)
    # print(title, exe_name)
    if not title:
        return "桌面", exe_name, hicon
    else:
        return title, exe_name, hicon


def get_all_window_info():
    call_results = set()
    result = list()

    def enum_windows_callback(hwnd, results):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            exe_name = psutil.Process(pid).name()
            exe_path = psutil.Process(pid).exe()
            title = win32gui.GetWindowText(hwnd)
            if not title or not exe_name:
                return
            if exe_name in ["TextInputHost.exe", "SystemSettings.exe", "NVIDIA Overlay.exe", "svchost.exe"]:
                return
            if exe_name == 'explorer.exe' and title == "Program Manager":
                return
            hicon = save_exe_icon(exe_path, exe_name)
            process_info = {"exe_name": exe_name, "title": title}
            result.append(process_info)
            call_results.add((exe_name, title, hicon))
        except Exception as e:
            logger.error(f"Error in enum_windows_callback: {e}")

    win32gui.EnumWindows(enum_windows_callback, call_results)
    upload_files = []
    for r in call_results:
        if r[2]:
            upload_files.append(r[0] + ".png")
    if upload_files:
        upload_icon(upload_files)
    return {"activity_window": result, "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# 发送数据到Flask API
def send_data_to_api(running_exe, report_time, exe_name, other: dict):
    url = args.url + "/set_info"
    headers = {
        'API-KEY': args.key
    }
    payload = {
        'type': 'pc',
        'running_exe': running_exe,
        'exe_name': exe_name,
        'other': other,
        'report_time': report_time
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            logger.error(f"{url=},{headers=},{str(payload)=},{response.text}")
        else:
            logger.info(f"{running_exe}  {response.json()}")
    except Exception as e:
        msg = str(e)
        logger.error(f"{url=},{str(payload)=},{msg=}")
        global retry_times
        if retry_times > 0:
            retry_times -= 1
            logger.info(f"Retrying... {retry_times=}")
            send_data_to_api(running_exe, report_time, exe_name, other)


def get_limit():
    response = requests.get(args.url + "/get_limit").text
    print(response)


def set_limit():
    url = args.url + "/set_limit"
    headers = {
        'API-KEY': args.key
    }
    try:
        payload = {limit_type: limit_number for limit_type, limit_number in args.limits}
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f"Limits set successfully: {response.json()}")
        else:
            logger.error(f"Failed to set limits: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    except ValueError as e:
        logger.error(f"JSON error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def get_allServerIcon():
    url = args.url + "/get_allIcon"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            ServerIcon.extend(response.json())
            logger.info(f"Server has Icon :{ServerIcon}")
            return
        else:
            logger.error(f"Failed to get all server icon: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def upload_icon(filenames: list[str]):
    filter_filenames = []
    for fi in filenames:
        if fi not in [f"{s}.png" for s in ServerIcon]:  # 只上传服务器没有的
            filter_filenames.append(fi)
    if not filter_filenames:
        print(f"skip upload,but {filenames} in ServerIcon")
        return
    url = args.url + "/upload_exeIcon"
    headers = {'API-KEY': args.key}
    try:
        files_to_upload = []
        logger.info(f"ServerIcon not have {filter_filenames} try upload ")
        for filename in filter_filenames:
            files_to_upload.append(
                ("files", (filename, open(os.path.join(ICON_FOLDER, filename), "rb"), "application/octet-stream")))
        response = requests.post(url, headers=headers, files=files_to_upload)
        if response.status_code == 200:
            ServerIcon.extend([f.split(".png")[0] for f in filter_filenames])  # 上传成功后更新服务器icon list
            logger.info(f"ServerIcon 更新后->{ServerIcon}")
            logger.info(f"{response.json()}")
        else:
            logger.error(f"Failed to upload icon{filter_filenames}: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def get_info():
    response = requests.get(args.url + f"/get_info?type={args.type}").json()
    pprint(response)


def del_info():
    headers = {
        'API-KEY': args.key,
        'Content-Type': 'application/json'
    }
    payload = {
        'type': args.type,
        'report_time': args.report_time
    }
    try:
        response = requests.post(args.url + "/del_info", headers=headers, json=payload)
        if response.status_code == 200:
            res = response.json()
            print(f"{res['message']}")
        elif response.status_code == 404:
            logger.error(f"{response.text}")
        else:
            logger.error(f"Failed to delete items: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")


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
    get_allServerIcon()
    time.sleep(5)
    while True:
        title, exe_name, hicon = get_active_window_title()
        times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        send_data_to_api(running_exe=title, report_time=times, exe_name=exe_name, other=get_all_window_info())
        if hicon:
            upload_icon([exe_name + ".png"])
        time.sleep(int(args.cycle_time))


if __name__ == "__main__":
    if args.command == 'run':
        logger.info("start".center(50, '-'))
        logger.info(f"环境变量 {report_url=},report_key='{report_key[:6]}*******'".center(50, ' '))
        logger.info(f"{args.url=},args.key='{args.key[:6]}*******'".center(50, ' '))
        if args.test:
            time.sleep(1)
            get_allServerIcon()
            title_t, exe_name_t, hicon_t = get_active_window_title()
            time_t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            send_data_to_api(running_exe=title_t, report_time=time_t, exe_name=exe_name_t, other=get_all_window_info())
            if hicon_t:
                upload_icon([exe_name_t + ".png"])
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
    elif args.command == 'getlimit':
        get_limit()
    elif args.command == 'setlimit':
        set_limit()
    elif args.command == 'getinfo':
        get_info()
    elif args.command == 'delinfo':
        del_info()
