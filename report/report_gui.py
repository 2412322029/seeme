import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from tkinter import messagebox

import ttkbootstrap as ttk
from PIL import ImageTk, Image
from ttkbootstrap import Window
from ttkbootstrap.constants import *

from Aut.config import cfg, setting_config
from Aut.logger import log_dir
from Aut.usage_analysis import get_total_duration_for_all, seconds2hms
from report import (check_process, pid_file, is_process_running, read_pid, kill_process, resume_process, pause_process,
                    Aut, Exclude_Process, icon_dir, save_exe_icon)


def get_log_files():
    if not os.path.exists(log_dir):
        return []
    log_files = [f for f in os.listdir(log_dir) if f.endswith(".log")]
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True)
    return log_files


def stop_report():
    m = kill_process(pid_file)
    messagebox.showinfo("info", m)


def stop_aut():
    m = kill_process(Aut.aut_pid_file)
    messagebox.showinfo("info", m)


class mainWindows(ttk.Frame):
    theme_list = ['cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'yeti', 'pulse', 'united', 'morph',
                  'journal', 'darkly', 'superhero', 'solar', 'cyborg', 'vapor', 'simplex', 'cerculean', ]

    def __init__(self, master: Window):
        self.remove_button = None
        self.add_button = None
        self.add_entry = None
        self.exclude_list = None
        self.key_entry = None
        self.url_entry = None
        self.theme_var = None
        self.log_text = None
        self.log_file_var = None
        self.output_thread2 = None
        self.process2 = None
        self.output_thread = None
        self.process = None
        self.output_frame = None
        self.analysis_button = None
        self.tree2 = None
        self.stop2_button = None
        self.clear_button = None
        self.run2_button = None
        self.tree = None
        self.resume_button = None
        self.pause_button = None
        self.stop_button = None
        self.run_button = None
        self.report_running = False
        self.aut_running = False
        self.app = master
        self.app.minsize(width=950, height=800)
        super().__init__(master, padding=5)
        self.output_text = None
        self.key = None
        self.url = None
        self.pack(fill=BOTH, expand=True)
        self.notebook = ttk.Notebook(self, style="info", height=800, width=900)
        self.notebook.pack(fill=BOTH)

        self.create_usage()
        self.create_process_checker()
        self.create_logs_viewer()
        self.create_setting()
        self.create_about()

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
        row = ttk.Frame()
        row.pack(fill=X)
        self.notebook.add(row, text="进程管理", state="normal")
        lf = ttk.Labelframe(row, text="报告程序")
        lf.pack(fill="both", padx=10, pady=5)
        btn_frame = ttk.Frame(lf)
        btn_frame.pack(fill=BOTH, padx=10, pady=5)
        self.run_button = ttk.Button(btn_frame, text="运行", command=self.run_report, width=10)
        self.run_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.stop_button = ttk.Button(btn_frame, text="停止", command=stop_report, width=10)
        self.stop_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.pause_button = ttk.Button(btn_frame, text="暂停", command=pause_process, width=10)
        self.pause_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.resume_button = ttk.Button(btn_frame, text="恢复", command=resume_process, width=10)
        self.resume_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.tree = ttk.Treeview(lf, columns=("k", "v"), show="", height=6)
        self.tree.pack(fill="both", expand=True)
        self.tree.column("k", stretch=False)
        self.tree.column("v", stretch=True)

        lf2 = ttk.Labelframe(row, text="应用时间统计")
        lf2.pack(fill="both", padx=10, pady=5)
        btn2_frame = ttk.Frame(lf2)
        btn2_frame.pack(fill=BOTH, padx=10, pady=5)
        self.run2_button = ttk.Button(btn2_frame, text="运行", command=self.run_aut, width=10)
        self.run2_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.stop2_button = ttk.Button(btn2_frame, text="停止", command=stop_aut, width=10)
        self.stop2_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.analysis_button = ttk.Button(btn2_frame, text="打印分析", command=Aut.print_analysis, width=10)
        self.analysis_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.clear_button = ttk.Button(btn2_frame, text="清空输出", command=self.clear_output_viewer, width=10)
        self.clear_button.pack(side=LEFT, anchor=W, padx=20, pady=2)
        self.tree2 = ttk.Treeview(lf2, columns=("k", "v"), show="", height=5)
        self.tree2.pack(fill="both", expand=True)
        self.tree2.column("k", stretch=False)
        self.tree2.column("v", stretch=True)
        self.update_process_info_loop()
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
        if os.path.exists("report.exe"):
            _args = ["report.exe", "run", "-c", "600", "-k", self.key, "-u", self.url]
        else:
            _args = ["python", "report.py", "run", "-c", "600", "-k", self.key, "-u", self.url]
        try:
            self.process = subprocess.Popen(_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                            text=True, creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                            bufsize=1, encoding="utf-8")
            # 启动线程来读取子进程的输出
            self.output_thread = threading.Thread(target=self.read_output, args=(self.process,))
            self.output_thread.daemon = True
            self.output_thread.start()
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def run_aut(self):
        if is_process_running(read_pid(Aut.aut_pid_file)):
            messagebox.showinfo("info", f"已经在运行!")
            return
        if os.path.exists("report.exe"):
            _args = ["report.exe", "aut"]
        else:
            _args = ["python", "report.py", "aut"]
        try:
            self.process2 = subprocess.Popen(_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                             creationflags=subprocess.CREATE_NO_WINDOW,  # 隐藏控制台窗口
                                             bufsize=1, encoding="utf-8")
            # 启动线程来读取子进程的输出
            self.output_thread2 = threading.Thread(target=self.read_output, args=(self.process2,))
            self.output_thread2.daemon = True
            self.output_thread2.start()
        except Exception as e:
            messagebox.showerror("错误", f"启动失败: {e}")

    def read_output(self, pc):
        try:
            for line in iter(pc.stdout.readline, ""):
                self.output_queue.put(line)
        finally:
            pc.stdout.close()
            pc.wait()

    def update_process_info_loop(self):
        self.update_process_info(pid_file, self.tree)
        self.update_process_info(Aut.aut_pid_file, self.tree2, check_pause=False)
        self.master.after(2000, self.update_process_info_loop)

    def update_process_info(self, pf, tr, check_pause=True):
        err, info = check_process(pf, pt=False, check_pause=check_pause)
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
        if err:
            tr.insert("", "end", values=("Error", f"Error - {err}"))
            return
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
        log_path = os.path.join(log_dir, selected_file)
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
        self.url_entry = ttk.Entry(row, width=50)
        self.url_entry.grid(row=1, column=1, padx=5, pady=5)

        # 密钥
        ttk.Label(row, text="服务器密钥:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.key_entry = ttk.Entry(row, width=50)
        self.key_entry.grid(row=2, column=1, padx=5, pady=5)

        # 排除进程
        ttk.Label(row, text="报告程序排除的进程（,分割添加多个）:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.exclude_list = tk.Listbox(row, width=50, height=10, selectmode="extended")
        self.exclude_list.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.add_entry = ttk.Entry(row)
        self.add_entry.grid(row=5, column=0, padx=5, pady=5, sticky="ew")
        self.add_button = ttk.Button(row, text="添加", command=self.add_exclude_process)
        self.add_button.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.remove_button = ttk.Button(row, text="删除选中", command=self.remove_exclude_process,
                                        bootstyle="danger-outline")
        self.remove_button.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        reload_button = ttk.Button(row, text="重载配置", command=self.load_settings, bootstyle="warning-outline")
        reload_button.grid(row=6, column=0, pady=15, padx=5, sticky="w")
        # 保存按钮
        save_button = ttk.Button(row, text="保存", command=self.save_settings, bootstyle="success-outline")
        save_button.grid(row=6, column=1, pady=15, padx=5, sticky="e")

        # 加载设置
        self.load_settings()

    def on_theme_changed(self, *args):
        selected_theme = self.theme_var.get()
        self.app.style.theme_use(themename=selected_theme)
        print(f"主题已切换为: {selected_theme}")

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

    def save_settings(self):
        self.key = self.key_entry.get()
        self.url = self.url_entry.get()
        cfg.set("DEFAULT", "key", self.key)
        cfg.set("DEFAULT", "url", self.url)
        cfg.set("DEFAULT", "theme", self.theme_var.get())
        cfg.set("DEFAULT", "exclude_process", ",".join(self.exclude_list.get(0, END)))
        self.notebook.update_idletasks()
        cfg.set("DEFAULT", "height", str(self.notebook.winfo_height()))
        cfg.set("DEFAULT", "width", str(self.notebook.winfo_width()))
        e, m = setting_config(cfg)
        if e:
            messagebox.showinfo("info", f"{m}")
        else:
            messagebox.showerror("错误", f"{m}")

    def load_settings(self):
        self.theme_var.set(cfg.get("DEFAULT", "theme", fallback="darkly"))
        height = int(cfg.get("DEFAULT", "height", fallback=800))
        width = int(cfg.get("DEFAULT", "width", fallback=900))
        self.notebook.configure(height=height, width=width)
        self.key_entry.delete(0, END)
        self.key = cfg.get("DEFAULT", "key", fallback="")
        self.key_entry.insert(0, self.key)
        self.url_entry.delete(0, END)
        self.url = cfg.get("DEFAULT", "url", fallback="")
        self.url_entry.insert(0, self.url)
        self.exclude_list.delete(0, END)
        for process in Exclude_Process:
            self.exclude_list.insert("end", process)

    def create_usage(self):
        row = ttk.Frame()
        row.pack(fill="both", expand=True)
        self.notebook.add(row, text="应用使用统计", state="normal")
        # 添加刷新按钮
        usage_ctrl_frame = ttk.Frame(row)
        usage_ctrl_frame.pack(fill=BOTH, padx=10, pady=5)
        refresh_button = ttk.Button(usage_ctrl_frame, text="刷新", command=self.load_usage_data)
        refresh_button.pack(side="left", padx=5, pady=5)
        save_icon_button = ttk.Button(usage_ctrl_frame, text="save icon", command=self.save_icon)
        save_icon_button.pack(side="left", padx=5, pady=5)
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

        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.canvas.bind("<Button-4>", on_mousewheel)
        self.canvas.bind("<Button-5>", on_mousewheel)
        self.app_frames = []
        self.load_usage_data()

    def save_icon(self):
        for o in Aut.get_all_names():
            save_exe_icon(o, o.split('\\')[-1])

    def load_usage_data(self):
        usage_data = get_total_duration_for_all()
        max_duration = max(row["total_duration"] for row in usage_data) if usage_data else 1
        for frame in self.app_frames:
            frame.destroy()
        self.app_frames.clear()
        for app in usage_data:
            self.create_app_frame(app, max_duration)

    def create_app_frame(self, app, max_duration):
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
            icon_label = ttk.Label(app_frame, image=icon_photo)
            icon_label.image = icon_photo
        else:
            icon_label = ttk.Label(app_frame, text="", width=3)
        icon_label.pack(side="left", padx=5)
        name_label = ttk.Label(app_frame, text=app_name, width=30, anchor="w")
        name_label.pack(side="left", padx=5)
        progress = ttk.Progressbar(app_frame, orient="horizontal", length=200, mode="determinate")
        progress["value"] = (total_duration / max_duration) * 100
        progress.pack(side="left", padx=5)
        duration_label = ttk.Label(app_frame, text=f"{seconds2hms(total_duration)}", width=10, anchor="e")
        duration_label.pack(side="left", padx=5)

    def create_about(self):
        def open_url(event):
            webbrowser.open("https://github.com/2412322029/seeme")

        row = ttk.Frame()
        row.pack(fill="both", expand=True)
        self.notebook.add(row, text="关于", state="normal")
        ttk.Label(row, text="Home page:").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        label2 = ttk.Label(row, text="https://github.com/2412322029/seeme", foreground="#2AADFF", cursor="hand2")
        label2.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        label2.bind("<Button-1>", open_url)


def main():
    app = ttk.Window("Report", "darkly")
    try:
        app.iconbitmap("icon.ico")
    except Exception as e:
        print(f"Error setting icon: {e}")
    mainWindows(app)
    app.mainloop()


if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        main()
    else:
        from report import main, args_parser

        args = args_parser()
        main(args)
