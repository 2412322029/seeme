import tkinter as tk


class ToolTip:
    def __init__(self, widget, text, delay=500, at_show_func=None, at_leave=None):
        self.label = None
        self.widget = widget
        self.text = text
        self.delay = delay  # 提示框显示的延迟时间（毫秒）
        self.at_show_func = at_show_func
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.at_leave = at_leave
        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event):
        # 获取鼠标在屏幕上的位置
        self.x = self.widget.winfo_pointerx() + 20
        self.y = self.widget.winfo_pointery() + 20
        if self.id is None:
            self.id = self.widget.after(self.delay, self.show_tooltip)

    def on_leave(self, event):
        if self.id is not None:
            self.widget.after_cancel(self.id)
            self.id = None
        self.hide_tooltip()
        if self.at_leave:
            self.at_leave()

    def on_motion(self, event):
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow:
            self.tipwindow.geometry(f"+{self.x}+{self.y}")

    def show_tooltip(self):
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{self.x}+{self.y}")
        self.label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT, relief='groove', borderwidth=2,
                              font=("tahoma", "10", "normal"))
        self.label.pack(ipadx=4)
        if self.at_show_func:
            self.at_show_func(self.label)

    def hide_tooltip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class BarChart(tk.Canvas):
    def __init__(self, master=None, data=None, width=400, height=300, **kwargs):
        """
        初始化柱状图组件
        :param master: 父窗口
        :param data: 数据列表，格式为 [(标签, 值, 颜色, 事件类型, 回调函数, Tooltip文本), ...]
        :param width: Canvas 宽度
        :param height: Canvas 高度
        :param kwargs: 其他 Canvas 参数
        """
        super().__init__(master, width=width, height=height, **kwargs)
        self.data = data if data else [
            ("A", 10, "red", "<Button-1>", self.on_click, "这是A柱子"),
            ("B", 20, "green", "<Button-1>", self.on_click, "这是B柱子"),
            ("C", 15, "blue", "<Button-1>", self.on_click, "这是C柱子"),
            ("D", 30, "purple", "<Button-1>", self.on_click, "这是D柱子")
        ]
        self.width = width
        self.height = height
        self.draw_chart()

    def draw_chart(self):
        # 计算最大值和柱子宽度
        max_value = max(value for _, value, _, _, _, _ in self.data)
        bar_width = self.width / len(self.data) * 0.8  # 柱子宽度为总宽度的80%
        spacing = (self.width - bar_width * len(self.data)) / (len(self.data) + 1)  # 柱子间距

        # 绘制柱状图
        for i, (label, value, color, event_type, callback, tooltip_text) in enumerate(self.data):
            x0 = spacing * (i + 1) + bar_width * i
            y0 = self.height - (value / max_value * self.height)
            x1 = x0 + bar_width
            y1 = self.height

            # 绘制柱子
            bar_id = self.create_rectangle(x0, y0, x1, y1, fill=color, outline='black', tags=f"bar_{i}")
            # 绑定事件
            self.tag_bind(bar_id, event_type, lambda event, idx=i, cb=callback: cb(event, idx))
            # 添加 Tooltip
            self.tag_bind(bar_id, "<Enter>",
                          lambda event, idx=i, text=tooltip_text: self.show_tooltip(event, idx, text))
            self.tag_bind(bar_id, "<Leave>", lambda event, idx=i: self.hide_tooltip(event, idx))

            # 绘制标签
            self.create_text(x0 + bar_width / 2, self.height + 10, text=label, anchor='n')

            # 绘制数值标签
            self.create_text(x0 + bar_width / 2, y0 - 10, text=str(value), anchor='s')

        self.tooltips = {}

    def show_tooltip(self, event, index, text):
        if index not in self.tooltips:
            self.tooltips[index] = ToolTip(self, text)

    def hide_tooltip(self, event, index):
        if index in self.tooltips:
            del self.tooltips[index]

    def on_click(self, event, index):
        # 默认的点击事件回调函数
        print(f"柱子 {index} 被点击了！")


if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.title("柱状图示例")

    # 创建柱状图组件
    data = [
        ("苹果", 30, "red", "<Button-1>", lambda event, idx: print(f"苹果柱子 {idx} 被点击"), "这是苹果柱子"),
        ("香蕉", 20, "yellow", "<Button-1>", lambda event, idx: print(f"香蕉柱子 {idx} 被点击"), "这是香蕉柱子"),
        ("橙子", 40, "orange", "<Button-1>", lambda event, idx: print(f"橙子柱子 {idx} 被点击"), "这是橙子柱子"),
        ("葡萄", 10, "purple", "<Button-1>", lambda event, idx: print(f"葡萄柱子 {idx} 被点击"), "这是葡萄柱子")
    ]
    chart = BarChart(root, data=data, width=50, height=300)
    chart.pack(padx=20, pady=20)

    # 运行主循环
    root.mainloop()
