# 文件 -- utils.py
import pyautogui
import win32gui
import time
import mouse
import win32con
from win32com.client import Dispatch
from  fonts.index import fontConfigs

projectPath = '.'  # 运行文件的地址


#获取窗口句柄，这个方法执行的时候必须鼠标在游戏窗口之上
class Utils:
    handle = ''
    op = Dispatch("op.opsoft") # 注册op插件，api和使用方法类似大漠插件
    #获取窗口句柄，这个方法执行的时候必须鼠标在游戏窗口之上
    def bindHandle(self):
        real = pyautogui.position()
        self.handle = win32gui.WindowFromPoint((real[0], real[1]))
        print('当前鼠标下窗口handle为' + str(self.handle))

    # 鼠标移动
    def move(self, x, y):
        if((abs(x) + abs(y)) < 100):
            mouse.move(x, y, absolute=False, duration=0.05)
        else:
            mouse.move(x, y, absolute=False, duration=0.1)

    # 鼠标点击
    def click(self):
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE,win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        time.sleep(0.2)

    # 鼠标双击
    def doubleClick(self):
        win32gui.SendMessage(self.handle, win32con.WM_ACTIVATE,win32con.WA_ACTIVE, 0)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(self.handle, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON)
        time.sleep(0.2)

    # 鼠标右击
    def rightClick(self):
        win32gui.SendMessage(self.handle, win32con.WM_RBUTTONDOWN, win32con.MK_RBUTTON)
        win32gui.SendMessage(self.handle, win32con.WM_RBUTTONUP, win32con.MK_RBUTTON)
        time.sleep(0.2)

    # 屏幕找图
    def findPicture(self, img, confidence=0.7):
        ret = pyautogui.locateOnScreen(projectPath + "\images\\"  + img, confidence=confidence)
        if(ret == None):
            return None
        return [ret.left, ret.top, ret.width, ret.height] 
    
    # op插件文字识别 area的形式是x，y 宽度 高度，返回识别到的文字
    def opOcrFont(self, area, fontType, confidence=0.85):
        self.op.SetDict(0, projectPath + '\\fonts\\' + fontType['fileName'])
        ret = self.op.Ocr(area[0], area[1], area[0] + area[2], area[1] + area[3], fontType['color'], confidence)
        return ret

    # op插件文字查找 area的形式是x，y 宽度 高度， 返回文字的所在位置
    def opFindFont(self, area, fontType, text, confidence=0.85):
        self.op.SetDict(0, projectPath + '\\fonts\\' + fontType['fileName'])
        ret = self.op.FindStr(area[0], area[1], area[2], area[3], text, "ffffff-000000", confidence)
        return ret

if __name__ == "__main__":
    print('程序启动后等待3秒，这3秒可以把鼠标切到游戏')
    utils = Utils()
    utils.bindHandle()
    # utils.move(50, 50)
    time.sleep(3)
    # 测试鼠标双击
    count = 1
    print('开始点击')
    while True:
        pyautogui.click()
        time.sleep(1)
        # pyautogui.click()
        # pyautogui.click()
        # pyautogui.click()
        # time.sleep(1)
        # pyautogui.hotkey('ctrl', 'tab')
        # count = count + 1
        # if(count == 6):
        #      time.sleep(60)
        #      count = 1
    # 测试全屏找图
    # ret = utils.findPicture("window_waring.png", confidence=0.95)
    # if(ret != None):
    #     print(ret)
    # ret = utils.opOcrFont([0, 0, 300, 300], fontConfigs['右上角当前地图文字集'])
    # print('识别文字：' ,ret)