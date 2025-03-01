import functools
import os
import queue
import subprocess
import sys
import tkinter as tk
import traceback
import webbrowser
from concurrent.futures import Future
from datetime import datetime, timedelta
from tkinter import messagebox

import ttkbootstrap as ttk
from PIL import ImageTk, Image
from ttkbootstrap import Window
from ttkbootstrap.constants import *

try:
    import Aut
    from report import (check_process, pid_file, is_process_running, read_pid, kill_process, resume_process,
                        pause_process,
                        Exclude_Process, icon_dir, save_exe_icon)
    from Aut import ToolTip
except Exception as e:
    messagebox.showerror('err', str(e))
    sys.exit(-1)

Press_key = set()


def catch_errors(func):
    @functools.wraps(func)
    def wrapper(*a, **k):
        try:
            return func(*a, **k)
        except Exception:
            error_message = traceback.format_exc()
            messagebox.showerror("错误", f"发生错误：\n{error_message}")

    return wrapper


def get_log_files():
    if not os.path.exists(Aut.log_dir):
        return []
    log_files = [f for f in os.listdir(Aut.log_dir) if f.endswith(".log")]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(Aut.log_dir, x)), reverse=True)
    return log_files


def stop_report():
    m = kill_process(pid_file)
    messagebox.showinfo("info", m)


def stop_aut():
    m = kill_process(Aut.aut_pid_file)
    messagebox.showinfo("info", m)


def open_folder(path, select=False):
    """
    打开文件所在目录，并定位到文件。
    :param path: 文件或目录的路径
    :param select: 是否定位到文件（仅在 Windows 上有效）
    """
    try:
        if os.name == 'nt':  # Windows
            if select:
                os.system(f'explorer /select,"{path}"')
            else:
                if os.path.isfile(path):
                    os.startfile(os.path.dirname(path))
                elif os.path.isdir(path):
                    os.startfile(path)
                else:
                    raise Exception("unknown path")
        elif os.name == 'posix':  # macOS 或 Linux
            if sys.platform == 'darwin':  # macOS
                subprocess.run(['open', path], check=True)
            else:  # Linux
                subprocess.run(['xdg-open', path], check=True)
        else:
            messagebox.showerror("错误", f"不支持的操作系统, {path=}")
    except Exception as e:
        messagebox.showerror("错误", f"无法打开路径: {path}\n错误信息: {e}")


def save_icon():
    for o in Aut.get_all_names():
        save_exe_icon(o, o.split('\\')[-1], a=48)


