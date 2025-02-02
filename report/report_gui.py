import os
import queue
import subprocess
import sys
import threading
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from Aut.logger import log_dir
from report import (check_process, pid_file, pause_file, timeAgo,
                    is_process_running, read_pid, kill_process, resume_process, pause_process)


def get_log_files():
    if not os.path.exists(log_dir):
        return []
    log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True)
    return log_files


class mainWindows(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=5)
        self.key = None
        self.url = None
        self.pack(fill=X, expand=0)
        self.notebook = ttk.Notebook(self, style="info")
        self.notebook.pack(fill=BOTH)
        self.notebook.configure(height=700, width=1000)
        self.create_process_checker()
        self.create_logs_viewer()
        self.create_setting()
        self.update_logs()
        self.cycle_time = 600
        # 重定向标准输出到队列
        self.output_queue = queue.Queue()
        sys.stdout = self.RedirectOutput(self.output_queue)
        sys.stderr = self.RedirectOutput(self.output_queue)
        # 定期更新输出框
        self.update_output_viewer()

    def update_output_viewer(self):
        # 定期从队列中获取输出并更新文本框
        try:
            while not self.output_queue.empty():
                output = self.output_queue.get_nowait()
                self.output_text.config(state=NORMAL)
                self.output_text.insert(END, output)
                self.output_text.config(state=DISABLED)
                self.output_text.see(END)  # 自动滚动到最底部
        except queue.Empty:
            pass

        # 每隔一段时间（例如100毫秒）调用一次自己
        self.after(100, self.update_output_viewer)

    class RedirectOutput:
        """重定向标准输出到队列"""

        def __init__(self, queue):
            self.queue = queue

        def write(self, message):
            self.queue.put(message)

        def flush(self):
            pass

    def create_process_checker(self):
        row = ttk.Frame()
        row.pack(fill=X)
        self.notebook.add(row, text="Process Checker", state="normal")
        btn_frame = ttk.Frame(row)
        btn_frame.pack(fill=BOTH, padx=10, pady=5)
        info_frame = ttk.Frame(row)
        info_frame.pack(fill=X, pady=20)
        self.run_button = ttk.Button(btn_frame, text="Run", command=self.run_report, width=10)
        self.run_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.stop_button = ttk.Button(btn_frame, text="Stop", command=self.stop_report, width=10)
        self.stop_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.pause_button = ttk.Button(btn_frame, text="Pause", command=pause_process, width=10)
        self.pause_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.resume_button = ttk.Button(btn_frame, text="Resume", command=resume_process, width=10)
        self.resume_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.pid_label = ttk.Label(info_frame, text="PID: ", font=("Helvetica", 12))
        self.pid_label.pack(anchor=W, padx=20, pady=2)
        self.status_label = ttk.Label(info_frame, text="Status: ", font=("Helvetica", 12))
        self.status_label.pack(anchor=W, padx=20, pady=2)
        self.memory_label = ttk.Label(info_frame, text="Memory Usage: ", font=("Helvetica", 12))
        self.memory_label.pack(anchor=W, padx=20, pady=2)
        self.start_time_label = ttk.Label(info_frame, text="Start Time: ", font=("Helvetica", 12))
        self.start_time_label.pack(anchor=W, padx=20, pady=2)
        self.cmd_line_label = ttk.Label(info_frame, text="Command Line: ", font=("Helvetica", 12))
        self.cmd_line_label.pack(anchor=W, padx=20, pady=2)
        self.pause_label = ttk.Label(info_frame, text="Paused at: ", font=("Helvetica", 12), foreground="red")
        self.pause_label.pack(anchor=W, padx=20, pady=2)
        self.update_process_info_loop()

        # 创建一个文本框用于显示输出
        self.output_frame = ttk.Frame(row)
        self.output_frame.pack(fill=BOTH, padx=10, pady=5)
        self.output_text = ttk.Text(self.output_frame, wrap=WORD, height=20, width=100)
        self.output_text.pack(fill=BOTH, expand=True)
        self.output_text.config(state=DISABLED)  # 禁止用户编辑

    def run_report(self):
        if is_process_running(read_pid(pid_file)):
            messagebox.showerror("错误", f"已经在运行!")
            return
        if not self.key or not self.url:
            messagebox.showerror("错误", f"{self.key=},{self.url=}")
            return
        try:
            self.process = subprocess.Popen(["report.exe", "run",
                                             "-c", "600", "-k", self.key, "-u", self.url],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT,
                                            text=True,
                                            creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                            bufsize=1)
            # 启动线程来读取子进程的输出
            self.output_thread = threading.Thread(target=self.read_output)
            self.output_thread.daemon = True
            self.output_thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def read_output(self):
        # 从子进程中读取输出并放入队列
        try:
            for line in iter(self.process.stdout.readline, ""):
                self.output_queue.put(line)
        finally:
            self.process.stdout.close()
            self.process.wait()

    def stop_report(self):
        m = kill_process(pid_file)
        messagebox.showerror("错误", m)

    def update_process_info_loop(self):
        self.update_process_info()
        self.master.after(2000, self.update_process_info_loop)

    def update_process_info(self):
        err, info = check_process(pid_file, pt=False)
        if err:
            self.pid_label.config(text=f"PID: Error - {err}")
            return
        self.pid_label.config(text=f"PID: {info.get('pid', 'N/A')}")
        if info.get('status') == "running":
            self.status_label.config(text=f"Status: {info.get('status', 'N/A')}", foreground="green")
        else:
            self.status_label.config(text=f"Status: {info.get('status', 'N/A')}", foreground="red")
        self.memory_label.config(text=f"Memory Usage: {info.get('memory', 0)} MB")
        self.start_time_label.config(text=f"Start Time: {info.get('create_time', 'N/A')}")
        self.cmd_line_label.config(text=f"Command Line: {info.get('cmdline', 'N/A')}")
        if os.path.exists(pause_file):
            getctime = datetime.fromtimestamp(os.path.getctime(pause_file))
            self.pause_label.config(text=f"Paused at: {getctime} ({timeAgo(getctime).strip()} ago)")
        else:
            self.pause_label.config(text="Paused at: N/A")

    def create_logs_viewer(self):
        row = ttk.Frame()
        row.pack(fill=BOTH, expand=True)
        self.notebook.add(row, text="Logs Viewer", state="normal")
        log_selector_frame = ttk.Frame(row)
        log_selector_frame.pack(fill=BOTH, padx=10, pady=5)
        log_files = get_log_files()
        if not log_files:
            log_files = ["No logs found"]
        self.log_file_var = ttk.StringVar(value=log_files[0])
        log_combo = ttk.Combobox(log_selector_frame, textvariable=self.log_file_var, values=log_files, state="readonly")
        log_combo.pack(side=LEFT, padx=10)
        refresh_btn = ttk.Button(log_selector_frame, text="Refresh Logs", command=self.update_logs)
        refresh_btn.pack(side=LEFT, padx=10)
        log_frame = ttk.Frame(row)
        log_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.log_text = ttk.ScrolledText(log_frame, wrap="none", width=100, height=20)
        self.log_text.pack(side=LEFT, fill=BOTH, expand=True)
        self.log_text.configure(state="disabled")  # 禁用编辑
        h_scrollbar = ttk.Scrollbar(self.log_text, orient="horizontal", command=self.log_text.xview)
        h_scrollbar.pack(side=BOTTOM, fill=X)
        self.log_text.configure(xscrollcommand=h_scrollbar.set)

    def update_logs(self):
        selected_file = self.log_file_var.get()
        if not selected_file:
            return
        log_path = os.path.join(log_dir, selected_file)
        if not os.path.exists(log_path):
            return
        try:
            with open(log_path, 'r', encoding='utf-8') as file:
                logs = file.readlines()
        except Exception as e:
            logs = [f"Error reading log file: {e}"]
        self.log_text.configure(state="normal")  # 允许编辑
        self.log_text.delete("1.0", "end")
        for log in logs:
            self.log_text.insert("end", log)
        self.log_text.configure(state="disabled")  # 禁用编辑

    def create_setting(self):
        row = ttk.Frame()
        row.pack(fill=BOTH, expand=True)
        self.notebook.add(row, text="Setting", state="normal")

        # 创建输入框
        ttk.Label(row, text="Key:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.key_entry = ttk.Entry(row, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(row, text="URL:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.url_entry = ttk.Entry(row, width=30)
        self.url_entry.grid(row=1, column=1, padx=5, pady=5)

        # 创建保存按钮
        save_button = ttk.Button(row, text="Save", command=self.save_settings)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 加载设置
        self.load_settings()

    def save_settings(self):
        self.key = self.key_entry.get()
        self.url = self.url_entry.get()
        with open("settings.txt", "w", encoding="utf8") as f:
            f.write(f"key={self.key}\n")
            f.write(f"url={self.url}\n")
        print("Settings saved.")

    def load_settings(self):
        if os.path.exists("settings.txt"):
            with open("settings.txt", "r", encoding="utf8") as f:
                for line in f:
                    if line.startswith("key="):
                        self.key = line.strip().split("=")[1]
                        self.key_entry.insert(0, self.key)
                    elif line.startswith("url="):
                        self.url = line.strip().split("=")[1]
                        self.url_entry.insert(0, self.url)
            print("Settings loaded.")


if __name__ == '__main__':
    app = ttk.Window("Report", "journal")
    mainWindows(app)
    app.mainloop()
