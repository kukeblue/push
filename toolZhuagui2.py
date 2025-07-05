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
import mhZhuagui2
from winsound import PlaySound
# 禁止控制台输出
import os
sys.stdout = open(os.devnull, 'w')

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
        app.statusBar().showMessage('程序运行中,任务等待中')
        while ProgramSwitch:
            app.statusBar().showMessage('线程执行中....')
            print('线程执行中....')
            try:
                mhZhuagui2.抓鬼(window, True)
            except:
                ProgramSwitch = False
                app.ButtonProgramSwitch.setText("开启")
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

