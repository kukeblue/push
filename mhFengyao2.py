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

# import io
# from contextlib import redirect_stdout
# import os
# import sys

# # 方法1: 重定向到空设备
# sys.stdout = open(os.devnull, 'w')
# sys.stderr = open(os.devnull, 'w')

def F_领取任务(window):
    for i in range(10):

        print('F_领取任务')
        window.F_使用道具('daoju_xfxq_red.png')
        window.F_游戏光标移动到(198, 339)
        window.utils.click()
        window.F_关闭道具()
        if(window.F_获取当前地图() == '长安城'):
            break

if __name__ == '__main__':
    # 位置信息 = [window.GameWindowArea[0] + 638, window.GameWindowArea[1] + 139,
    #             150, 85]
    # ret = window.utils.baidu通用文字识别(位置信息)
    # print(ret)

    time.sleep(20)
    while True:
        window.F_小地图寻路(['24', '33'], 检查是否到达指定坐标=False, 是否等待人物停止移动=False)
        window.F_关闭对话()
        window.F_等待人物停止移动()
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
            window.utils.click()
            window.utils.click()
            break
    while True:
        window.F_小地图寻路(['77', '67'], 检查是否到达指定坐标=False,是否等待人物停止移动=False)
        window.F_关闭对话()
        window.F_等待人物停止移动()
        time.sleep(3)
        pyautogui.hotkey('alt', '7')
        time.sleep(1)
        
        point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务2'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务1'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务3'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务4'], confidence=0.9)
        if point:
            window.F_游戏光标移动到(point[0]+10, point[1])
            window.utils.click()
            window.utils.click()
            break
    while True:
        window.F_小地图寻路(['46', '110'], 检查是否到达指定坐标=False, 是否等待人物停止移动=False)
        window.F_关闭对话()
        window.F_等待人物停止移动()
        time.sleep(3)
        pyautogui.hotkey('alt', '7')
        time.sleep(2)
        point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务2'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务1'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务3'], confidence=0.9)
        if(not point):
            point = window.F_窗口内查找图片(IMAGES_FENGYAO['封妖任务4'], confidence=0.9)
        if point:
            window.F_游戏光标移动到(point[0]+10, point[1])
            window.utils.click()
            window.utils.click()
            break

    window.F_小地图寻路(['75', '163'], 检查是否到达指定坐标=False, 是否等待人物停止移动=False)
    window.F_关闭对话()
    # window.F_游戏光标移动到(341, 218)
    # pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    window.F_游戏光标移动到(341, 218)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    window.F_游戏光标移动到(341, 218)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    window.F_游戏光标移动到(341, 218)
    pyautogui.click()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'tab')
    window.F_游戏光标移动到(341, 218)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'tab')

    window.F_关闭对话()
    window.F_等待人物停止移动()
    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
    time.sleep(150)
    if(window.F_是否在战斗()):
        print('进入战斗')
        # 等待战斗结束
        while True:
            time.sleep(0.1)
            if(window.F_是否结束战斗()):
                print('战斗结束')
                # 播放音频
                # PlaySound(projectPath + "\\" + "y913.wav", flags=1)
                break
    time.sleep(2)
    window.F_关闭对话()
    pyautogui.hotkey('alt', 'w')
    window.F_游戏光标移动到(715, 160)
    pyautogui.hotkey('alt', 'w')
    time.sleep(1)
    window.utils.click()
    time.sleep(2)
    window.F_关闭对话()
    F_领取任务(window)
    pyautogui.hotkey('alt', 'w')
    window.F_游戏光标移动到(660, 180)
    pyautogui.hotkey('alt', 'w')
    time.sleep(1)
    window.utils.click()
    time.sleep(3)
    PlaySound(projectPath + "\\" + "y913.wav", flags=1)
       
        



