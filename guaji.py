# coding=utf-8
from tkinter import NO
import mhWindow
import re
import json
import sys
import io
import time
import pyautogui
import utils
from winsound import PlaySound
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
from winsound import PlaySound
projectPath = mhWindow.projectPath
import mouse



if __name__ == '__main__':
    print('F_开始封妖任务')
    window = mhWindow.MHWindow()
    while(True):
        # 判断是否在战斗
        if(window.F_是否在战斗()):
            print('进入战斗')
            # 等待战斗结束
            while True:
                time.sleep(1)
                point = window.F_窗口内查找图片('window_zidong2.png')
                if(point):
                    print('开始自动操作')
                    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
                    time.sleep(20)
                if(window.F_是否结束战斗()):
                    print('战斗结束')
                    # 播放音频
                    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
                    break
        
        time.sleep(2)
    
