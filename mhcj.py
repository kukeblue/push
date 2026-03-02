import pyautogui
import keyboard
import time
import mhWindow
import win32gui
import win32con
import win32api
import ctypes
from ctypes import wintypes
import mouse


def press_key(key, times=1):
    """按键指定次数"""
    for _ in range(times):
        pyautogui.press(key)


def press_hotkey(*keys, times=1):
    """组合键指定次数"""
    for _ in range(times):
        pyautogui.hotkey(*keys)


def switch_tab():
    """切换到下一个标签页"""
    pyautogui.hotkey('ctrl', 'tab')


def perform_actions_f5():
    """执行 F5 相关的操作序列"""
    time.sleep(1)  # 延迟执行
    
    # 第一组操作
    press_key('f5')
    switch_tab()
    
    # 第二组操作
    press_key('f5')
    switch_tab()
    
    # 第三组操作
    press_key('f5')
    switch_tab()
    
    # 第四组操作
    press_key('f5')
    switch_tab()
    
    # 第五组操作
    press_key('f5')
    switch_tab()
    
    # 第六组操作
    press_key('f5')
    switch_tab()

def perform_actions_f2(window):
    """执行 Alt 组合键相关的操作序列"""
    time.sleep(1)  # 延迟执行
    window.F_游戏光标移动到(382, 102)
    # 第一组：Alt+D 三次，然后切换标签
    press_hotkey('alt', 'q', times=2)
    switch_tab()

    # 第二组：Alt+Q, Alt+A, Alt+A
    window.F_游戏光标移动到(382, 102)
    pyautogui.press('f2')
    pyautogui.click()
    pyautogui.click()
    press_hotkey('alt', 'q', times=2)
    switch_tab()

    # 第三组：Alt+Q, Alt+A, Alt+A
    window.F_游戏光标移动到(382, 102)
    pyautogui.press('f2')
    pyautogui.click()
    pyautogui.click()
    press_hotkey('alt', 'q', times=2)
    switch_tab()

    # 第四组：Alt+Q, Alt+A, Alt+A
    window.F_游戏光标移动到(382, 102)
    pyautogui.press('f2')
    pyautogui.click()
    pyautogui.click()
    press_hotkey('alt', 'q', times=2)
    switch_tab()

    # 第五组：Alt+Q, Alt+A, Alt+A
    window.F_游戏光标移动到(382, 102)
    pyautogui.press('f2')
    pyautogui.click()
    pyautogui.click()
    press_hotkey('alt', 'q', times=2)
    switch_tab()

def perform_actions_3():
    """执行 Alt 组合键相关的操作序列"""
    time.sleep(1)  # 延迟执行

    press_hotkey('alt', 'd')
    press_hotkey('alt', 'd')
    switch_tab()

    # 第一组：Alt+D 三次，然后切换标签
    press_hotkey('alt', 'q', times=2)
    press_hotkey('alt', 'q')
    switch_tab()
    
    # 第二组：Alt+Q, Alt+A, Alt+A
    press_hotkey('alt', 'q')
    press_hotkey('alt', 'q', times=2)
    switch_tab()
    
    # # 第三组：Alt+Q, Alt+A, Alt+A
    # press_hotkey('alt', 'q')
    # press_hotkey('alt', 'a', times=2)
    # switch_tab()
    
    # 第四组：Alt+Q, Alt+A, Alt+A
    press_hotkey('alt', 'q')
    press_hotkey('alt', 'q', times=2)
    switch_tab()

