import argparse
import os
import sys
import time
import traceback
from datetime import datetime
from pprint import pprint

import Aut
from Aut import read_pid, is_process_running, kill_process, pause_file, pid_file, icon_dir
from Aut.config import cfg
from Aut.logger import logger, log_file

try:
    import requests  # pip install requests
    from PIL import Image  # pip install pillow
    import psutil  # pip install psutil
    import win32process  # pip install pywin32
    import win32gui
    import win32ui
except ModuleNotFoundError:
    raise ModuleNotFoundError("Module Not Found. pip install pillow,psutil,pywin32,requests")

report_key = cfg.get("DEFAULT", "key", fallback="")
report_url = cfg.get("DEFAULT", "url", fallback="")
ServerIcon = []  # 服务器的icon列表
retry_times = 1  # 失败重试次数
# 排除的活动进程
Exclude_Process = cfg.get("DEFAULT", "exclude_process", fallback="").split(",")


# logger.info(f"{Exclude_Process=}")


# 检查进程是否存在


def timeAgo(t: datetime):
    current_time = datetime.now()
    time_diff = current_time - t
    days = time_diff.days
    hours = time_diff.seconds // 3600
    minutes = (time_diff.seconds % 3600) // 60
    seconds = time_diff.seconds % 60
    time_diff_str = ""
    if days > 0:
        time_diff_str += f"{days} days "
    if hours > 0:
        time_diff_str += f"{hours} hours "
    if minutes > 0:
        time_diff_str += f"{minutes} minutes "
    if seconds > 0 or not time_diff_str:
        time_diff_str += f"{seconds} seconds"
    return f"{time_diff_str}"


def ifPrint(*values: object, IF: bool) -> None:
    if IF:
        print(*values)


def check_process(pf, check_pause=True, pt=True):
    err = None
    info = {}
    try:
        pid = read_pid(pf)
        info["pid"] = pid
        ifPrint(f"pid(file)   :{pid}", IF=pt)
        if is_process_running(pid):
            process = psutil.Process(pid)
            info["status"] = process.status()
            rss = process.memory_info().rss
            info["memory"] = f'{rss // (1024 ** 2)}'
            info["cmdline"] = " ".join(process.cmdline())
            create_time = datetime.fromtimestamp(process.create_time())
            info["create_time"] = (f"{create_time.strftime('%Y-%m-%d %H:%M:%S')}  "
                                   f"({timeAgo(create_time)} ago)")
            ifPrint(f"status      : \033[92m{info['status']}\033[0m", IF=pt)
            ifPrint(f"mem(rs     ): {info['memory']} MB", IF=pt)
            ifPrint(f"cmdline     : {info['cmdline']}", IF=pt)
            ifPrint(f"create time : {create_time.strftime('%Y-%m-%d %H:%M:%S')}  "
                    f"(\033[92m{timeAgo(create_time)}\033[0m ago)", IF=pt)
            if os.path.exists(pause_file) and check_pause:
                info["status"] = "paused"
                getctime = datetime.fromtimestamp(os.path.getctime(pause_file))
                info["paused"] = f"{getctime} ({timeAgo(getctime).strip()} ago!)"
                ifPrint(f"The process was paused at  {getctime} (\033[91m{timeAgo(getctime).strip()}\033[0m ago!)",
                        IF=pt)
        else:
            info["status"] = "stop"
            ifPrint(f"status      : \033[91mstop\033[0m", IF=pt)
    except (FileNotFoundError, ValueError) as e:
        err = str(e)
        logger.error(f"没有找到进程ID文件或进程不存在. {e}")
    except Exception as e:
        err = str(e)
        logger.error(f"发生未知错误: {e}")
    return err, info


def get_allIcon():
    try:
        all_entries = os.listdir(icon_dir)
        filenames = [entry for entry in all_entries if
                     os.path.isfile(os.path.join(icon_dir, entry))]
        return filenames
    except Exception as e:
        logger.error(f"{e}")
        return []


