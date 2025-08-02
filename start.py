import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import psutil
import os
from tkinter import font as tkfont

class Application:
    def __init__(self, master):
        self.master = master
        master.title("寻觅控制面板")
        master.geometry("450x400")
        master.configure(bg="#f0f2f5")
        
        # 获取当前进程ID
        self.current_pid = os.getpid()
        
        # 存储所有启动的进程
        self.processes = {
            "mhLogin.py": None,
            "mhLogin2.py": None,
            "mhZhuagui.py": None
        }

        # 自定义字体
        self.title_font = tkfont.Font(family="Microsoft YaHei", size=14, weight="bold")
        self.button_font = tkfont.Font(family="Microsoft YaHei", size=10)

        # 主标题
        self.header = ttk.Label(
            master, 
            text="寻觅多功能控制台",
            font=self.title_font,
            background="#f0f2f5",
            foreground="#333333"
        )
        self.header.pack(pady=(20, 10))

        # 主框架
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # 配置样式
        self.setup_styles()

        # 按钮布局
        button_params = {
            "width": 15,
            "padding": (10, 5)  # 通过padding控制按钮高度
        }

        # 启动游戏1按钮
        self.start_game1_btn = ttk.Button(
            self.main_frame, 
            text="启动游戏1", 
            command=lambda: self.start_script("mhLogin.py", "游戏1"),
            style="Game1.TButton",
            **button_params
        )
        self.start_game1_btn.pack(pady=8, padx=20, fill=tk.X)

        # 启动游戏2按钮
        self.start_game2_btn = ttk.Button(
            self.main_frame, 
            text="启动游戏2", 
            command=lambda: self.start_script("mhLogin2.py", "游戏2"),
            style="Game2.TButton",
            **button_params
        )
        self.start_game2_btn.pack(pady=8, padx=20, fill=tk.X)

        # 抓鬼按钮
        self.zhuagui_btn = ttk.Button(
            self.main_frame, 
            text="抓鬼脚本", 
            command=lambda: self.start_script("mhZhuagui.py", "抓鬼"),
            style="Zhuagui.TButton",
            **button_params
        )
        self.zhuagui_btn.pack(pady=8, padx=20, fill=tk.X)

        # 关闭全部按钮
        self.stop_all_btn = ttk.Button(
            self.main_frame, 
            text="关闭全部", 
            command=self.stop_all,
            style="StopAll.TButton",
            **button_params
        )
        self.stop_all_btn.pack(pady=8, padx=20, fill=tk.X)

        # 状态栏
        self.status_bar = ttk.Label(
            master, 
            text="就绪",
            relief=tk.SUNKEN,
            anchor=tk.W,
            background="#e9ecef",
            foreground="#495057",
            font=("Microsoft YaHei", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_styles(self):
        """配置所有按钮样式"""
        style = ttk.Style()
        
        # 基础按钮样式
        style.configure("TButton", 
                      font=self.button_font,
                      padding=6)
        
        # 游戏1按钮样式
        style.configure("Game1.TButton",
                      foreground="white",
                      background="#4e73df",
                      bordercolor="#4e73df",
                      focuscolor="#4e73df")
        
        # 游戏2按钮样式
        style.configure("Game2.TButton",
                      foreground="white",
                      background="#1cc88a",
                      bordercolor="#1cc88a",
                      focuscolor="#1cc88a")
        
        # 抓鬼按钮样式
        style.configure("Zhuagui.TButton",
                      foreground="white",
                      background="#36b9cc",
                      bordercolor="#36b9cc",
                      focuscolor="#36b9cc")
        
        # 关闭按钮样式
        style.configure("StopAll.TButton",
                      foreground="white",
                      background="#e74a3b",
                      bordercolor="#e74a3b",
                      focuscolor="#e74a3b")

        # 使按钮颜色在Windows上生效
        style.map("Game1.TButton",
                 background=[("active", "#3a56b5")])
        style.map("Game2.TButton",
                 background=[("active", "#17a673")])
        style.map("Zhuagui.TButton",
                 background=[("active", "#2a9eb4")])
        style.map("StopAll.TButton",
                 background=[("active", "#c23a2b")])

    def start_script(self, script_name, display_name):
        """启动指定脚本"""
        if self.processes.get(script_name) is None:
            try:
                self.processes[script_name] = subprocess.Popen(["python", script_name])
                self.update_status(f"{display_name}启动成功")
                # messagebox.showinfo("提示", f"{display_name}启动成功！")
            except Exception as e:
                self.update_status(f"启动{display_name}失败")
                messagebox.showerror("错误", f"启动{display_name}失败: {str(e)}")
        else:
            self.update_status(f"{display_name}已在运行中")
            messagebox.showwarning("警告", f"{display_name}已经在运行中！")

    def stop_all(self):
        """关闭所有启动的脚本，但不关闭控制面板本身"""
        try:
            # 关闭所有记录的进程
            for script_name, process in self.processes.items():
                if process:
                    process.terminate()
                    self.processes[script_name] = None
            
            # 额外检查并关闭所有Python进程（排除自己）
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['pid'] == self.current_pid:
                        continue
                        
                    if proc.info['name'].lower() in ['python.exe', 'python', 'python3']:
                        p = psutil.Process(proc.info['pid'])
                        p.terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.update_status("已关闭所有游戏和脚本")
            messagebox.showinfo("提示", "已关闭所有游戏和脚本！")
        except Exception as e:
            self.update_status("关闭进程出错")
            messagebox.showerror("错误", f"关闭进程时出错: {str(e)}")

    def update_status(self, message):
        """更新状态栏"""
        self.status_bar.config(text=f"状态: {message}")
        self.master.after(3000, lambda: self.status_bar.config(text="就绪"))

if __name__ == "__main__":
    # 检查并安装psutil
    try:
        import psutil
    except ImportError:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "psutil"])
        import psutil
    
    root = tk.Tk()
    
    # 设置窗口图标（如果有）
    try:
        root.iconbitmap("icon.ico")  # 请准备一个icon.ico文件
    except:
        pass
    
    app = Application(root)
    root.mainloop()