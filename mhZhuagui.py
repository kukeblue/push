from telnetlib import theNULL
from tkinter import N, NO
import mhWindow
import sys
import io
import time
import pyautogui
from Images.index import IMAGES
import utils
projectPath = utils.projectPath


def F_识别抓鬼任务(window):
        point = window.F_窗口内查找图片(IMAGES['游戏窗口任务追踪'], area=[773, 106, 33, 37])
        if(point == None):
            pyautogui.hotkey('alt', 'q')
            window.F_游戏光标移动到(178, 341)
            window.utils.click()
            pyautogui.hotkey('alt', 'q')
            time.sleep(1.5)
        window.F_使用道具('daoju_yan.png')
        window.F_关闭道具()
        
        print('识别抓鬼任务')
        area = [window.GameWindowArea[0] + 630, window.GameWindowArea[1] + 110, window.GameWindowArea[0] + 640 + 163, window.GameWindowArea[1] + 110 + 233]
        print(area)
        data = {
            '鬼王': None,
            '捉鬼': None,
        }
        print('检查是否有鬼王任务')
        window.utils.op.SetDict(0, projectPath + "\\fonts\\" + "renwu_green.txt")
         # zhuoWang - 鬼王
        ret = window.utils.op.FindStr(area[0], area[1], area[2], area[3], 'guiWang', "00ff00-000000", 0.7)
        print(ret[0])
        if(ret[0] > -1):
            print('识别到鬼王任务')
            data['鬼王'] = True
        else:
            print('未识别到鬼王任务')
        # zhuoGui - 捉鬼
        ret = window.utils.op.FindStr(area[0], area[1], area[2], area[3],'zhuoGui', "00ff00-000000", 0.7)
        if(ret[0] > -1):
            print('识别到小鬼任务')
            data['捉鬼'] = [ret[1]-20, ret[2]-20, 183, 110]
        else:
            print('未识别到小鬼任务')
            
        if(data['捉鬼'] != None):
            print('????????')
            text = window.utils.baidu通用文字识别(data['捉鬼'])
            data['捉鬼'] = text
            print('INFO: 识别到抓鬼任务')
            print(text)
        return data

def F_领取大鬼任务(window):
    pyautogui.press('tab')
    window.F_游戏光标移动到(422, 342)
    window.utils.click()
    window.F_小地图寻路([102, 53], 是否等待人物停止移动=False)
    # 点击钟馗
    window.F_游戏光标移动到(447, 198)
    window.F_等待人物停止移动() 
    window.utils.click()
    time.sleep(1)
    pyautogui.press('f9')
    window.F_游戏光标移动到(546, 190)
    window.utils.click()
    time.sleep(0.5)
    point = window.F_窗口内查找图片('renwu_zhuagui_dagui.png')
    if(point):
        window.F_游戏光标移动到(373, point[1] + 2)
        window.utils.click()
        time.sleep(0.5)
        window.utils.click()
    window.F_游戏光标移动到(373, 508)
    window.utils.click()
    time.sleep(1)
    if(window.F_获取当前地图() == '地府'):
        return
    else:
        point = window.F_窗口内查找图片('renwu_zhuagui_dagui.png')
        if(point):
            window.F_游戏光标移动到(point[0], point[1] + 2)
            window.utils.click()
            time.sleep(1)
            window.utils.click()
        window.F_关闭对话()
        window.F_游戏光标移动到(373, 508)
        window.utils.click()
        time.sleep(2)
        window.F_游戏光标移动到(373, 508)
        window.utils.click()
        time.sleep(2)
        window.utils.click()

def F_领取钟馗任务(window):
    pyautogui.press('tab')
    window.F_游戏光标移动到(265, 323)
    window.utils.click()
    point = window.F_窗口内查找图片(IMAGES['游戏窗口任务追踪'], area=[773, 106, 33, 37])
    if(point == None):
        pyautogui.hotkey('alt', 'q')
        window.F_游戏光标移动到(178, 341)
        window.utils.click()
        pyautogui.hotkey('alt', 'q')
        time.sleep(1.5)

    window.F_打开道具()
    window.F_游戏光标移动到(269, 318)
    window.utils.rightClick()
    window.F_关闭道具()
    
    # window.F_游戏光标移动到(643, 20)
    # window.utils.rightClick()
    # pyautogui.press('tab')
    for i in range(3):
        window.F_小地图寻路([52, 51], 是否等待人物停止移动=False)
        # 点击钟馗
        window.F_游戏光标移动到(244, 173)
        window.F_等待人物停止移动() 
        window.utils.click()
        pyautogui.click()
        point = window.F_窗口内查找图片('renwu_zhuagui_haode.png')
        if(point):
            window.F_游戏光标移动到(point[0], point[1])
            window.utils.click()
            time.sleep(1)
            window.utils.click()
            point = window.F_窗口内查找图片('renwu_zhuagui_haode.png')
            if(point):
                pass
            else:
                break
   


def F_开关追踪(window):
    pyautogui.hotkey('alt', 'q')
    window.F_游戏光标移动到(178, 341)
    window.utils.click()
    pyautogui.hotkey('alt', 'q')

def F_去抓鬼(window, ret, 是否是大鬼=True):
    window.F_智能导航(ret[0], point = ret[1])
    window.F_小地图寻路(ret[1], 检查是否到达指定坐标=False)
    # window.F_等待人物停止移动() 
    if(是否是大鬼):
        window.F_点击战斗()
        window.F_点击主怪自动战斗()
        # window.F_点击主怪自动战斗('f5')
    else:
        window.F_点击战斗()
        # window.F_点击主怪自动战斗()
        window.F_点击主怪自动战斗('f5')
    time.sleep(0.5)
    window.F_关闭对话()
    


def 抓鬼(window, 是否抓大鬼=True):
    time.sleep(2)
    if(window.F_是否在战斗()):
        time.sleep(1)
        while(True):
            time.sleep(1)
            if(window.F_是否结束战斗()):
                break
    print('F_领取抓鬼任务')
    time.sleep(2)
    while True:
        任务 = F_识别抓鬼任务(window)
        摄药香时间 = window.F_获取当前摄药香时间()
        if(摄药香时间 and int(摄药香时间) < 10):
            window.F_使用道具('daoju_xiang.png')
        if(是否抓大鬼 and 任务['鬼王'] != None):
            pyautogui.hotkey('alt', 'q')
            window.F_游戏光标移动到(178, 341)
            鬼王任务 = window.F_识别自定义任务()
            window.utils.click()
            pyautogui.hotkey('alt', 'q')
            ret = window.F_获取任务位置和坐标(鬼王任务)
            F_去抓鬼(window, ret)
        if(任务['捉鬼'] != None):
            小鬼任务 = 任务['捉鬼']
            ret = window.F_获取任务位置和坐标(小鬼任务)
            F_去抓鬼(window, ret, 是否是大鬼=False)
        window.F_导航到地府()
        if(是否抓大鬼):
            F_领取大鬼任务(window)
            pyautogui.press('f5')
            pyautogui.press('up')
            pyautogui.press('enter')
        F_领取钟馗任务(window)
        


# window = mhWindow.MHWindow()
# 抓鬼(window, True)
