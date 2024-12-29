from telnetlib import theNULL
from tkinter import N, NO
import mhWindow
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QLineEdit, QMainWindow, QLabel, QCheckBox, QPushButton, QApplication
import threading
import pyautogui
import time 
import atexit

from winsound import PlaySound
projectPath = mhWindow.projectPath
exit_event = threading.Event()

ProgramSwitch = False  # 程序开关

def F_启动进程(app):
    window = mhWindow.MHWindow()
    if(window.GameWindowArea[0] == 0 ):
        app.statusBar().showMessage('读取窗口失败，请关闭软件')
        return 
    global ProgramSwitch
    while True:
        app.statusBar().showMessage('程序运行中')
        time.sleep(1)
        第一回合操作 = app.option1.split("+")
        第一回合操作位置 = None
        if(app.option1Path != ''):
            第一回合操作位置 = app.option1Path.split(",")
            第一回合操作位置[0] = int(第一回合操作位置[0])
            第一回合操作位置[1] = int(第一回合操作位置[1])
        
        第二回合操作 = app.option2.split("+")
        第二回合操作位置 = None
        if(app.option2Path != ''):
            第二回合操作位置 = app.option2Path.split(",")
            第二回合操作位置[0] = int(第二回合操作位置[0])
            第二回合操作位置[1] = int(第二回合操作位置[1])
        抓鬼数 = 1
        while ProgramSwitch:
            app.statusBar().showMessage('线程执行中....')
            print('线程执行中....')
            time.sleep(1)
            ret = window.utils.findPicture("window_waring.png", confidence=0.98)
            if(ret):
                print('处理验证')
                window.F_播放铃声('y1954.wav')
                time.sleep(10)
            else:
                print('没有代处理')

            if(window.F_是否在战斗()):
                回合数 = 1
                app.statusBar().showMessage('进入战斗')
                print('进入战斗')
                time.sleep(1)
                while(True and ProgramSwitch == True):
                    time.sleep(1)
                    ret = window.utils.findPicture("window_waring.png", confidence=0.98)
                    if(ret):
                        print('处理验证')
                        window.F_播放铃声('y1954.wav')
                        time.sleep(10)
                    else:
                        print('没有代处理')
                    point = window.F_窗口内查找图片('window_zidong2.png')
                    if(point):
                        app.statusBar().showMessage('开始自动操作')
                        print('开始自动操作')
                        if(app.zgMode != 2):
                            if(回合数 == 1):
                                if(第二回合操作位置 != None):
                                    window.F_游戏光标移动到(第一回合操作位置[0], 第一回合操作位置[1])
                                if(len(第一回合操作) == 1):
                                    pyautogui.press(第一回合操作[0])
                                if(len(第一回合操作) == 2):
                                    pyautogui.hotkey(第一回合操作[0], 第一回合操作[1])
                                
                                    pyautogui.click()
                                    pyautogui.click()
                                pyautogui.hotkey('alt', 'q')
                                pyautogui.hotkey('alt', 'q')
                            elif(回合数 == 2):
                            
                                if(第二回合操作位置 != None):
                                    window.F_游戏光标移动到(第二回合操作位置[0], 第二回合操作位置[1])
                                if(len(第二回合操作) == 1):
                                    pyautogui.press(第一回合操作[0])
                                if(len(第二回合操作) == 2):
                                    pyautogui.hotkey(第二回合操作[0], 第二回合操作[1])
                                    pyautogui.click()
                                    pyautogui.click()
                                pyautogui.hotkey('alt', 'q')
                                pyautogui.hotkey('alt', 'q')
                            else:
                                pyautogui.hotkey('alt', 'q')
                                pyautogui.hotkey('alt', 'q')
                                pyautogui.hotkey('alt', 'q')
                        else:
                            if(回合数 == 1):
                                if(抓鬼数 % 2 == 0):
                                    if(第二回合操作位置 != None):
                                        window.F_游戏光标移动到(第二回合操作位置[0], 第二回合操作位置[1])
                                    if(len(第二回合操作) == 1):
                                        pyautogui.press(第二回合操作[0])
                                    if(len(第二回合操作) == 2):
                                        pyautogui.hotkey(第二回合操作[0], 第二回合操作[1])
                                    
                                else:
                                    if(第一回合操作位置 != None):
                                        window.F_游戏光标移动到(第一回合操作位置[0], 第一回合操作位置[1])
                                    if(len(第一回合操作) == 1):
                                        pyautogui.press(第一回合操作[0])
                                    if(len(第一回合操作) == 2):
                                        pyautogui.hotkey(第一回合操作[0], 第一回合操作[1])
                                
                                pyautogui.click()
                            pyautogui.hotkey('alt', 'q')
                            pyautogui.hotkey('alt', 'q')
                            pyautogui.hotkey('alt', 'q')

                        回合数 = 回合数 + 1
                        if(app.hhMode == 2):
                            pyautogui.press('up')
                            pyautogui.press('enter')
                    if(window.F_是否结束战斗()):
                        抓鬼数 = 抓鬼数 + 1
                        break
        app.statusBar().showMessage('线程关闭成功')


