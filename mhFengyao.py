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
from Images.index import IMAGES_FENGYAO

projectPath = utils.projectPath

window = mhWindow.MHWindow()
def F_是否刷新封妖(window):
    point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖刷新'], confidence=0.9)
    if(point):
        return True
    return False


if __name__ == '__main__':
    print('F_开始封妖任务')
    while(True):
        # 判断是否在战斗
        if(window.F_是否在战斗()):
            print('进入战斗')
            # 等待战斗结束
            while True:
                time.sleep(0.1)
                if(window.F_是否结束战斗()):
                    print('战斗结束')
                    # 播放音频
                    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
                    break
        
        if(F_是否刷新封妖(window)):
            print('发现封妖')
            PlaySound(projectPath + "\\" + "y913.wav", flags=1)
        time.sleep(2)
        # print('未发现封妖')
