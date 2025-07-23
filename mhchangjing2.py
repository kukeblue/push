from telnetlib import theNULL
from tkinter import N, NO
import mhWindow
import sys
import io
import time
import pyautogui
from Images.index import IMAGES
import utils
from tkinter import messagebox

projectPath = utils.projectPath

是否刚战斗 = False


window = mhWindow.MHWindow()
POINT = [[21,130], [168,18], [171, 129], [24,19]]  # 小地图寻路坐标
while True:
    for i in POINT:
        window.F_小地图寻路(i, 检查是否到达指定坐标=False)
        window.F_等待人物停止移动()
        if(window.F_是否在战斗()):
            while True:
                time.sleep(0.1)
                if(window.F_是否结束战斗()):
                    break
    

