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
        master.geometry("450x450")
        master.configure(bg="#f0f2f5")
        
        self.current_pid = os.getpid()
        
        # 所有可启动的脚本
        self.processes = {
            "mhLogin.py": None,
            "mhLogin2.py": None,
            "mhZhuagui.py": None,
            "mhZhuagui2.py": None
        }

        self.title_font = tkfont.Font(family="Microsoft YaHei", size=14, weight="bold")
        self.button_font = tkfont.Font(family="Microsoft YaHei", size=10)

        self.header = ttk.Label(
            master, 
            text="寻觅多功能控制台",
            font=self.title_font,
            background="#f0f2f5",
            foreground="#333333"
        )
        self.header.pack(pady=(20, 10))

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.setup_styles()

        button_params = {
            "width": 15,
            "padding": (10, 5)
        }

        self.start_game1_btn = ttk.Button(
            self.main_frame, 
            text="启动游戏1", 
            command=lambda: self.start_script("mhLogin.py", "游戏1"),
            style="Game1.TButton",
            **button_params
        )
        self.start_game1_btn.pack(pady=8, padx=20, fill=tk.X)

        self.start_game2_btn = ttk.Button(
            self.main_frame, 
            text="启动游戏2", 
            command=lambda: self.start_script("mhLogin2.py", "游戏2"),
            style="Game2.TButton",
            **button_params
        )
        self.start_game2_btn.pack(pady=8, padx=20, fill=tk.X)

        self.zhuagui_btn = ttk.Button(
            self.main_frame, 
            text="抓鬼脚本", 
            command=lambda: self.start_script("mhZhuagui.py", "抓鬼"),
            style="Zhuagui.TButton",
            **button_params
        )
        self.zhuagui_btn.pack(pady=8, padx=20, fill=tk.X)

        self.zhuagui2_btn = ttk.Button(
            self.main_frame, 
            text="抓鬼脚本2", 
            command=lambda: self.start_script("mhZhuagui2.py", "抓鬼2"),
            style="Zhuagui.TButton",
            **button_params
        )
        self.zhuagui2_btn.pack(pady=8, padx=20, fill=tk.X)

        self.stop_all_btn = ttk.Button(
            self.main_frame, 
            text="关闭全部", 
            command=self.stop_all,
            style="StopAll.TButton",
            **button_params
        )
        self.stop_all_btn.pack(pady=8, padx=20, fill=tk.X)

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
        style = ttk.Style()
        style.configure("TButton", font=self.button_font, padding=6)
        
        style.configure("Game1.TButton",
                      foreground="white",
                      background="#4e73df",
                      bordercolor="#4e73df",
                      focuscolor="#4e73df")
        
        style.configure("Game2.TButton",
                      foreground="white",
                      background="#1cc88a",
                      bordercolor="#1cc88a",
                      focuscolor="#1cc88a")
        
        style.configure("Zhuagui.TButton",
                      foreground="white",
                      background="#36b9cc",
                      bordercolor="#36b9cc",
                      focuscolor="#36b9cc")
        
        style.configure("StopAll.TButton",
                      foreground="white",
                      background="#e74a3b",
                      bordercolor="#e74a3b",
                      focuscolor="#e74a3b")

        style.map("Game1.TButton", background=[("active", "#3a56b5")])
        style.map("Game2.TButton", background=[("active", "#17a673")])
        style.map("Zhuagui.TButton", background=[("active", "#2a9eb4")])
        style.map("StopAll.TButton", background=[("active", "#c23a2b")])

    def start_script(self, script_name, display_name):
        if self.processes.get(script_name) is None:
            try:
                self.processes[script_name] = subprocess.Popen(["python", script_name])
                self.update_status(f"{display_name}启动成功")
            except Exception as e:
                self.update_status(f"启动{display_name}失败")
                messagebox.showerror("错误", f"启动{display_name}失败: {str(e)}")
        else:
            self.update_status(f"{display_name}已在运行中")
            messagebox.showwarning("警告", f"{display_name}已经在运行中！")

    def stop_all(self):
        try:
            for script_name, process in self.processes.items():
                if process:
                    process.terminate()
                    self.processes[script_name] = None
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['pid'] == self.current_pid:
                        continue
                    if proc.info['name'].lower() in ['python.exe', 'python', 'python3']:
                        psutil.Process(proc.info['pid']).terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            self.update_status("已关闭所有游戏和脚本")
            messagebox.showinfo("提示", "已关闭所有游戏和脚本！")
        except Exception as e:
            self.update_status("关闭进程出错")
            messagebox.showerror("错误", f"关闭进程时出错: {str(e)}")

    def update_status(self, message):
        self.status_bar.config(text=f"状态: {message}")
        self.master.after(3000, lambda: self.status_bar.config(text="就绪"))

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        import subprocess
        subprocess.check_call(["python", "-m", "pip", "install", "psutil"])
        import psutil
    
    root = tk.Tk()
    try:
        root.iconbitmap("icon.ico")
    except:
        pass

    app = Application(root)
    root.mainloop()
