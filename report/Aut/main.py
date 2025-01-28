import os
import signal
import sqlite3
import time
from datetime import datetime

import psutil
import win32gui
import win32process

from .logger import logger

script_dir = os.path.dirname(os.path.abspath(__file__))
sqlite_file = os.path.join(script_dir, "app_usage.db")
aut_pid_file = os.path.join(script_dir, 'aut.pid')  # 保存进程pid
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS app_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hourly_start_time TEXT NOT NULL,  -- 每小时的开始时间
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    duration REAL NOT NULL
)
''')
conn.commit()

# 用于存储每个应用的累计使用时间
app_usage_time = {}
# 上一个活动窗口的进程路径
last_active_process_path = None
# 上一个活动窗口的开始时间
last_start_time = None


def get_active_window_process_path():
    """获取当前活动窗口对应的进程路径"""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        # title = win32gui.GetWindowText(hwnd)
        # print(title)
        try:
            process = psutil.Process(pid)
            exe_path = process.exe()  # 获取进程的可执行文件路径
            if not exe_path.endswith("explorer.exe"):
                return exe_path
        except psutil.NoSuchProcess:
            return None
    return None


def update_app_usage_time():
    """更新应用使用时间"""
    global last_active_process_path, last_start_time
    current_process_path = get_active_window_process_path()
    if current_process_path != last_active_process_path:
        # 如果窗口切换了
        if last_active_process_path:
            # 计算上一个应用的使用时间
            end_time = datetime.now()
            duration = (end_time - last_start_time).seconds
            # 获取每小时的开始时间
            hourly_start_time = last_start_time.replace(minute=0, second=0, microsecond=0)
            # 检查是否已经存在同一小时内相同应用的记录
            cursor.execute('''
            SELECT id, duration FROM app_usage
            WHERE name = ? AND hourly_start_time = ?
            ''', (last_active_process_path, hourly_start_time.strftime('%Y-%m-%d %H:%M:%S')))
            result = cursor.fetchone()
            if result:
                # 如果存在，更新持续时间
                existing_id, existing_duration = result
                new_duration = existing_duration + duration
                cursor.execute('''
                UPDATE app_usage
                SET duration = ?
                WHERE id = ?
                ''', (new_duration, existing_id))
            else:
                # 如果不存在，插入新记录
                cursor.execute('''
                INSERT INTO app_usage (name, hourly_start_time, start_time, end_time, duration)
                VALUES (?, ?, ?, ?, ?)
                ''', (last_active_process_path, hourly_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                      last_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                      end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
            conn.commit()
        # 更新为当前应用
        last_active_process_path = current_process_path
        last_start_time = datetime.now()


def save_data():
    """保存当前应用的使用时间"""
    global last_active_process_path, last_start_time
    if last_active_process_path:
        # 计算当前应用的使用时间
        end_time = datetime.now()
        duration = (end_time - last_start_time).seconds
        # 获取每小时的开始时间
        hourly_start_time = last_start_time.replace(minute=0, second=0, microsecond=0)
        # 检查是否已经存在同一小时内相同应用的记录
        cursor.execute('''
        SELECT id, duration FROM app_usage
        WHERE name = ? AND hourly_start_time = ?
        ''', (last_active_process_path, hourly_start_time.strftime('%Y-%m-%d %H:%M:%S')))
        result = cursor.fetchone()
        if result:
            # 如果存在，更新持续时间
            existing_id, existing_duration = result
            new_duration = existing_duration + duration
            cursor.execute('''
            UPDATE app_usage
            SET duration = ?
            WHERE id = ?
            ''', (new_duration, existing_id))
        else:
            # 如果不存在，插入新记录
            cursor.execute('''
            INSERT INTO app_usage (name, hourly_start_time, start_time, end_time, duration)
            VALUES (?, ?, ?, ?, ?)
            ''', (last_active_process_path, hourly_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                  last_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                  end_time.strftime('%Y-%m-%d %H:%M:%S'), duration))
        conn.commit()


def on_exit(signum, frame):
    """处理程序退出"""
    save_data()
    cursor.close()
    conn.close()
    print("数据已保存，程序退出。")
    exit(0)


def run(upload_callback=None):
    print("开始监听窗口切换...")
    # 保存进程ID到文件
    with open(aut_pid_file, 'w') as f:
        f.write(str(os.getpid()))
    try:
        # 注册信号处理函数
        signal.signal(signal.SIGTERM, on_exit)
        signal.signal(signal.SIGINT, on_exit)
        last_upload_time = time.time()  # 记录上次上传时间
        while True:
            update_app_usage_time()
            time.sleep(1)
            # 检查是否需要上传数据
            current_time = time.time()
            if upload_callback and (current_time - last_upload_time) >= 3600:  # 一小时上传一次
                upload_callback(sqlite_file)
                last_upload_time = current_time  # 更新上次上传时间
    except Exception as e:
        logger.fatal(f"发生异常: {e}")
        on_exit(None, None)
