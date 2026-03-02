import pyautogui
import keyboard
import time
import mhWindow
import win32gui
import win32con
import win32api
import ctypes
from ctypes import wintypes
import mouse


window = mhWindow.MHWindow()
while True:
    ret =  window.F_窗口内查找图片('huahun.png')
    ret2 =  window.F_窗口内查找图片('huahun2.png')
    ret3 =  window.F_窗口内查找图片('huahun3.png')
    if(ret3): 
        print('找到画魂3')
        break
    if(ret2): 
        print('找到画魂2')
        break
    if(ret): 
        print('找到画魂')
        break
    ret = window.F_获取当前场景文字()
    if('宝宝' in ret):
        print('找到宝宝')
        break