class mainWindows(ttk.Frame):
    theme_list = ['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'yeti', 'pulse', 'united', 'morph',
                  'journal', 'darkly', 'superhero', 'solar', 'cyborg', 'vapor', 'simplex', 'cerculean', ]

    def __init__(self, master: Window):
        self.app_frames = []
        self.download_progress = None
        self.download_text = None
        self.is_download = False
        self.update_info = None
        self.report_running = False
        self.aut_running = False
        self.cycle_time = 600
        self.app = master
        self.app.minsize(width=950, height=800)
        super().__init__(master, padding=5)
        # 重定向标准输出到队列
        self.output_queue = queue.Queue()
        sys.stdout = self.RedirectOutput(self.output_queue)
        # 定期更新输出框
        self.update_output_viewer()
        # sys.stderr = self.RedirectOutput(self.output_queue)# logger使用
        self.output_text = None
        self.key = None
        self.url = None
        self.pack(fill=BOTH, expand=True)
        self.notebook = ttk.Notebook(self, style="info")
        self.notebook.pack(fill=BOTH, expand=True)
        self.create_usage()
        self.create_process_checker()
        self.create_logs_viewer()
        self.create_setting()
        self.create_about()
        self.update_logs()
        self.cycle_time = 600

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

        # 每隔一段时间调用一次自己
        self.after(100, self.update_output_viewer)

    def clear_output_viewer(self):
        self.output_text.config(state=NORMAL)
        self.output_text.delete(1.0, END)
        self.output_text.config(state=DISABLED)

    class RedirectOutput:
        """重定向标准输出到队列"""

        def __init__(self, _queue):
            self.queue = _queue

        def write(self, message):
            self.queue.put(message)

        def flush(self):
            pass

    def create_process_checker(self):
        if os.path.exists("report.exe"):
            path = os.path.join(os.path.dirname(__file__), "report.exe")
        else:
            path = f"pythonw {os.path.join(os.path.dirname(__file__), 'report.py')}"
        row = ttk.Frame()
        row.pack(fill=X)
        self.notebook.add(row, text="进程管理", state="normal")
        lf = ttk.Labelframe(row, text="报告程序")
        lf.pack(fill="both", padx=10, pady=5)
        btn_frame = ttk.Frame(lf)
        btn_frame.pack(fill=BOTH, padx=10, pady=5)
        self.run_button = ttk.Button(btn_frame, text="运行", command=self.run_report, width=8)
        self.run_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.stop_button = ttk.Button(btn_frame, text="停止", command=stop_report, width=8)
        self.stop_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.pause_button = ttk.Button(btn_frame, text="暂停", command=pause_process, width=8)
        self.pause_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.resume_button = ttk.Button(btn_frame, text="恢复", command=resume_process, width=8)
        self.resume_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.startup1_var = tk.IntVar(value=Aut.check_startup_exists('seeme-report'))

        def on_toggle1():
            if self.startup1_var.get():
                Aut.set_startup('seeme-report', f'{path} run -c {str(self.cycle_time)} --without_check')
            else:
                Aut.delete_startup('seeme-report')

        self.startup1 = ttk.Checkbutton(btn_frame, text="开机启动", variable=self.startup1_var,
                                        command=on_toggle1, width=10)
        self.startup1.pack(side=LEFT, anchor=W, padx=20, pady=2)
        ToolTip(self.startup1, 'no',
                at_show_func=lambda label: label.config(text=f"启动项为: {Aut.get_startup('seeme-report')}"))
        self.tree = ttk.Treeview(lf, columns=("k", "v"), show="", height=6)
        self.tree.pack(fill="both", expand=True)
        self.tree.column("k", stretch=False)
        self.tree.column("v", stretch=True)

        lf2 = ttk.Labelframe(row, text="应用时间统计")
        lf2.pack(fill="both", padx=10, pady=5)
        btn2_frame = ttk.Frame(lf2)
        btn2_frame.pack(fill=BOTH, padx=10, pady=5)
        self.run2_button = ttk.Button(btn2_frame, text="运行", command=self.run_aut, width=8)
        self.run2_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.stop2_button = ttk.Button(btn2_frame, text="停止", command=stop_aut, width=8)
        self.stop2_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        # self.analysis_button = ttk.Button(btn2_frame, text="打印分析", command=Aut.print_analysis, width=8)
        # self.analysis_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.startup2_var = tk.IntVar(value=Aut.check_startup_exists('seeme-report-aut'))

        def on_toggle2():
            if self.startup2_var.get():
                Aut.set_startup('seeme-report-aut', f'{path} aut --without_check')
            else:
                Aut.delete_startup('seeme-report-aut')

        self.startup2 = ttk.Checkbutton(btn2_frame, text="开机启动", variable=self.startup2_var,
                                        command=on_toggle2, width=10)
        self.startup2.pack(side=LEFT, anchor=W, padx=20, pady=2)
        ToolTip(self.startup2, f"no",
                at_show_func=lambda label: label.config(text=f"启动项为: {Aut.get_startup('seeme-report-aut')}"))
        self.tree2 = ttk.Treeview(lf2, columns=("k", "v"), show="", height=5)
        self.tree2.pack(fill="both", expand=True)
        self.tree2.column("k", stretch=False)
        self.tree2.column("v", stretch=True)
        self.update_process_info_loop()

        self.cmd_frame = ttk.LabelFrame(row, text="运行命令行命令")
        self.cmd_frame.pack(fill=BOTH, padx=10, pady=5)
        self.cmd_entry = ttk.Entry(self.cmd_frame, width=50)
        self.cmd_entry.pack(side=LEFT, padx=10, pady=5, anchor=W)
        self.cmd_entry.insert(0, '--help')
        self.runcmd_button = ttk.Button(self.cmd_frame, text="运行", command=self.run_cmd, width=8)
        self.runcmd_button.pack(side=LEFT, anchor=W, padx=10, pady=5)
        self.clear_button = ttk.Button(self.cmd_frame, text="清空输出", command=self.clear_output_viewer, width=8)
        self.clear_button.pack(side=LEFT, anchor=W, padx=10, pady=5)

        self.output_frame = ttk.LabelFrame(row, text="输出")
        self.output_frame.pack(fill=BOTH, padx=10, pady=5)
        self.output_text = ttk.Text(self.output_frame, wrap=WORD)
        self.output_text.pack(fill=BOTH, expand=True, side=LEFT)
        scrollbar = ttk.Scrollbar(self.output_frame, command=self.output_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.output_text.config(yscrollcommand=scrollbar.set, state=DISABLED)  # 禁止用户编辑

    def run_report(self):
        if is_process_running(read_pid(pid_file)):
            messagebox.showerror("错误", f"已经在运行!")
            return
        if not self.key or not self.url:
            messagebox.showerror("错误", f"{self.key=},{self.url=}")
            return
        if os.path.exists(os.path.join(os.path.dirname(__file__), "report.exe ")):
            _args = ["report.exe", "run", "-c", str(self.cycle_time)]
        else:
            _args = ["python", "report.py", "run", "-c", str(self.cycle_time)]
        try:
            self.process = subprocess.Popen(_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            text=True, creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                            bufsize=1, encoding="utf-8")
            # 启动线程来读取子进程的输出
            print(f"running pid={self.process.pid}")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def run_aut(self):
        if is_process_running(read_pid(Aut.aut_pid_file)):
            messagebox.showinfo("info", f"已经在运行!")
            return
        if os.path.exists(os.path.join(os.path.dirname(__file__), "report.exe ")):
            _args = ["report.exe", "aut"]
        else:
            _args = ["python", "report.py", "aut"]
        try:
            self.process2 = subprocess.Popen(_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                             creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                             bufsize=1, encoding="utf-8")
            print(f"running pid={self.process2.pid}")
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def run_cmd(self):
        command_string = self.cmd_entry.get().strip()
        if command_string == '': return
        if command_string.startswith('run') or command_string.startswith('aut'):
            print('不能在这里运行阻塞程序')
            return
        cli = os.path.join(os.path.dirname(__file__), "report_cli.exe ")
        import shutil
        if shutil.which('python'):
            cli = f'python {os.path.join(os.path.dirname(__file__), "report.py ")}'
        elif not os.path.exists(cli):
            print('需要 report_cli.exe')
            return
        self.process3 = subprocess.Popen(cli + " " + command_string, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                         text=True, creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                         bufsize=1, encoding="utf-8")
        Aut.executor.submit(self.read_output, self.process3)
        self.cmd_entry.delete(0, END)

    def read_output(self, pc):
        try:
            for line in iter(pc.stdout.readline, ""):
                self.output_queue.put(line)
        finally:
            pc.stdout.close()
            pc.wait()

    def update_process_info_loop(self):
        try:
            self.update_process_info(pid_file, self.tree)
            self.update_process_info(Aut.aut_pid_file, self.tree2, check_pause=False)
            self.master.after(2000, self.update_process_info_loop)
        except Exception as e:
            messagebox.showerror("err", str(e))

    def update_process_info(self, pf, tr, check_pause=True):
        err, info = check_process(pf, pt=False, check_pause=check_pause)
        if err:
            tr.insert("", "end", values=("Error", f"{err}"))
            tr.insert("", "end", values=("Stop", f"stop update process info"))
            raise Exception(f'更新进程状态信息出错 {err}')
        tr.tag_configure("running", foreground="green")
        tr.tag_configure("stop", foreground="red")
        tr.tag_configure("paused", foreground="yellow")
        status = info.get("status", "N/A")
        if status == "running":
            if check_pause:
                self.report_running = True
            else:
                self.aut_running = True
        else:
            if check_pause:
                self.report_running = False
            else:
                self.aut_running = False
        for i in tr.get_children():
            tr.delete(i)
        tr.insert("", "end", values=("进程ID", info.get("pid", "N/A")))
        tr.insert("", "end", values=("状态", status), tags=(status,))
        tr.insert("", "end", values=("工作集内存", f"{info.get('memory', 0)} MB"))
        tr.insert("", "end", values=("创建时间", info.get("create_time", "N/A")))
        tr.insert("", "end", values=("命令行", info.get("cmdline", "N/A")))
        if check_pause:
            tr.insert("", "end", values=("暂停信息", info.get("paused", "N/A")))

    def create_logs_viewer(self):
        row = ttk.Frame()
        row.pack(fill=BOTH, expand=True)
        self.notebook.add(row, text="日志查看", state="normal")
        log_selector_frame = ttk.Frame(row)
        log_selector_frame.pack(fill=BOTH, padx=10, pady=5)
        log_files = get_log_files()
        if not log_files:
            log_files = ["No logs found"]
        self.log_file_var = ttk.StringVar(value=log_files[0])
        self.log_file_var.trace("w", self.on_log_file_changed)  # 绑定事件
        log_combo = ttk.Combobox(log_selector_frame, textvariable=self.log_file_var, values=log_files, state="readonly")
        log_combo.pack(side=LEFT, padx=10)
        refresh_btn = ttk.Button(log_selector_frame, text="Refresh Logs", command=self.update_logs)
        refresh_btn.pack(side=LEFT, padx=10)
        log_frame = ttk.Frame(row)
        log_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.log_text = ttk.Text(log_frame, wrap=WORD)
        self.log_text.pack(fill=BOTH, expand=True, side=LEFT)
        h_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        h_scrollbar.pack(side=RIGHT, fill=Y)
        self.log_text.configure(yscrollcommand=h_scrollbar.set, state=DISABLED)

    def on_log_file_changed(self, *args):
        self.update_logs()

    def update_logs(self):
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("critical", foreground="purple")
        selected_file = self.log_file_var.get()
        if not selected_file:
            return
        log_path = os.path.join(Aut.log_dir, selected_file)
        if not os.path.exists(log_path):
            return
        try:
            with open(log_path, 'r', encoding='utf-8') as file:
                logs = file.readlines()
        except Exception as e:
            logs = [f"Error reading log file: {e}"]
        self.log_text.configure(state=NORMAL)  # 允许编辑
        self.log_text.delete("1.0", "end")
        for log in logs:
            if "[ERROR]" in log:
                tag = "error"
            elif "[WARNING]" in log:
                tag = "warning"
            elif "[CRITICAL]" in log:
                tag = "critical"
            else:
                tag = "info"
            self.log_text.insert("end", log, tag)
        self.log_text.configure(state=DISABLED)  # 禁用编辑

    def create_setting(self):
        # 创建设置页面
        row = ttk.Frame()
        row.pack(fill="both", expand=True)
        self.notebook.add(row, text="设置", state="normal")
        ttk.Label(row, text="主题:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.theme_var = ttk.StringVar(value="")
        self.theme_var.trace("w", self.on_theme_changed)  # 绑定事件
        theme_combo = ttk.Combobox(row, textvariable=self.theme_var, values=mainWindows.theme_list, state="readonly")
        theme_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        # 服务器地址
        ttk.Label(row, text="服务器地址:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(row, width=50, validatecommand=self.validate_url, validate="focusout")
        self.url_entry.grid(row=1, column=1, padx=5, pady=5)

        # 密钥
        ttk.Label(row, text="服务器密钥:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.key_entry = ttk.Entry(row, width=50, show="*", name="a")
        self.key_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(row, text="报告周期(s)>300:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cycle_time_entry = ttk.Entry(row, validatecommand=self.validate_cycle_time, validate="focusout")
        self.cycle_time_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        # 排除进程
        ttk.Label(row, text="报告程序排除的进程（,分割添加多个）:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.exclude_list = tk.Listbox(row, width=50, height=10, selectmode="extended")
        self.exclude_list.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.add_entry = ttk.Entry(row)
        self.add_entry.grid(row=6, column=0, padx=5, pady=5, sticky="ew")
        self.add_button = ttk.Button(row, text="添加", command=self.add_exclude_process)
        self.add_button.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.remove_button = ttk.Button(row, text="删除选中", command=self.remove_exclude_process,
                                        bootstyle="danger-outline")
        self.remove_button.grid(row=6, column=1, padx=5, pady=5, sticky="e")

        def getsize(f):
            try:
                kb = os.path.getsize(f) // 1024
                if kb < 1024:
                    return f"{kb} KB"
                else:
                    return f"{kb / 1024} MB"
            except Exception as e:
                return str(e)

        def open_folder_and_select_file(event):
            open_folder(path=Aut.sqlite_file, select=True)

        ttk.Label(row, text="数据库文件：").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        label3 = ttk.Label(row, text=f"{Aut.sqlite_file.split("\\")[-1]} {getsize(Aut.sqlite_file)}",
                           foreground="#2AADFF", cursor="hand2")
        label3.grid(row=7, column=1, columnspan=2, padx=5, pady=5, sticky="we")
        label3.bind("<Button-1>", open_folder_and_select_file)

        ttk.Label(row, text="更新源:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.update_source_var = ttk.StringVar(value="gitee")
        self.update_source_var.trace("w", self.on_update_source_changed)
        update_sourceComb = ttk.Combobox(row, textvariable=self.update_source_var,
                                         values=["gitee", "github"], state="readonly")
        update_sourceComb.grid(row=8, column=1, padx=5, pady=5, sticky="ew")
        ttk.Label(row, text="自动检查更新频率:").grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.check_frequency_var = ttk.StringVar(value="每天")
        self.check_frequency_var.trace("w", self.on_check_frequency_changed)
        (ttk.Combobox(row, textvariable=self.check_frequency_var, values=["每天", "每周", "从不"], state="readonly")
         .grid(row=9, column=1, padx=5, pady=5, sticky="ew"))

        button1 = ttk.Button(row, text="打开程序文件夹", command=lambda: open_folder(path=os.path.dirname(__file__)))
        button1.grid(row=10, column=0, pady=15, padx=5, sticky="w")
        button2 = ttk.Button(row, text="打开数据文件夹", command=lambda: open_folder(path=Aut.APPDATA))
        button2.grid(row=10, column=0, pady=15, padx=5, sticky="e")
        button3 = ttk.Button(row, text="测试更新服务连接", command=Aut.test_conn)
        button3.grid(row=10, column=1, pady=15, padx=5, sticky="w")

        reload_button = ttk.Button(row, text="重载配置", command=self.load_settings, bootstyle="warning-outline")
        reload_button.grid(row=11, column=0, pady=15, padx=5, sticky="w")
        # 保存按钮
        save_button = ttk.Button(row, text="保存", command=self.save_settings, bootstyle="success-outline")
        save_button.grid(row=11, column=1, pady=15, padx=5, sticky="e")
        # 加载设置
        self.load_settings()

    def validate_url(self):
        if self.url_entry.get().startswith("http://") or self.url_entry.get().startswith("https://"):
            return True
        else:
            messagebox.showerror("验证失败", "服务器地址必须以 'http://' 或 'https://' 开头！")
            return False

    def validate_cycle_time(self):
        try:
            cycle_time = int(self.cycle_time_entry.get())
            if 300 < cycle_time < 86400:
                return True
            else:
                messagebox.showerror("验证失败", "输入值必须大于5分钟（300秒）且小于1天（86400秒）")
                self.cycle_time_entry.delete(0, END)
                self.cycle_time_entry.insert(0, "600")
                return False
        except ValueError:
            messagebox.showerror("验证失败", "请输入有效的整数！")
            self.cycle_time_entry.delete(0, END)
            self.cycle_time_entry.insert(0, "600")
            return False

    def on_theme_changed(self, *args):
        selected_theme = self.theme_var.get()
        self.app.style.theme_use(themename=selected_theme)
        print(f"主题已切换为: {selected_theme}")

    def on_update_source_changed(self, *args):
        self.selected_source = self.update_source_var.get()
        print(f"更新源已切换为: {self.selected_source}")

    def on_check_frequency_changed(self, *args):
        self.check_frequency = self.check_frequency_var.get()
        print(f"检查更新频率已切换为: {self.check_frequency}")

    def add_exclude_process(self):
        inp = self.add_entry.get().split(",")
        for i in inp:
            i = i.strip()
            if i:
                self.exclude_list.insert(END, i)
            else:
                messagebox.showerror("错误", "不能添加空值")
                break
        self.add_entry.delete(0, END)

    def remove_exclude_process(self):
        # 删除选中的排除进程
        selected = self.exclude_list.curselection()
        if selected:
            for s in reversed(selected):
                self.exclude_list.delete(s)
        else:
            messagebox.showerror("错误", "列表中没有选中的项")

    @catch_errors
    def save_settings(self):
        if not (self.validate_url() and self.validate_cycle_time()):
            return
        self.key = self.key_entry.get()
        self.url = self.url_entry.get()
        self.cycle_time = self.cycle_time_entry.get()
        Aut.cfg.set("DEFAULT", "key", self.key)
        Aut.cfg.set("DEFAULT", "url", self.url)
        Aut.cfg.set("DEFAULT", "theme", self.theme_var.get())
        Aut.cfg.set("DEFAULT", "exclude_process", ",".join(self.exclude_list.get(0, END)))
        self.notebook.update_idletasks()
        Aut.cfg.set("DEFAULT", "height", str(self.notebook.winfo_height()))
        Aut.cfg.set("DEFAULT", "width", str(self.notebook.winfo_width()))
        Aut.cfg.set("DEFAULT", "cycle_time", str(self.cycle_time))
        Aut.cfg.set("DEFAULT", "update_source", str(self.selected_source))
        Aut.cfg.set("DEFAULT", "check_frequency", str(self.check_frequency))
        e, m = Aut.setting_config(Aut.cfg)
        if e:
            messagebox.showinfo("info", f"{m}")
        else:
            messagebox.showerror("错误", f"{m}")

    @catch_errors
    def load_settings(self):
        self.theme_var.set(Aut.cfg.get("DEFAULT", "theme", fallback="cyborg"))
        self.update_source_var.set(Aut.cfg.get("DEFAULT", "update_source", fallback="gitee"))
        self.check_frequency_var.set(Aut.cfg.get("DEFAULT", "check_frequency", fallback="每天"))
        height = int(Aut.cfg.get("DEFAULT", "height", fallback=800))
        width = int(Aut.cfg.get("DEFAULT", "width", fallback=900))
        self.cycle_time = int(Aut.cfg.get("DEFAULT", "cycle_time", fallback=600))
        self.key = Aut.cfg.get("DEFAULT", "key", fallback="")
        self.url = Aut.cfg.get("DEFAULT", "url", fallback="")
        self.notebook.configure(height=height, width=width)
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, self.key)
        self.url_entry.delete(0, END)
        self.url_entry.insert(0, self.url)
        self.cycle_time_entry.delete(0, END)
        self.cycle_time_entry.insert(0, str(self.cycle_time))
        self.exclude_list.delete(0, END)
        for process in Exclude_Process:
            self.exclude_list.insert("end", process)
        self.after(1000, self.auto_check)

    def auto_check(self):
        # 检查更新
        last_update_time = Aut.cfg.get("DEFAULT", "last_update_time", fallback="2000-01-01 10:01:01")
        last_update_time_o = datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        check_frequency = self.check_frequency_var.get()
        if check_frequency == "每天":
            t_delta = timedelta(days=1)
        elif check_frequency == "每周":
            t_delta = timedelta(weeks=1)
        elif check_frequency == "从不":
            t_delta = timedelta(days=365 * 100)  # 相当于 "从不"
        else:
            self.check_frequency_var.set("每周")
            t_delta = timedelta(weeks=1)
        if now - last_update_time_o >= t_delta:
            print(f"需要更新  上传更新时间:{last_update_time}")
            Aut.get_update_info(self.update_source_var.get(), self)
        else:
            print(f"不需要更新  上次更新时间: {last_update_time}")

    def create_usage(self):
        row = ttk.Frame()
        row.pack(fill="both", expand=True)
        self.notebook.add(row, text="应用使用统计", state="normal")
        usage_ctrl_frame = ttk.Frame(row)
        usage_ctrl_frame.pack(fill=BOTH, padx=10, pady=5)
        refresh_button = ttk.Button(usage_ctrl_frame, text="刷新", command=self.load_usage_data)
        refresh_button.pack(side="left", padx=5, pady=5)

        save_icon_button = ttk.Button(usage_ctrl_frame, text="save icon", command=save_icon)
        save_icon_button.pack(side="left", padx=5, pady=5)
        self.canvas_at = ttk.Label(usage_ctrl_frame)
        self.canvas_at.pack(side="left", padx=5)
        self.canvas = tk.Canvas(row)
        scrollbar = ttk.Scrollbar(row, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            if event.num == 5 or event.delta < 0:  # 向下滚动
                self.canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta > 0:  # 向上滚动
                self.canvas.yview_scroll(-1, "units")

        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.canvas.bind_all("<Button-4>", on_mousewheel)
        self.canvas.bind_all("<Button-5>", on_mousewheel)
        self.load_usage_data()

    def load_usage_data(self):
        f: Future = Aut.get_total_duration_for_all()
        self.canvas_at.config(text=f"加载中")

        def get_show(future):
            try:
                for frame in self.app_frames:
                    frame.destroy()
                self.app_frames.clear()
                usage_data = future.result()
                max_duration = max(row["total_duration"] for row in usage_data) if usage_data else 1
                for app in usage_data:
                    self.create_app_frame(app, max_duration)
                self.canvas_at.config(text=f"更新于 {datetime.now().strftime("%H:%M:%S")}")
            except Exception as e:
                print(e)
                self.canvas_at.config(text=f"Error:{str(e)}")

        f.add_done_callback(get_show)

    def create_app_frame(self, app, max_duration=1):
        app_name = app["name"].split('\\')[-1]
        total_duration = app["total_duration"]
        app_frame = ttk.Frame(self.scrollable_frame)
        app_frame.pack(fill="x", padx=5, pady=5)
        self.app_frames.append(app_frame)
        icon_path = os.path.join(icon_dir, f"{app_name}.png")
        if os.path.exists(icon_path):
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((32, 32), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = ttk.Label(app_frame, image=icon_photo, cursor='hand2')
            icon_label.image = icon_photo
        else:
            icon_label = ttk.Label(app_frame, text="", width=3, cursor='hand2')

        def delete_app(event):
            confirm = messagebox.askyesno("确认删除", f"确定要删除应用 '{app_name}' 的所有记录吗？")
            if confirm:
                Aut.delete_app_by_name(app["name"])
                messagebox.showinfo('info', f"已删除所有名为 '{app_name}' 的应用记录。")
                # self.load_usage_data()
            else:
                messagebox.showinfo('info', f"取消删除应用 '{app_name}' 的记录。")

        icon_label.bind('<Button-3>', lambda event: delete_app(event))
        icon_label.bind('<Button-1>', lambda event: open_folder(icon_path, select=True))
        icon_label.pack(side="left", padx=5)
        ToolTip(icon_label, f'{app_name}\n左键点击打开icon所在位置\n右键点击删除该应用的记录', delay=100)
        name_label = ttk.Label(app_frame, text=app_name, width=30, anchor="w", cursor="hand2")
        name_label.pack(side="left", padx=5)
        name_label.bind("<Button-1>", lambda event: open_folder(app["name"], select=True))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))  # 更新滚动区域。
        show_text = f"打开目录: \n{os.path.dirname(app["name"])}"
        after_id = ""

        def at_show(lab):
            f: Future = Aut.get_hourly_duration_for_name(app['name'])
            data = None

            def get_show(future):
                nonlocal after_id, data
                if 'Control_L' in Press_key:
                    try:
                        if not data:
                            print(f"query {os.path.basename(app['name'])} hourly duration")
                            data = future.result()
                        lab.winfo_exists() and lab.config(text=f"{show_text}\n{data}")
                    except Exception as e:
                        print(e)
                        lab.winfo_exists() and lab.config(text=f"{show_text}\n查询错误: {e}")
                else:
                    lab.winfo_exists() and lab.config(text=f"{show_text}\n按住ctrl显示每小时的信息")

                after_id = self.scrollable_frame.after(100, lambda: get_show(f))

            f.add_done_callback(get_show)

        def stop_after():
            if after_id:
                self.scrollable_frame.after_cancel(after_id)

        ToolTip(name_label, show_text, delay=100, at_show_func=at_show, at_leave=stop_after)
        progress = ttk.Progressbar(app_frame, orient="horizontal", length=200, mode="determinate")
        progress["value"] = (total_duration / max_duration) * 100
        progress.pack(side="left", padx=5)
        duration_label = ttk.Label(app_frame, text=f"{Aut.seconds2hms(total_duration)}", width=10, anchor="e")
        duration_label.pack(side="left", padx=5)

    def show_and_download(self, event):
        if not self.update_info or Aut.__version__ >= self.update_info["version"]:
            messagebox.showinfo("info", "无需下载")
            return
        if self.is_download:
            messagebox.showinfo("info", "进行中")
            return
        if not self.update_info:
            return
        zip_name, zip_url, sum_name, sum_url = None, None, None, None
        self.is_download = True
        for asset in self.update_info["assets"]:  # 暂时这样
            if asset["name"].endswith(f".zip") and "dist" in asset["name"]:
                zip_name = asset["name"]
                zip_url = asset["url"]
        for asset in self.update_info["assets"]:
            if asset["name"].endswith(".sha256.txt") and "dist" in asset["name"]:
                sum_name = asset["name"]
                sum_url = asset["url"]
        print(f"{zip_name=}\n {sum_name=}")
        if not self.download_text:
            self.download_text = ttk.Label(self.about_row, text="开始下载更新文件...")
            self.download_text.grid(row=3, column=0, columnspan=10, padx=5, pady=5, sticky="w")

        else:
            self.download_text.config(text="")
        if not self.download_progress:
            self.download_progress = ttk.Progressbar(self.about_row,
                                                     orient="horizontal", length=400, mode="determinate")
            self.download_progress.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # step 3
        def do_check_file():
            zip_file = os.path.join(Aut.temp_dir, zip_name)
            sum_file = os.path.join(Aut.temp_dir, sum_name)
            Aut.check_file_integrity(str(zip_file), sum_file, s=self)

        # step 2
        def download_sum():
            Aut.download_file(sum_name, sum_url, Aut.temp_dir, s=self, do_next=do_check_file)

        # step 1
        Aut.download_file(zip_name, zip_url, Aut.temp_dir, s=self, do_next=download_sum)

    def create_about(self):
        def open_url(event):
            webbrowser.open("https://github.com/2412322029/seeme")

        self.about_row = ttk.Frame()
        self.about_row.pack(fill="both", expand=True)
        self.notebook.add(self.about_row, text="关于", state="normal")
        ttk.Label(self.about_row, text="Home page:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        label2 = ttk.Label(self.about_row, text="https://github.com/2412322029/seeme", foreground="#2AADFF",
                           cursor="hand2")
        label2.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        label2.bind("<Button-1>", open_url)
        ttk.Label(self.about_row, text=f"version:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.about_row, text=f"{Aut.__version__}").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(self.about_row, text=f"build time:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(self.about_row, text=f"{Aut.__buildAt__}").grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.info_label = ttk.Label(self.about_row, text="当前是最新版", foreground="#2AADFF")
        self.info_label.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.info_label.bind("<Button-1>", self.show_and_download)

        def get_update(event):
            Aut.get_update_info(self.selected_source, self)

        label3 = ttk.Label(self.about_row, text="检查更新", foreground="#2AADFF", cursor="hand2")
        label3.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        label3.bind("<Button-1>", get_update)

        self.about_row.columnconfigure(0, weight=0)
        self.about_row.columnconfigure(1, weight=0)
        self.about_row.columnconfigure(2, weight=1)


def main():
    try:
        app = ttk.Window("Report", "cyborg")
        app.geometry("950x1000")
        app.iconbitmap(os.path.join(os.path.dirname(__file__), "icon.ico"))
        mainWindows(app)
        def on_key_press(event):
            Press_key.add(event.keysym)

        def on_key_release(event):
            Press_key.clear()

        app.bind("<KeyPress>", on_key_press)
        app.bind("<KeyRelease>", on_key_release)
        app.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))


if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        main()
    else:
        from report import main, args_parser

        args = args_parser()[0]
        main(args)