def perform_actions():
    """执行 Alt 组合键相关的操作序列"""
    time.sleep(1)  # 延迟执行

    # press_hotkey('alt', 'q')
    # press_hotkey('alt', 'q')
    # switch_tab()

    # 第一组：Alt+D 三次，然后切换标签
    pyautogui.press('f5')
    press_hotkey('alt', 'd', times=1)
    switch_tab()
    
    # 第二组：Alt+Q, Alt+A, Alt+A
    press_hotkey('alt', 'q')
    press_hotkey('alt', 'd', times=2)
    switch_tab()
    
    # 第三组：Alt+Q, Alt+A, Alt+A
    press_hotkey('alt', 'q')
    press_hotkey('alt', 'd', times=2)
    switch_tab()
    
    # 第四组：Alt+Q, Alt+A, Alt+A
    press_hotkey('alt', 'q')
    press_hotkey('alt', 'd', times=2)
    switch_tab()    
    # time.sleep(10)
    # while(True):
    #     if(window.F_是否结束战斗()):
    #         break
    #     ret = window.utils.findPicture('window_zidong2.png')
    #     if(ret != None):
    #         print('发现自动')
    #         perform_actions_f2(window)
    #         break
    #     time.sleep(1)
    
    # 第五组：Alt+Q 三次
    # press_hotkey('alt', 'q', times=3)
    # switch_tab()
    
    # # 第六组：Alt+Q 三次
    # press_hotkey('alt', 'q', times=3)
    # switch_tab()


# 全局变量存储窗口句柄
window_handle = None
# 执行状态标志，防止重复触发
is_executing = False