def save_exe_icon(exe_path, exe_name: str, a=32):
    # 多线程环境下可能表现不稳定，保存部分图片,tk部分设置a=48保存正常??
    # 与图标绘制的设备上下文（DC）相关
    if not os.path.exists(exe_path):
        logger.info(f"文件 {exe_path} 不存在，跳过保存")
        return
    if os.path.exists(f"{icon_dir}/{exe_name}.png"):
        return True
    try:
        large, small = win32gui.ExtractIconEx(exe_path, 0)
        if small:
            win32gui.DestroyIcon(small[0])
        if not large:
            return False
        hwnd = win32gui.GetDesktopWindow()
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(hwnd))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, a, a)
        hdc_hwnd = hdc.CreateCompatibleDC()
        hdc_hwnd.SelectObject(hbmp)
        hdc_hwnd.DrawIcon((0, 0), large[0])
        win32gui.DestroyIcon(large[0])
        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        print(bmpinfo, len(bmpstr))
        img = Image.frombuffer(
            'RGBA',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRA', 0, 1)
        img = img.resize((32, 32))
        img.save(f"{icon_dir}/{exe_name}.png", format="PNG")
        logger.info(f"{exe_name}.png save successfully!")
        return True
    except Exception as e:
        logger.error(f"Error saving icon for {exe_name}: {e}")
        return False


# TODO 对title进行正则过滤
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


def get_all_window_info(args):
    call_results = set()
    result = list()

    def enum_windows_callback(hwnd, mycall_results):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            exe_name = psutil.Process(pid).name()
            exe_path = psutil.Process(pid).exe()
            title = win32gui.GetWindowText(hwnd)
            if not title or not exe_name:
                return
            if exe_name in Exclude_Process:
                return
            if exe_name == 'explorer.exe' and title == "Program Manager":
                return
            hicon = save_exe_icon(exe_path, exe_name)
            process_info = {"exe_name": exe_name, "title": title}
            result.append(process_info)
            mycall_results.add((exe_name, title, hicon))
        except Exception as e:
            logger.error(f"Error in enum_windows_callback: {e}")

    win32gui.EnumWindows(enum_windows_callback, call_results)
    upload_files = []
    for r in call_results:
        if r[2]:
            upload_files.append(r[0] + ".png")
    if upload_files:
        upload_icon(args, upload_files)
    return {"activity_window": result, "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


# 发送数据到Flask API
def send_data_to_api(args, running_exe, report_time, exe_name, other: dict):
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
            send_data_to_api(args, running_exe, report_time, exe_name, other)


def get_limit(args):
    response = requests.get(args.url + "/get_limit").text
    print(response)


def set_limit(args):
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


def get_allServerIcon(args):
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


def upload_icon(args, filenames: list[str]):
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
                ("files", (filename, open(os.path.join(icon_dir, filename), "rb"), "application/octet-stream")))
        response = requests.post(url, headers=headers, files=files_to_upload)
        if response.status_code == 200:
            ServerIcon.extend([f.split(".png")[0] for f in filter_filenames])  # 上传成功后更新服务器icon list
            logger.info(f"ServerIcon 更新后->{ServerIcon}")
            logger.info(f"{response.json()}")
        else:
            logger.error(f"Failed to upload {url} icon {filter_filenames}: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


def get_info(args):
    response = requests.get(args.url + f"/get_info?type={args.type}").json()
    pprint(response)


def del_info(args):
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


def pause_process():
    """暂停进程"""
    if not is_process_running(read_pid(pid_file)):
        print("process is not running.")
        return
    if not os.path.exists(pause_file):
        open(pause_file, "w").close()
        logger.info("Process paused.")
    else:
        print("Process is already paused.")


def resume_process():
    """恢复进程"""
    if not is_process_running(read_pid(pid_file)):
        print("process is not running.")
        return
    if os.path.exists(pause_file):
        os.remove(pause_file)
        logger.info("Process resumed.")
    else:
        print("Process is already running.")


def logcat(tail=10, pt=True, lf=log_file):
    red = '\033[91m'
    end = '\033[0m'
    try:
        with open(lf, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except Exception as e:
        ifPrint(f"读取文件时出错: {e}", IF=pt)
        return [f"读取文件时出错: {e}"]
    # 只显示最后几行
    lines = lines[-tail:]

    for line in lines:
        line = line.strip()
        if "[INFO]" not in line:
            ifPrint(f"{red}{line}{end}", IF=pt)
        else:
            ifPrint(line, IF=pt)
    return lines


def args_parser():
    def check_cycle_time(value):
        try:
            value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value} 不是一个有效的整数")
        if value <= 10:
            raise argparse.ArgumentTypeError(f"报告周期必须大于 10 秒，当前值为 {value}")
        return value

    parser = argparse.ArgumentParser(description='''定时报告命令行程序''')
    parser.add_argument('-v', '--version', action='store_true', help='显示版本')
    subparsers = parser.add_subparsers(dest='command', help='可用的命令')
    parser_log = subparsers.add_parser('log', help='查看最新日志')
    parser_log.add_argument("-t", "--tail", type=int, nargs="?", default=10, help="显示的最后几行，默认为10行")
    subparsers.add_parser('status', help='查询进程状态')
    subparsers.add_parser('kill', help='杀死进程')
    subparsers.add_parser('pause', help='暂停进程')
    subparsers.add_parser('resume', help='恢复进程')
    parent_key_parser = argparse.ArgumentParser(add_help=False)
    parent_key_parser.add_argument('-k', '--key', required=report_key is None, help='密钥')
    parent_url_parser = argparse.ArgumentParser(add_help=False)
    parent_url_parser.add_argument('-u', '--url', required=report_url is None, help='api接口, 如: http://127.0.0.1')
    parser_run = subparsers.add_parser('run', help='运行定时报告程序',
                                       parents=[parent_key_parser, parent_url_parser])
    parser_run.add_argument('--test', action='store_true', help='测试api')
    parser_run.add_argument('--without_check', action='store_true', help='不检查进程是否存在')
    parser_run.add_argument('-c', '--cycle_time', type=check_cycle_time, help='报告周期(单位秒)', default=600)
    # 服务器端命令
    subparsers.add_parser('getlimit', help='获取服务器限制值', parents=[parent_url_parser])
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
    parser_aut = subparsers.add_parser('aut', help='运行应用使用时间统计, 定时上传app_usage.db到服务器(未完成)', )
    # parents=[parent_key_parser, parent_url_parser]
    parser_aut.add_argument('--status', action='store_true', help='查询 "应用使用时间统计" 的进程状态 and exit')
    parser_aut.add_argument('--kill', action='store_true', help='杀死 "应用使用时间统计" 进程 and exit')
    parser_aut.add_argument('--analysis', action='store_true', help='显示应用使用时间统计')
    parser_aut.add_argument('--without_check', action='store_false', help='不检查进程是否存在')

    parser_args = parser.parse_args()
    # 确保 args.key 和 args.url 存在
    if not hasattr(parser_args, 'key'):
        parser_args.key = None
    if not hasattr(parser_args, 'url'):
        parser_args.url = None
    if report_key and not parser_args.key:
        parser_args.key = report_key
    if report_url and not parser_args.url:
        parser_args.url = report_url
    if not hasattr(parser_args, 'without_check'):
        parser_args.without_check = False
    return parser_args, parser


# def upload_db(args, sql_path: str):
#     try:
#         # TODO upload_db
#         for o in Aut.get_all_names():
#             save_exe_icon(o, o.split('\\')[-1])
#         # upload_icon(args, get_allIcon())
#         print("upload_db")
#     except Exception as e:
#         logger.error(f"{e}")


def run_aut(check=True):
    try:
        if check:
            p = read_pid(Aut.aut_pid_file)
            if is_process_running(p):
                logger.error(
                    f"应用使用时间统计 进程 pid={p} 已经在运行勿重复执行。如果这不是本程序 删除aut.pid文件后重试")
                check_process(Aut.aut_pid_file, check_pause=False)
                sys.exit(0)
        logger.info("start-aut".center(50, '-'))
        Aut.run()
    except Exception as e:
        logger.fatal(f"{e}")
        sys.exit(-1)


def run(args, check=True):
    try:
        if check:
            p = read_pid(pid_file)
            if is_process_running(p):
                logger.error(f"report 进程 pid={p} 已经在运行勿重复执行。如果这不是本程序，删除report.pid文件后重试")
                check_process(pid_file)
                sys.exit(0)
        # 保存进程ID到文件
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))
        print("start...5")
        logger.info("start".center(50, '-'))
        get_allServerIcon(args)
        time.sleep(5)
        while True:
            if not os.path.exists(pause_file):
                result = get_active_window_title()
                if result is None:
                    continue  # 如果 result 为 None，则跳过本次循环
                title, exe_name, hicon = result
                times = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                send_data_to_api(args, running_exe=title, report_time=times, exe_name=exe_name,
                                 other=get_all_window_info(args))
                if hicon:
                    upload_icon(args, [exe_name + ".png"])
            time.sleep(int(args.cycle_time))
    except Exception as e:
        error_message = traceback.format_exc()
        logger.fatal(f"发生异常终止程序运行：{e}\n{error_message}")
        sys.exit(-1)


