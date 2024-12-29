# coding=utf-8
from tkinter import NO
import mhWindow
import re
import json
import sys
import io
import time
import fire
import pyautogui
import utils
from winsound import PlaySound
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
import mouse



if __name__ == '__main__':
    print('开始脚本')
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow()
    window.utils.click()
    while True:
        
        for i in range(4):
            window.F_游戏光标移动到(251, 341)
            if(i == 0):
                while window.F_是否在战斗():
                    time.sleep(1)
                        
                pyautogui.hotkey('alt', 'e')
                time.sleep(1)
                mouse.right_click()
                time.sleep(1)
                pyautogui.hotkey('alt', 'e')
                time.sleep(1)
            mouse.click()
            time.sleep(1)
            mouse.click()
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'tab')
            time.sleep(1)
        time.sleep(300)

    
