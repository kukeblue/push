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


def 铃铛():
    print('F_领取铃铛任务')
    time.sleep(3)
    MHWindow = mhWindow.MHWindow
    window = MHWindow()
    window.utils.click()
    while True:
        F_铃铛任务(window)


def F_铃铛任务(window):
    window.F_游戏光标移动到(173, 335)
    time.sleep(0.5)
    window.utils.click()
    time.sleep(1)
    window.utils.click()
    pyautogui.hotkey('alt', 'q')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'q')
    time.sleep(0.5)
    pyautogui.hotkey('alt', 'q')
    time.sleep(0.5)
    任务 = window.F_识别自定义任务()
    print(任务)
    if('弱妖' in 任务):
        找怯弱妖(window, 任务)
    if('虫' in 任务 and '使用' in 任务):
        pyautogui.hotkey('alt', 'q')
        放虫(window, 任务)
    if('虫' in 任务 and '发现' in 任务):
        pyautogui.hotkey('alt', 'q')
        杀虫(window, 任务)
    if('找' in 任务 and '迷幻妖' in 任务):
        找迷幻妖(window, 任务)
    if('巧' in 任务):
        找巧智(window, 任务)
    if('使用' in 任务 and '招魂' in 任务):
        pyautogui.hotkey('alt', 'q')
        使用招魂(window, 任务)
    if('梦' in 任务):
        找梦魔(window, 任务)


def 找梦魔(window, 任务):
    point = window.F_窗口内查找图片('all-ld-mym.png')
    if point != None:
        ret = window.F_获取任务位置和坐标(任务)
        window.F_智能导航(ret[0])
        window.F_游戏光标移动到(point[0] + 10, point[1] + 5, 手指操作模式=True)
        window.utils.click()
        window.utils.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'q')
        window.F_等待人物停止移动()
        PlaySound("C:\\y913.wav", flags=1)
        window.F_铃铛自动战斗()


def 使用招魂(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_智能导航(ret[0], point = ret[1])
    window.F_小地图寻路(ret[1], True)
    pyautogui.hotkey('alt', 'h')
    pyautogui.hotkey('alt', 'e')
    for i in range(3):
        point = window.F_窗口内查找图片('all_ld_zht.png')
        if point != None:
            window.F_游戏光标移动到(point[0], point[1])
            window.utils.rightClick()
            pyautogui.hotkey('alt', 'e')
            break
    time.sleep(5)
    window.utils.click()
    time.sleep(1)
    PlaySound("C:\\y913.wav", flags=1)
    window.F_铃铛自动战斗()


def 找巧智(window, 任务):
    point = window.F_窗口内查找图片('all-ld-qzm.png')
    if point != None:
        ret = window.F_获取任务位置和坐标(任务)
        window.F_智能导航(ret[0])
        window.F_游戏光标移动到(point[0] + 10, point[1] + 5, 手指操作模式=True)
        window.utils.click()
        window.utils.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'q')
        window.F_等待人物停止移动()
        pyautogui.hotkey('alt', 'h')
        time.sleep(0.5)
        time.sleep(1)
        point = window.F_窗口内查找图片('mh_lingdan_qiaozhimo.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 15, point[1] + 5)
            window.utils.click()
            window.utils.click()
            PlaySound("C:\\y913.wav", flags=1)
            window.F_铃铛自动战斗()
        window.utils.click()
       


def 找怯弱妖(window, 任务):
    point = window.F_窗口内查找图片('all-ld-qry.png')
    print(point)
    if point != None:
        ret = window.F_获取任务位置和坐标(任务)
        window.F_智能导航(ret[0])
        window.F_游戏光标移动到(point[0] + 10, point[1] + 5, 手指操作模式=True)
        window.utils.click()
        window.utils.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'q')
        window.F_等待人物停止移动()
        pyautogui.hotkey('alt', 'h')
        time.sleep(1)
        point = window.F_窗口内查找图片('mh_lingdan_qieluoyao.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 15, point[1] + 5)
            window.utils.click()
            window.utils.click()
            PlaySound("C:\\y913.wav", flags=1)
            window.F_铃铛自动战斗()
        window.utils.click()
            


def 找迷幻妖(window, 任务):
    point = window.F_窗口内查找图片('all-ld-mhy.png')
    if point != None:
        ret = window.F_获取任务位置和坐标(任务)
        window.F_智能导航(ret[0])
        window.F_游戏光标移动到(point[0] + 10, point[1] + 5, 手指操作模式=True)
        window.utils.click()
        window.utils.click()
        time.sleep(1)
        pyautogui.hotkey('alt', 'q')
        window.F_等待人物停止移动()
        pyautogui.hotkey('alt', 'h')
        time.sleep(1)
        PlaySound("C:\\y913.wav", flags=1)
        # window.F_点击战斗(True)
        # time.sleep(1)
        # window.F_游戏光标移动到(275, 340)
        # time.sleep(3)
        # window.utils.click()
        # time.sleep(0.5)
        window.F_铃铛自动战斗()
        window.utils.click()


def 杀虫(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_小地图寻路(ret[1], None)
    time.sleep(0.5)
    PlaySound("C:\\y913.wav", flags=1)
    window.F_铃铛自动战斗()
    window.utils.click()


def 放虫(window, 任务):
    ret = window.F_获取任务位置和坐标(任务)
    window.F_智能导航(ret[0], point=ret[1])
    window.F_小地图寻路(ret[1], True)
    pyautogui.hotkey('alt', 'h')
    pyautogui.hotkey('alt', 'e')
    for i in range(3):
        point = window.F_窗口内查找图片('all-chong.png')
        if point != None:
            window.F_游戏光标移动到(point[0], point[1])
            window.utils.rightClick()
            pyautogui.hotkey('alt', 'e')
            time.sleep(2)
            
            window.utils.click()
            return


if __name__ == '__main__':
    print('F_领取铃铛任务')
    铃铛()
