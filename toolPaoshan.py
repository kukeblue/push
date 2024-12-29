from telnetlib import theNULL
from tkinter import N, NO
import mhWindow
import utils
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import  QFrame, QLineEdit, QMainWindow, QLabel, QCheckBox, QPushButton, QApplication
import threading
import pyautogui
import string
import ctypes 
import time 

from winsound import PlaySound
projectPath = mhWindow.projectPath



def 判断人物是否停止(window):
    colors = None
    for i in range(60):
        time.sleep(1)
        x = window.GameWindowArea[0] + 31  # 位置的X坐标
        y = window.GameWindowArea[1] + 77  # 位置的Y坐标
        color = pyautogui.pixel(int(x), int(y))


        x = window.GameWindowArea[0] + 674  # 位置的X坐标
        y = window.GameWindowArea[1] + 52  # 位置的Y坐标
        color2 = pyautogui.pixel(int(x), int(y))

        x = window.GameWindowArea[0] + 13  # 位置的X坐标
        y = window.GameWindowArea[1] + 558  # 位置的Y坐标
        color3 = pyautogui.pixel(int(x), int(y))

        x = window.GameWindowArea[0] + 784  # 位置的X坐标
        y = window.GameWindowArea[1] + 535  # 位置的Y坐标
        color4 = pyautogui.pixel(int(x), int(y))
        new_colors = [color, color2, color3, color4]
        if(colors != None):
            count = 0
            for i in range(4):
                if(new_colors[i] == colors[i]):
                    count = count + 1
            if(count > 1):
                print('寻路停止')
                break
            else:
                colors = new_colors 
        else:
            colors = new_colors