def perform_actions_z():
    """按下 z 键时执行：按 6 -> 点击鼠标 -> 按 q -> 点击鼠标"""
    global window_handle, is_executing
    
    # 如果正在执行，直接返回
    if is_executing:
        return
    
    # 设置执行标志
    is_executing = True
    
    try:
        # 使用已保存的窗口句柄
        if window_handle is None:
            # 如果窗口句柄未初始化，则获取当前鼠标位置下的窗口
            pos = pyautogui.position()
            handle = win32gui.WindowFromPoint((pos.x, pos.y))
        else:
            handle = window_handle
        
        # 方法1: 使用 SetForegroundWindow 激活窗口，然后发送键盘消息
        # 激活窗口（如果已激活则不需要重复激活） 
        # 先按 6 键
        scan_code_6 = win32api.MapVirtualKey(0x36, 0)  # VK_6 的扫描码 (0x36)
        lparam_down_6 = (scan_code_6 << 16) | 1  # 按下
        lparam_up_6 = (scan_code_6 << 16) | 0xC0000001  # 释放
        
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, 0x36, lparam_down_6)
        time.sleep(0.05)
        win32gui.SendMessage(handle, win32con.WM_KEYUP, 0x36, lparam_up_6)
        # time.sleep(1)
        
        # 点击鼠标
        win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        time.sleep(0.5)
        
        # 发送 q 键 - 使用完整的键盘消息参数
        # lParam 参数格式: 0-15位: 重复次数, 16-23位: 扫描码, 24位: 扩展键, 25-28位: 保留, 29位: 上下文, 30位: 前一个键状态, 31位: 转换状态
        scan_code = win32api.MapVirtualKey(0x51, 0)  # VK_Q 的扫描码
        lparam_down = (scan_code << 16) | 1  # 按下
        lparam_up = (scan_code << 16) | 0xC0000001  # 释放
        
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, 0x51, lparam_down)
        time.sleep(0.05)
        win32gui.SendMessage(handle, win32con.WM_KEYUP, 0x51, lparam_up)
        time.sleep(1)
        
        # 再次点击鼠标
        win32gui.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
        win32gui.SendMessage(handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, 0)
        time.sleep(1)
        
        # 最后按 Q 键
        scan_code_q = win32api.MapVirtualKey(0x51, 0)  # VK_Q 的扫描码
        lparam_down_q = (scan_code_q << 16) | 1  # 按下
        lparam_up_q = (scan_code_q << 16) | 0xC0000001  # 释放
        
        win32gui.SendMessage(handle, win32con.WM_KEYDOWN, 0x51, lparam_down_q)
        time.sleep(0.05)
        win32gui.SendMessage(handle, win32con.WM_KEYUP, 0x51, lparam_up_q)
        time.sleep(1)
    finally:
        # 重置执行标志，允许下次触发
        is_executing = False
    # except:
    #     # 方法2: 如果方法1失败，尝试使用 SendInput API
    #     try:
    #         # 定义 SendInput 结构
    #         PUL = ctypes.POINTER(ctypes.c_ulong)
            
    #         class KeyBdInput(ctypes.Structure):
    #             _fields_ = [("wVk", ctypes.c_ushort),
    #                       ("wScan", ctypes.c_ushort),
    #                       ("dwFlags", ctypes.c_ulong),
    #                       ("time", ctypes.c_ulong),
    #                       ("dwExtraInfo", PUL)]
            
    #         class HardwareInput(ctypes.Structure):
    #             _fields_ = [("uMsg", ctypes.c_ulong),
    #                       ("wParamL", ctypes.c_short),
    #                       ("wParamH", ctypes.c_ushort)]
            
    #         class MouseInput(ctypes.Structure):
    #             _fields_ = [("dx", ctypes.c_long),
    #                       ("dy", ctypes.c_long),
    #                       ("mouseData", ctypes.c_ulong),
    #                       ("dwFlags", ctypes.c_ulong),
    #                       ("time", ctypes.c_ulong),
    #                       ("dwExtraInfo", PUL)]
            
    #         class Input_I(ctypes.Union):
    #             _fields_ = [("ki", KeyBdInput),
    #                       ("mi", MouseInput),
    #                       ("hi", HardwareInput)]
            
    #         class Input(ctypes.Structure):
    #             _fields_ = [("type", ctypes.c_ulong),
    #                       ("ii", Input_I)]
            
    #         # 激活窗口
    #         win32gui.SetForegroundWindow(handle)
    #         time.sleep(0.1)
            
    #         # 点击鼠标
    #         pyautogui.click()
    #         time.sleep(1)
            
    #         # 发送 q 键
    #         extra = ctypes.c_ulong(0)
    #         ii_ = Input_I()
    #         ii_.ki = KeyBdInput(0x51, 0, 0, 0, ctypes.pointer(extra))  # VK_Q
    #         x = Input(ctypes.c_ulong(1), ii_)
    #         ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
    #         time.sleep(0.05)
            
    #         # 释放 q 键
    #         ii_.ki = KeyBdInput(0x51, 0, 0x0002, 0, ctypes.pointer(extra))  # KEYEVENTF_KEYUP
    #         x = Input(ctypes.c_ulong(1), ii_)
    #         ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            
    #         time.sleep(1)
            
    #         # 再次点击鼠标
    #         pyautogui.click()
    #         time.sleep(1)
    #     except:
    #         # 方法3: 最后的备选方案 - 使用 keyboard 库但先激活窗口
    #         win32gui.SetForegroundWindow(handle)
    #         time.sleep(0.1)
    #         pyautogui.click()
    #         time.sleep(1)
    #         keyboard.send('q')
    #         time.sleep(1)
    #         pyautogui.click()
    #         time.sleep(1)


# window = mhWindow.MHWindow()

# print("按下 Alt+1 键将触发操作...")

# 程序启动5秒后激活窗口
# print("程序启动，5秒后将激活鼠标所在位置的窗口...")
# time.sleep(5)
# pos = pyautogui.position()
# window_handle = win32gui.WindowFromPoint((pos.x, pos.y))
# win32gui.SetForegroundWindow(window_handle)
# print(f"窗口已激活，句柄: {window_handle}")

# 注册组合键监听
# keyboard.add_hotkey('alt+2', lambda: perform_actions_f2(window))
keyboard.add_hotkey('alt+1', lambda: perform_actions())
# keyboard.add_hotkey('alt+1', lambda: perform_actions_3())
keyboard.add_hotkey('e', lambda: perform_actions_z())

# 注册鼠标滚轮键（中键）监听
mouse.on_middle_click(lambda: perform_actions_z())


# 保持程序运行
try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\n程序已退出")