def test_run(args):
    logger.info(f"配置文件 {report_url=},report_key='{report_key[:6]}*******'".center(50, ' '))
    logger.info(f"{args.url=},args.key='{args.key[:6]}*******'".center(50, ' '))
    time.sleep(1)
    get_allServerIcon(args)
    title_t, exe_name_t, hicon_t = get_active_window_title()
    time_t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_data_to_api(args, running_exe=title_t, report_time=time_t, exe_name=exe_name_t,
                     other=get_all_window_info(args))
    if hicon_t:
        upload_icon(args, [exe_name_t + ".png"])


def main(args):
    if args.version:
        print(Aut.__version__)
        sys.exit(0)
    if args.command == 'run':
        if args.test:
            test_run(args)
            sys.exit(0)
        run(args, check=args.without_check)
    if args.command == 'aut':
        if args.status:
            check_process(Aut.aut_pid_file, check_pause=False)
            sys.exit(0)
        if args.kill:
            kill_process(Aut.aut_pid_file)
            sys.exit(0)
        if args.analysis:
            Aut.print_analysis()
            sys.exit(0)
        run_aut(check=args.without_check)
    elif args.command == 'status':
        print("自动汇报".center(50, "-"))
        check_process(pid_file)
        print("应用使用时间统计".center(50, "-"))
        check_process(Aut.aut_pid_file, check_pause=False)
    elif args.command == 'kill':
        kill_process(pid_file)
    elif args.command == 'pause':
        pause_process()
    elif args.command == 'resume':
        resume_process()
    elif args.command == 'log':
        logcat(args.tail)
    elif args.command == 'getlimit':
        get_limit(args)
    elif args.command == 'setlimit':
        set_limit(args)
    elif args.command == 'getinfo':
        get_info(args)
    elif args.command == 'delinfo':
        del_info(args)
    else:
        print("这是一个命令行程序，添加 -h 查看帮助。")
        input("按Enter退出...")


if __name__ == "__main__":
    main(args_parser()[0])
    # for o in Aut.get_all_names():
    #     save_exe_icon(o, o.split('\\')[-1])
