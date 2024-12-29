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


def 女魃战斗(window):
    if(window.F_是否在战斗()):
        回合数 = 1
        print('进入战斗')
        while(True):
            
            point = window.F_窗口内查找图片('window_zidong2.png')
            if(point):
                print('开始自动操作')
                if(回合数 == 1):
                    pyautogui.press('f5')
                    pyautogui.hotkey('alt', 'q')
                    pass
                else:
                    pyautogui.hotkey('alt', 'q')
                    pyautogui.hotkey('alt', 'q')
                    pass
                回合数 = 回合数 + 1
            if(window.F_是否结束战斗()):
                break
            time.sleep(0.1)
    return True

def F_做任务(window):
    global 是否刚战斗
    任务 = ''
    if(是否刚战斗 == True):
        F_领取任务(window)
        任务 = F_识别任务(window)
        pyautogui.hotkey('alt', 'q')
    else:
        任务 = F_识别任务(window)
        pyautogui.hotkey('alt', 'q')
        if(任务==""):
            F_领取任务(window)
            是否刚战斗 = False
            return
    是否刚战斗 = False 
    if('奇遇' in 任务):
        messagebox.showinfo('严重错误', '奇遇')
        sys.exit()
        
    if('咬金' in 任务):
        window.F_使用道具('daoju_xfxq_yello.png')
        window.F_游戏光标移动到(198, 335)
        window.utils.click()
        window.F_关闭道具()
        window.F_游戏光标移动到(238, 70)
        window.utils.click()
        time.sleep(1)
        window.F_游戏光标移动到(693, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
        window.F_游戏光标移动到(250, 407)
        window.utils.click()
        time.sleep(2)
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
        window.F_游戏光标移动到(393, 403)
        window.utils.click()

    if('地府' in 任务):
        window.F_使用飞行旗('长安城', '驿站', 是否检验坐标=False)
        window.F_导航到地府()
        window.F_游戏光标移动到(678, 179, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
       
        point = window.F_窗口内查找图片('window_duihua_jnh.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 10, point[1] + 2)
            window.utils.click()
        window.F_游戏光标移动到(197, 352)
        window.utils.click()
        time.sleep(2)

        while True:
           
            if(女魃战斗(window)):
                是否刚战斗 = True
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    if('宝象国' in 任务):
        window.F_使用飞行旗('宝象国', '飞行符传送点', 是否检验坐标=False)
        window.F_游戏光标移动到(698, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
        window.F_游戏光标移动到(197, 352)
        window.utils.click()
        time.sleep(2)
        while True:
            
            if(女魃战斗(window)):
                是否刚战斗 = True
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    if('空度' in 任务):
        window.F_导航到化生寺()
        window.F_游戏光标移动到(693, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
        window.F_游戏光标移动到(250, 407)
        window.utils.click()
        time.sleep(2)
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    if('普陀山' in 任务):
        window.F_使用飞行旗('长安城', '大唐国境', 是否检验坐标=False)
        window.F_关闭道具()
        window.F_导航到普陀山()
        window.F_游戏光标移动到(702, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
        window.F_游戏光标移动到(197, 350)
        window.utils.click()
        time.sleep(2)
        while True:
            
            if(女魃战斗(window)):
                是否刚战斗 = True
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
        time.sleep(0.1)
        window.utils.click()




            
    if('奇怪的章鱼' in 任务):
        window.F_使用飞行符('建邺城')
        window.F_游戏光标移动到(650, 175)
        window.F_游戏光标移动到(692, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(196, 338)
        window.utils.click()
        window.F_游戏光标移动到(197, 352)
        window.utils.click()
        time.sleep(2)
        while True:
            time.sleep(1)
            if(window.F_是否在战斗()):
                是否刚战斗 = True
            if(女魃战斗(window)):
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    if('长寿郊外' in 任务):
        window.F_导航到长寿郊外()
        window.F_游戏光标移动到(722, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()

        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        point = window.F_窗口内查找图片('window_duihua_jnh.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 10, point[1] + 2)
            window.utils.click()
        window.F_游戏光标移动到(228, 335)
        window.utils.click()
        time.sleep(2)
        while True:
            time.sleep(1)
            if(window.F_是否在战斗()):
                是否刚战斗 = True
            if(女魃战斗(window)):
              
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    if('狮驼岭' in 任务):
        window.F_导航到狮驼岭()
        window.F_游戏光标移动到(707, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        point = window.F_窗口内查找图片('window_duihua_jnh.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 10, point[1] + 2)
            window.utils.click()
        window.F_游戏光标移动到(197, 352)
        window.utils.click()
        time.sleep(2)
        while True:
            time.sleep(1)
            if(window.F_是否在战斗()):
                是否刚战斗 = True
            if(女魃战斗(window)):
              
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()

    if('江南野外' in 任务):
        window.F_使用飞行旗('长安城', '江南野外', 是否检验坐标=False)
        window.F_导航到江南野外()
        window.F_游戏光标移动到(707, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        point = window.F_窗口内查找图片('window_duihua_jnh.png')
        if point != None:
            window.F_游戏光标移动到(point[0] + 10, point[1] + 2)
            window.utils.click()
        window.F_游戏光标移动到(197, 331)
        window.utils.click()
        time.sleep(2)
        while True:
            time.sleep(1)
            if(window.F_是否在战斗()):
                是否刚战斗 = True
            if(女魃战斗(window)):
              
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    
    if('庆典舞者' in 任务):
        window.F_游戏光标移动到(701, 175, 手指操作模式=True)
        window.utils.doubleClick()
        time.sleep(2)
        window.utils.doubleClick()
        window.F_鼠标移动到窗口中心()
        window.F_等待人物停止移动()
        window.F_游戏光标移动到(200, 331)
        window.utils.click()
        time.sleep(2)
        while True:
            time.sleep(1)
            if(window.F_是否在战斗()):
                是否刚战斗 = True
            if(女魃战斗(window)):
                
                break
        window.F_游戏光标移动到(393, 403)
        window.utils.click()
    


def F_识别任务(window):
    pyautogui.hotkey('alt', 'q')
    time.sleep(0.5)
    任务 = window.F_识别自定义任务()
    print(任务)
    if(任务 == ""):
        print('未识别到任务')
    return 任务

def F_领取任务(window):
    print('F_领取任务')
    window.F_使用道具('daoju_xfxq_red.png')
    window.F_游戏光标移动到(198, 335)
    window.utils.click()
    window.F_关闭道具()
    window.F_游戏光标移动到(244, 285)
    window.utils.click()
    window.F_游戏光标移动到(231, 322)
    window.utils.click()
    time.sleep(1)
    window.utils.click()

window = mhWindow.MHWindow()
while True:
    time.sleep(1)
    if(女魃战斗(window)):
        break
while True:
    F_做任务(window)

