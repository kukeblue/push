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
from Images.index import IMAGES_FENGYAO

projectPath = utils.projectPath

window = mhWindow.MHWindow()

import io
from contextlib import redirect_stdout
import os
import sys

# 方法1: 重定向到空设备
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

if __name__ == '__main__':
    time.sleep(25)
    while True:
        window.F_关闭对话()
        window.F_小地图寻路(['24', '33'], 检查是否到达指定坐标=False)
        print('已寻路至封妖地点')
        time.sleep(3)
        pyautogui.hotkey('alt', '7')
        time.sleep(1)
        window.F_关闭对话()
        point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务2'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务1'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务3'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务4'], confidence=0.9)
        if point:
            window.F_游戏光标移动到(point[0]+10, point[1])
            time.sleep(1)
            window.utils.click()
            window.utils.click()
            window.F_关闭对话()
            break
    while True:
        window.F_小地图寻路(['77', '67'], 检查是否到达指定坐标=False)
        print('已寻路至封妖地点')
        time.sleep(3)
        pyautogui.hotkey('alt', '7')
        time.sleep(1)
        window.F_关闭对话()
        point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务2'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务1'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务3'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务4'], confidence=0.9)
        if point:
            window.F_游戏光标移动到(point[0]+10, point[1])
            time.sleep(1)
            window.utils.click()
            window.utils.click()
            window.F_关闭对话()
            break
    while True:
        window.F_小地图寻路(['46', '110'], 检查是否到达指定坐标=False)
        print('已寻路至封妖地点')
        time.sleep(3)
        pyautogui.hotkey('alt', '7')
        time.sleep(2)
        window.F_关闭对话()
        point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务2'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务1'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务3'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务4'], confidence=0.9)
        if point:
            window.F_游戏光标移动到(point[0]+10, point[1])
            time.sleep(1)
            window.utils.click()
            window.utils.click()
            window.F_关闭对话()
            break

    window.F_小地图寻路(['75', '163'], 检查是否到达指定坐标=False)
    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
    time.sleep(3)



