import pyautogui
import keyboard
import time






def perform_actions_f5():
    time.sleep(1)  # 延迟执行
    for _ in range(1):
        pyautogui.press('f5')
    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.press('f5')
        

    for _ in range(1):
        pyautogui.press('f5')

    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.press('f5')

    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.press('f5')
    pyautogui.hotkey('ctrl', 'tab')
    for _ in range(1):
        pyautogui.press('f5')
    pyautogui.hotkey('ctrl', 'tab')

def perform_actions():
    time.sleep(1)  # 延迟执行
    for _ in range(3):
        pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.hotkey('alt', 'r')
        pyautogui.hotkey('alt', 'q')
        pyautogui.hotkey('alt', 'q')
        

    for _ in range(1):
        pyautogui.hotkey('alt', 'r')
        pyautogui.hotkey('alt', 'q')
        pyautogui.hotkey('alt', 'q')

    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.hotkey('alt', 'r')
        
        pyautogui.hotkey('alt', 'q')
        pyautogui.hotkey('alt', 'q')

    pyautogui.hotkey('ctrl', 'tab')

    for _ in range(1):
        pyautogui.hotkey('alt', 'r')
        pyautogui.hotkey('alt', 'q')
        pyautogui.hotkey('alt', 'q')
    pyautogui.hotkey('ctrl', 'tab')
    for _ in range(1):
        pyautogui.hotkey('alt', 'r')
        pyautogui.hotkey('alt', 'q')
        pyautogui.hotkey('alt', 'q')

    pyautogui.hotkey('ctrl', 'tab')


# window = mhWindow.MHWindow()
# 抓鬼(window, True)

print("按下 Tab 键将触发操作...")

# 监听键盘
while True:
    if keyboard.is_pressed('shift'):
        perform_actions()
        while keyboard.is_pressed('shift'):  # 等待释放 Tab 键
            time.sleep(0.1)