class Main(QMainWindow):
    
    ButtonProgramSwitch = None # 程序开关按钮
    option1 = "f3"               # 第一回合操作
    option1Path = "275,134"           # 第一回合操作位置
    option2 = "f5"               # 第二回合操作
    option2Path = "275,134"           # 第二回合操作位置
    zgMode = 2
    hhMode = 0
    isInit = False

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):

        self.ButtonProgramSwitch = QPushButton("读取窗口", self)
        self.ButtonProgramSwitch.move(10, 10)
        self.ButtonProgramSwitch.clicked.connect(self.onClickButtonProgramSwitch)

        # 程序开关
        self.ButtonProgramSwitch = QPushButton("开启", self)
        self.ButtonProgramSwitch.move(120, 10)
        self.ButtonProgramSwitch.clicked.connect(self.onClickButtonStart)

        # 创建一个标签
        QLabel("第一回合:", self).move(10, 50)
        # # 设置第一回合操作
        firstOptionInput = QLineEdit(self)
        firstOptionInput.move(80, 50)
        firstOptionInput.setPlaceholderText("请输入回合操作")
        firstOptionInput.setFixedWidth(50)
        firstOptionInput.setText(self.option1)
        firstOptionInput.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option1'))
        # 设置第一回合操作位置
        firstOptionInputPath = QLineEdit(self)
        firstOptionInputPath.move(140, 50)
        firstOptionInputPath.setPlaceholderText("操作位置")
        firstOptionInputPath.setFixedWidth(70)
        firstOptionInputPath.setText(self.option1Path)
        firstOptionInputPath.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option1Path'))


        QLabel("第二回合:", self).move(10, 90)
        # # 设置第一回合操作
        secondOptionInput = QLineEdit(self)
        secondOptionInput.move(80, 90)
        secondOptionInput.setPlaceholderText("请输入回合操作")
        secondOptionInput.setFixedWidth(50)
        secondOptionInput.setText(self.option2)
        secondOptionInput.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option2'))
        # 设置第一回合操作位置
        secondOptionInputPath = QLineEdit(self)
        secondOptionInputPath.move(140, 90)
        secondOptionInputPath.setPlaceholderText("操作位置")
        secondOptionInputPath.setFixedWidth(70)
        secondOptionInputPath.setText(self.option2Path)
        secondOptionInputPath.textChanged.connect(lambda text: self.onOptionInputChange(text, type='option2Path'))
        
        cb = QCheckBox('抓鬼模式', self)
        cb.move(10, 130)
        cb.stateChanged.connect(lambda text: self.onOptionInputChange(text, type='zgMode'))
        cb.toggle()

        cb = QCheckBox('自动喊话', self)
        cb.move(100, 130)
        cb.stateChanged.connect(lambda text: self.onOptionInputChange(text, type='hhMode'))
        self.statusBar().showMessage('脚本初始化完成')
        self.setGeometry(300, 300, 260, 320)
        self.setWindowTitle('驱动大师')
        self.show()

    def onOptionInputChange(self, text, type):
        print('change' + type, text)
        if(type == 'option1'):
            self.option1 = text
        elif(type == 'option1Path'):
            self.option1Path = text
        elif(type == 'option2'):
            self.option2 = text
        elif(type == 'option2Path'):
            self.option2Path = text
        elif(type == 'zgMode'):
            self.zgMode = text
        elif(type == 'hhMode'):
            self.hhMode = text
    
    def onClickButtonProgramSwitch(self):
        if(self.isInit):
            self.statusBar().showMessage('请关闭后再重新读取')
            return 
        self.isInit = True
        self.statusBar().showMessage('读取窗口中...')
        t = threading.Thread(target=F_启动进程, args=[self])
        t.start()
        
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

def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())

def cleanup():
    # 执行需要在程序退出之前进行的清理操作
    exit_event.set()

atexit.register(cleanup)

if __name__ == '__main__':
    main()

