from telnetlib import theNULL
from tkinter import N, NO
import mhWindow
import sys
import io
import time
import pyautogui
from Images.index import IMAGES
import utils
import math
projectPath = utils.projectPath


def is_distance_greater_than_100(x1, y1, x2, y2):
    # 计算直线距离
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # 判断距离是否大于100
    if distance > 200:
        return False
    else:
        return True
    
def 识别任务(window):
    window.F_关闭对话()
    pyautogui.hotkey('alt', 'q')
    time.sleep(0.5)
    ret = window.F_识别自定义任务()
    pyautogui.hotkey('alt', 'q')
    if('挖宝' in ret):
        print('读取自定任务:' + ret)
        ret = window.F_获取任务位置和坐标(ret)
        window.F_智能导航(ret[0], point = ret[1])
        window.F_小地图寻路(ret[1], 检查是否到达指定坐标=False)
        window.F_点击战斗2()
        window.F_点击主怪自动战斗('f5', 是否关闭对话框=False)
        time.sleep(0.5)
        if(window.F_关闭对话()):
            window.F_error()
            window.F_抓鬼自动战斗()
        return ret


    

def 领任务(window):
    window.F_使用飞行旗('长安城', '酒店', 是否检验坐标=False)
    window.F_游戏光标移动到(530,138)
    window.utils.click()
    window.utils.click()
    time.sleep(2)
    pyautogui.press('f9')
    for p in range(100):
        for i in range(1, 12):
            print('find i', i)
            point = window.F_窗口内查找图片(f'datu_xiaoer{i}.png', confidence=0.8)
            if(point):
                if(point[0] > 400):
                    pianyi = -50
                else:
                    pianyi = 80
                
                if(point[1] > 300):
                    pianyi2 = 50
                else:
                    pianyi2 = -50

                print('找到店小二')
                s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point  == None):
                    s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point  == None):
                    s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point  == None):
                    s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point  == None):
                    s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point  == None):
                    s_point = window.F_窗口内查找图片(IMAGES['狮子队标'], confidence=0.95)
                if(s_point):
                    if(s_point and is_distance_greater_than_100(point[0], point[1], s_point[0], s_point[1] + 80)):
                        window.F_游戏光标移动到(point[0] + 10, point[1] - 10)
                        window.utils.click()
                        window.utils.click()
                        window.utils.click()
                        point = window.F_窗口内查找图片(f'datu_renwu_tingting.png', confidence=0.75)
                        if(point):
                            window.F_游戏光标移动到(point[0] + 20, point[1] + 7)
                            window.utils.click()
                            window.utils.click()
                            window.utils.click()

                            point = window.F_窗口内查找图片(f'datu_renwu_tingting.png', confidence=0.75)
                            if(point):
                                window.F_游戏光标移动到(189, 356)
                                window.utils.click()
                                window.utils.click()
                                window.utils.click()
                            return
                        else:
                            ret = window.utils.findPicture(IMAGES["游戏窗口左上角"])
                            if(ret == None):
                                window.F_error()
                                sys.exit()
                            window.F_鼠标移动到窗口中心()
                    else:
                        print('狮子头距离不够！！！！')
                        window.F_游戏光标移动到(point[0] + pianyi, point[1] - pianyi2)
                        window.utils.click()
                        time.sleep(3)
                        pyautogui.press('f9')
                else:
                    print('狮子头找不到！！！！')
                    window.F_游戏光标移动到(point[0] + pianyi, point[1] - pianyi2)
                    window.utils.click()
                    time.sleep(3)
                    pyautogui.press('f9')

                    
                break
        if(p == 0):
            window.F_游戏光标移动到(514, 293)
            window.utils.click()
            time.sleep(3)
            pyautogui.press('f9')
        else:
            window.F_鼠标移动到窗口中心()

def start():            
    window = mhWindow.MHWindow()
    while True:     
        识别任务(window)   
        领任务(window)
  