def 回到帮派(window):
    global ProgramSwitch
    for x in range(5):
        if(ProgramSwitch == False):
            break
        当前所在地图 = window.F_获取当前地图()
        if(当前所在地图 == '长安城'):
            window.F_小地图寻路([390, 269])
            PlaySound(projectPath + "\\" + "y1954.wav", flags=1)
            break;
        if(当前所在地图 == '北俱芦洲'):
            window.F_小地图寻路([51, 117], 是否等待人物停止移动=False, 检查是否到达指定坐标=False)
            判断人物是否停止(window)
            window.F_游戏光标移动到(316, 220)
            window.utils.click()
            time.sleep(1)
            if(window.F_窗口内查找图片('window_goto.png')):
                window.F_游戏光标移动到(191, 338)
                window.utils.click()
                time.sleep(2)
        elif(当前所在地图 == '地府'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(422, 342)
            window.utils.click()
            window.F_小地图寻路([102, 53], 检查是否到达指定坐标=False)
            判断人物是否停止(window)
            window.F_游戏光标移动到(447, 198)
            window.utils.click()
            time.sleep(2)
            window.F_游戏光标移动到(242, 227)
            window.utils.click()
            time.sleep(1)
            window.F_游戏光标移动到(168, 335)
            time.sleep(1)
            window.utils.click()
            time.sleep(3)

def 跑商到北俱(window):
    print('跑商到北具')
    global ProgramSwitch
    while ProgramSwitch:
        当前所在地图 = window.F_获取当前地图()
        if(当前所在地图 == '北俱芦洲'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(435, 262)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            PlaySound(projectPath + "\\" + "y1954.wav", flags=1)
            time.sleep(10)
            break
        elif(当前所在地图 == '地府'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(527, 449)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            判断人物是否停止(window)
            window.F_游戏光标移动到(701, 507)
            time.sleep
            window.utils.click()
            time.sleep(3)
        elif(当前所在地图 == '长安城'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(664, 434)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            window.F_等待人物停止移动()
            window.F_游戏光标移动到(716, 406)
            window.utils.click()
            time.sleep(2)
        elif(当前所在地图 == '江南野外'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(528, 335)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            判断人物是否停止(window)
            window.F_游戏光标移动到(719, 189)
            window.utils.click()
            time.sleep(2)
        elif(当前所在地图 == '建邺城'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(651, 382)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            判断人物是否停止(window)
            window.F_游戏光标移动到(627, 336)
            window.utils.click()
            time.sleep(3)
        elif(当前所在地图 == '傲来国'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(556, 193)
            window.utils.click()
            window.utils.click()
            time.sleep(0.5)
            pyautogui.press('tab')
            判断人物是否停止(window)
            window.F_游戏光标移动到(674, 85)
            window.utils.click()
            time.sleep(2)
        elif(当前所在地图 == '花果山'):
            # pyautogui.press('tab')
            # window.F_游戏光标移动到(235, 219)
            # window.utils.click()
            # window.utils.click()
            # time.sleep(0.5)
            # pyautogui.press('tab')
            window.F_点击小地图出入口按钮()
            window.F_小地图寻路([23, 101], 检查是否到达指定坐标=False, 是否关闭出入口=False, 是否等待人物停止移动=False)
            判断人物是否停止(window)
            pyautogui.press('f9')
            window.F_点击小地图出入口按钮()
            window.F_游戏光标移动到(492, 346)
            window.utils.click()
            time.sleep(1)
            if(window.F_窗口内查找图片('window_goto.png')):
                window.F_游戏光标移动到(191, 338)
                window.utils.click()
                time.sleep(2)
        elif(当前所在地图 == '东海湾'):
            window.F_小地图寻路([70, 15], 检查是否到达指定坐标=False, 是否关闭出入口=True)
            time.sleep(7)  
            window.F_点击小地图出入口按钮()
            while True:
                ret = window.F_点击傲来驿站老板()
                if(ret):
                    break
                window.F_小地图寻路([70, 15], 检查是否到达指定坐标=False)
                
        elif(当前所在地图 == '大唐国境'):
            window.F_小地图寻路([86, 250], 检查是否到达指定坐标=False)
            判断人物是否停止(window)
            pyautogui.press('f9')
            window.F_游戏光标移动到(419, 267)
            window.utils.click()
            window.utils.click()
            if(window.F_窗口内查找图片('window_goto.png')):
                window.F_游戏光标移动到(191, 338)
                window.utils.click()
                time.sleep(2)
      


def 跑商到地府(window):
    global ProgramSwitch
    while ProgramSwitch:
        当前所在地图 = window.F_获取当前地图()
        print(当前所在地图)
        if(当前所在地图 == '地府'):
            PlaySound(projectPath + "\\" + "y1954.wav", flags=1)
            window.F_小地图寻路([81, 7], 检查是否到达指定坐标=False)
            break
        elif(当前所在地图 == '北俱芦洲'):
            window.F_小地图寻路([51, 117], 检查是否到达指定坐标=False)
            判断人物是否停止(window)
            window.F_游戏光标移动到(316, 220)
            window.utils.click()
            time.sleep(1)
            if(window.F_窗口内查找图片('window_goto.png')):
                window.F_游戏光标移动到(191, 338)
                window.utils.click()
                time.sleep(2)
        elif(当前所在地图 == '长安城'):
            window.F_导航到大唐国境2()
        elif(当前所在地图 == '大唐国境'):
            pyautogui.press('tab')
            window.F_游戏光标移动到(224, 144)
            window.utils.click()
            window.F_小地图寻路([48, 325], 检查是否到达指定坐标=False)
            判断人物是否停止(window)
            window.F_游戏光标移动到(370, 58)
            window.utils.click()
            time.sleep(2)
            # window.F_导航到地府()


ProgramSwitch = False  # 程序开关
goDifu = False   # 去地府
goBeiju = False  # 去北具
goBangpai = False  # 去帮派


def F_启动进程(app):
    window = mhWindow.MHWindow()
    if(window.GameWindowArea[0] == 0 ):
        app.statusBar().showMessage('读取窗口失败，请关闭软件')
        return 
    global ProgramSwitch
    global goDifu
    global goBeiju
    global goBangpai
    while True:
        if(ProgramSwitch == True):
            app.statusBar().showMessage('程序运行中')
        else:
            app.statusBar().showMessage('程序未开启')
        time.sleep(1)
        if(ProgramSwitch):
            if(goDifu == True):
                app.statusBar().showMessage('开始去地府')
                time.sleep(1)
                goDifu = False
                跑商到地府(window)
            elif(goBeiju == True):
                app.statusBar().showMessage('开始去北俱')
                time.sleep(1)
                goBeiju = False
                跑商到北俱(window)
            elif(goBangpai == True):
                app.statusBar().showMessage('开始去帮派')
                time.sleep(1)
                goBangpai = False
                回到帮派(window)
        else:
            goDifu = False 
            goBeiju = False
            goBangpai = False


    app.statusBar().showMessage('线程关闭成功')



class Main(QMainWindow):
    
    # ButtonProgramSwitch = None # 程序开关按钮
    # option1 = "f3"               # 第一回合操作
    # option1Path = "275,134"           # 第一回合操作位置
    # option2 = "f5"               # 第二回合操作
    # option2Path = "275,134"           # 第二回合操作位置
    # zgMode = 2
    # hhMode = 0
    isInit = False

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def onClickButtonProgramSwitch(self):
        if(self.isInit):
            self.statusBar().showMessage('请关闭后再重新读取')
            return 
        self.isInit = True
        self.statusBar().showMessage('读取窗口中...')
        t = threading.Thread(target=F_启动进程, args=[self])
        t.start()

    def onClickButtonGoDifu(self):
        global goDifu
        print('点击程序开关')
        if(goDifu == False):
            goDifu = True
            self.statusBar().showMessage('去地府')
        else:
            self.statusBar().showMessage('去地府')
    
    def onClickButtonGoBeiju(self):
        global goBeiju
        print('点击程序开关')
        if(goBeiju == False):
            goBeiju = True
            self.statusBar().showMessage('去北俱')
        else:
            self.statusBar().showMessage('去北俱')
    
    def onClickButtonGoBangpai(self):
        global goBangpai
        print('点击程序开关')
        if(goBangpai == False):
            goBangpai = True
            self.statusBar().showMessage('去帮派')
        else:
            self.statusBar().showMessage('去帮派')
           
    
    def onClickButtonStart(self):
        global ProgramSwitch
        print('点击程序开关')
        if(ProgramSwitch == False):
            ProgramSwitch = True
            self.ButtonProgramSwitch.setText("关闭")
            self.statusBar().showMessage('正在开启脚本...')
        else:
            self.ButtonProgramSwitch.setText("开启")
            self.statusBar().showMessage('正在关闭脚本...')
            ProgramSwitch = False
    
    def initUI(self):

        self.ButtonProgramSwitch = QPushButton("读取窗口", self)
        self.ButtonProgramSwitch.move(10, 10)
        self.ButtonProgramSwitch.clicked.connect(self.onClickButtonProgramSwitch)

        # 程序开关
        self.ButtonProgramSwitch = QPushButton("开启", self)
        self.ButtonProgramSwitch.move(120, 10)
        self.ButtonProgramSwitch.clicked.connect(self.onClickButtonStart)

        self.ButtonDifu = QPushButton("到地府", self)
        self.ButtonDifu.move(10, 60)
        self.ButtonDifu.setIconSize(QSize(16, 16))
        self.ButtonDifu.setStyleSheet(
            """
            QPushButton {
                background-color: #5d5cde;  /* 设置背景色 */
                color: white;  /* 设置文本颜色 */
                border-radius: 5px;  /* 设置圆角 */
                padding: 8px;  /* 设置内边距 */
            }
            QPushButton:hover {
                background-color: #d2d2fe;  /* 设置背景色 */
            }
            """
        )
        self.ButtonDifu.clicked.connect(self.onClickButtonGoDifu)

        self.ButtonBeiju = QPushButton("到北俱", self)
        self.ButtonBeiju.move(10, 100)
        self.ButtonBeiju.setIconSize(QSize(16, 16))
        self.ButtonBeiju.setStyleSheet(
            """
            QPushButton {
                background-color: #1677ff;  /* 设置背景色 */
                color: white;  /* 设置文本颜色 */
                border-radius: 5px;  /* 设置圆角 */
                padding: 8px;  /* 设置内边距 */
            }
            QPushButton:hover {
                background-color: #4096ff;  /* 鼠标悬停时的背景色 */
            }
            """
        )
        self.ButtonBeiju.clicked.connect(self.onClickButtonGoBeiju)
        

        self.ButtonBangpai = QPushButton("回帮派", self)
        self.ButtonBangpai.move(10, 140)
        self.ButtonBangpai.setIconSize(QSize(16, 16))
        self.ButtonBangpai.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;  /* 设置背景色 */
                color: white;  /* 设置文本颜色 */
                border-radius: 5px;  /* 设置圆角 */
                padding: 8px;  /* 设置内边距 */
            }
            QPushButton:hover {
                background-color: #45a049;  /* 鼠标悬停时的背景色 */
            }
            """
        )
        self.ButtonBangpai.clicked.connect(self.onClickButtonGoBangpai)

        # # 创建一个标签
        # QLabel("第一回合:", self).move(10, 50)
        # # # 设置第一回合操作
        # firstOptionInput = QLineEdit(self)
        # firstOptionInput.move(80, 50)
        # firstOptionInput.setPlaceholderText("请输入回合操作")
        # firstOptionInput.setFixedWidth(50)
        # firstOptionInput.setText(self.option1)
        # firstOptionInput.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option1'))
        # # 设置第一回合操作位置
        # firstOptionInputPath = QLineEdit(self)
        # firstOptionInputPath.move(140, 50)
        # firstOptionInputPath.setPlaceholderText("操作位置")
        # firstOptionInputPath.setFixedWidth(70)
        # firstOptionInputPath.setText(self.option1Path)
        # firstOptionInputPath.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option1Path'))


        # QLabel("第二回合:", self).move(10, 90)
        # # # 设置第一回合操作
        # secondOptionInput = QLineEdit(self)
        # secondOptionInput.move(80, 90)
        # secondOptionInput.setPlaceholderText("请输入回合操作")
        # secondOptionInput.setFixedWidth(50)
        # secondOptionInput.setText(self.option2)
        # secondOptionInput.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option2'))
        # # 设置第一回合操作位置
        # secondOptionInputPath = QLineEdit(self)
        # secondOptionInputPath.move(140, 90)
        # secondOptionInputPath.setPlaceholderText("操作位置")
        # secondOptionInputPath.setFixedWidth(70)
        # secondOptionInputPath.setText(self.option2Path)
        # secondOptionInputPath.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option2Path'))
        
        # cb = QCheckBox('抓鬼模式', self)
        # cb.move(10, 130)
        # cb.stateChanged.connect(lambda text: self.onOptionInputChange(text, type='zgMode'))
        # cb.toggle()

        # cb = QCheckBox('自动喊话', self)
        # cb.move(100, 130)
        # cb.stateChanged.connect(lambda text: self.onOptionInputChange(text, type='hhMode'))
        self.statusBar().showMessage('脚本初始化完成')
        self.setGeometry(300, 300, 260, 320)
        self.setWindowTitle('驱动大师')
        self.show()

def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
    # window = mhWindow.MHWindow()
    # time.sleep(3)
    # 回到帮派(window)
    # 判断人物是否停止(window)
    # while True:
    #     price_str = input("输入1继续：")
    #     time.sleep(3)
    #     if(price_str == '1'):
    #         回到帮派(window)
    #     elif(price_str == '2'):
    #         跑商到北具(window)
    #     else:
    #         跑商到地府(window)