import utils
import time
import sys
import pyautogui
import random
import pointUtil
from Images.index import IMAGES
from config_color import COLORS
from  fonts.index import fontConfigs
from tkinter import messagebox
projectPath = utils.projectPath
import re
from winsound import PlaySound



class MHWindow:
    GameWindowArea = [0, 0, 0, 0]  #顶点长宽的格式 游戏区域
    SafeWindowArea = [0, 0, 0, 0]  #游戏鼠标安全区域
    DaojuArea = [0, 0, 0, 0]       #道具区域 
    道具使用延时 = 0.1
    utils = None

    def __init__(self):
        print('程序启动后等待3秒，这3秒可以把鼠标切到游戏')
        time.sleep(3)
        self.utils = utils.Utils()
        self.utils.bindHandle()
        ret = self.utils.findPicture(IMAGES["游戏窗口左上角"])
        if(ret == None):
            print('致命错误！未找到游戏窗口，程序退出')
            sys.exit()
        else:
            ret[1] = ret[1] - 14
            self.GameWindowArea = [ret[0], ret[1], 800, 600]
            self.SafeWindowArea = [ret[0] + 100, ret[1] + 100, 700,  500]
            print('绑定窗口成功, 顶部坐标为：(' + str(ret[0]) + "," + str(ret[1])+")")
    
    def F_窗口内查找颜色(self, colors, confidence=0.85):
        ret = self.utils.op.FindMultiColor(
            self.GameWindowArea[0], 
            self.GameWindowArea[1], 
            self.GameWindowArea[0] + 800, 
            self.GameWindowArea[1] + 600, colors[0], colors[1], confidence, 0)
        if(ret[1] > 0):
            return (ret[1] - self.GameWindowArea[0] , ret[2] - self.GameWindowArea[1])
        
    def F_获取游戏光标位置(self):
        for x in range(5):
            ret = self.F_窗口内查找颜色(COLORS["鼠标指针"], confidence=0.9)
            if(ret == None):
                ret = self.F_窗口内查找颜色(COLORS["鼠标指针2"], confidence=0.9)
            if(ret != None):
                # 设置鼠标偏移
                dx = ret[0] - 13
                dy = ret[1] + 4
                return [dx, dy]
    
    def F_鼠标移动到窗口中心(self):
        pyautogui.moveTo(self.GameWindowArea[0] + random.randint(380, 400), self.GameWindowArea[1] + random.randint(280, 320))
        return True

    def F_游戏光标移动到(self, x, y, 手指操作模式 = False):
        targetX = x + 10  # 鼠标的颜色位置有一点偏移需要矫正
        targetY = y + 30  # 鼠标的颜色位置有一点偏移需要矫正
        stepCount = 0
        errorCount = 0
        isSafeArea = False
        手指操作模式计数器 = 0
        if(x > self.SafeWindowArea[0] and x < self.SafeWindowArea[2] and y > self.SafeWindowArea[1] and y < self.SafeWindowArea[3]):
            isSafeArea = True
        lastGamePoint = None
        for i in range(100):
            trueX = pyautogui.position().x
            trueY = pyautogui.position().y
            if(False == (trueX > (self.GameWindowArea[0]-50) and trueX < (self.GameWindowArea[2]+100) and trueY > (self.GameWindowArea[1] - 50) and trueY < (self.GameWindowArea[3] + 100))):
                print('不在游戏框内')
                self.F_鼠标移动到窗口中心()
                continue
            errorCount = errorCount + 0.05
            gamePoint = self.F_获取游戏光标位置()
            if(gamePoint == None):

                if(手指操作模式):
                    手指操作模式计数器 = 手指操作模式计数器 + 1
                    if(手指操作模式计数器 > 3):
                        break
                print('窗口未识别到鼠标')
                errorCount = errorCount + 1
                continue
            if(errorCount == 20):
                errorCount = 0
                self.F_鼠标移动到窗口中心()
                continue
            currentX = gamePoint[0]
            currentY = gamePoint[1]
            currentGamePoint = gamePoint[0] + gamePoint[1]
            if(currentGamePoint == lastGamePoint):
                errorCount = errorCount + 1
            lastGamePoint = currentGamePoint

            # print('当前鼠标位置为：' + str(currentX) + ":" + str(currentY))
            moveX = targetX - currentX
            moveY = targetY - currentY
            # print('距离目标位置为：' + str(moveX) + ":" + str(moveY))
            if abs(moveX) > 2 or abs(moveY) > 2:
                if(stepCount < 2):
                    self.utils.move(moveX / 2 + random.randint(1, 20),
                                moveY / 2 + random.randint(1, 20))
                    stepCount = stepCount + 1
                else:
                    if(isSafeArea):
                        self.utils.move(moveX, moveY)
                    else:
                        if(moveX > 40):
                            moveX = 40
                        elif(moveX < -40):
                            moveX = -40
                        if(moveY > 30):
                            moveY = 30
                        elif(moveY < -30):
                            moveY = -30
                        pyautogui.move(moveX, moveY)
            else:
                break
    
    def F_窗口内查找图片(self, img, confidence=0.75, area=(0, 0, 0, 0)):
        imgPath = projectPath + "\images\\"  + img
        location = None
        windowArea = None
        if(area[0] != 0):
            x = self.GameWindowArea[0] + area[0]
            y = self.GameWindowArea[1] + area[1]
            width = area[2]
            height = area[3]
            windowArea = (x, y, width, height)
        else:
            windowArea = [self.GameWindowArea[0], self.GameWindowArea[1], 800, 600]
        if(confidence == None):
            location = pyautogui.locateOnScreen(imgPath, region=windowArea, grayscale=False)
        else:
            location = pyautogui.locateOnScreen(imgPath, region=windowArea, confidence=confidence)
        if(location != None):
            ret = [int(location.left) - self.GameWindowArea[0], int(location.top) - self.GameWindowArea[1], int(location.width), int(location.height)]
            return ret
        return None

    def F_窗口区域截图(self, fileName, area):
        x = self.GameWindowArea[0] + area[0]
        y = self.GameWindowArea[1] + area[1]
        width = area[2]
        height = area[3]
        windowArea = (x, y, width, height)
        pyautogui.screenshot(projectPath + "\images\\" + fileName, region=windowArea)
        return projectPath + "\images\\" + fileName
    
    ############################### 基础游戏操作 #############################

    def F_获取任务位置和坐标(self, str):
        map = ""
        if("花果山" in str):
            map = "花果山"
        elif("宝象国" in str):
            map = "宝象国"
        elif("五庄观" in str or '庄观' in str):
            map = "五庄观"
        elif("江南野外" in str or "野外" in str):
            map = "江南野外"
        elif("傲来国" in str):
            map = "傲来国"
        elif("墨家村" in str):
            map = "墨家村"
        elif("女儿村" in str):
            map = "女儿村"
        elif("大唐" in str and "外" in str):
            map = "大唐境外"
        elif("大唐国境" in str):
            map = "大唐国境"
        elif("北俱芦洲" in str):
            map = "北俱芦洲"
        elif("驼岭" in str):
            map = "狮驼岭"
        elif("麒麟" in str):
            map = "麒麟山"
        elif("麒山" in str):
            map = "麒麟山"
        elif("东海" in str):
            map = "东海湾"
        elif("建" in str):
            map = "建邺城"
        elif("朱紫国" in str):
            map = "朱紫国"
        elif("普陀山" in str):
            map = "普陀山"
        elif("宝象国" in str):
            map = "宝象国"
        elif("长寿村" in str):
            map = "长寿村"
        elif("长寿郊外" in str or ("外" in str and "长寿" in str)):
            map = "长寿郊外"
        elif("女国" in str):
            map = "西梁女国"
        elif("化生寺" in str):
            map = "化生寺"
        elif("地府" in str):
            map = "地府"
        elif("地狱迷宫" in str or ("地" in str and "迷宫" in str)):
            map = "地狱迷宫"
        elif("碗子山" in str):
            map = "碗子山"
        elif("波月洞" in str):
            map = "波月洞"
        elif("女娲" in str):
            map = "女娲神迹"
        elif("天宫" in str):
            map = "天宫"
        elif("海底迷宫" in str):
            map = "海底迷宫"
        else:
           print('未匹配地图', str)

        str = str.replace(".", ",")
        str = str.replace("。", ",")
        str = str.replace("，", ",")
        str1 = re.findall("(\d+,\d+)", str)
        try:
            point = str1[0].split(",")
            print('F_获取任务位置和坐标->')
            print([map, point])
            return [map, point]
        except:
            return [map, [0, 0]]

    def F_识别自定义任务(self):
        位置信息 = [self.GameWindowArea[0] + 342, self.GameWindowArea[1] + 76,
                211, 105]
        ret = self.utils.baidu通用文字识别(位置信息)
        print('读取自定任务:' + ret)
        return ret
    
    def F_获取当前摄药香时间(self):
        ret = self.utils.ocrXiangTime([self.GameWindowArea[0] + 58, self.GameWindowArea[1] + 69, self.GameWindowArea[0] +113,  self.GameWindowArea[1] + 95])
        if(ret != None):
            str = ret.replace(",", "")
            return str

    def F_获取当前地图(self):
        ret = self.utils.opOcrFont(
            [self.GameWindowArea[0], self.GameWindowArea[1], 143, 47],
            fontConfigs['右上角当前地图文字集'],
            confidence=1
        )
        if(ret != None):
            return ret

    def F_获取当前坐标(self):
        ret = self.utils.opOcrFont(
            [self.GameWindowArea[0], self.GameWindowArea[1], 143, 59], 
            fontConfigs['右上角当前地图坐标文字集'],
            confidence=0.9
            )
        if(ret != None):
            str = ret.replace(",", "")
            return str 
    
    def F_等待人物停止移动(self, 是否要按F9=True):
        上次坐标 = self.F_获取当前坐标()
        time.sleep(1)
        while(True):
            当前坐标 = self.F_获取当前坐标()
            if(当前坐标 != 上次坐标):
                上次坐标 = 当前坐标
                time.sleep(0.8)
                continue
            else:
                break
        if(是否要按F9):
            pyautogui.press('f9')
        print('info: 人物停止移动')
        return True
    
    def F_打开道具(self):
        for i in range(10):
            point = self.F_窗口内查找图片(IMAGES["道具栏"])
            if(point == None):
                pyautogui.hotkey('alt', 'e')
                time.sleep(0.25)
            else:
                self.DaojuArea = [point[0] + 3, point[1] + 55, 250, 205]
                return True
        messagebox.showinfo('严重错误', '打开道具栏失败')
        sys.exit()
    
    def F_关闭道具(self):
        for i in range(10):
            point = self.F_窗口内查找图片(IMAGES["道具栏"], confidence=0.8)
            if(point == None):
                break
            else:
                pyautogui.hotkey('alt', 'e')
                time.sleep(0.5)
                break

    def F_使用道具(self, 道具图片, 是否行囊查找=False):
        self.F_鼠标移动到窗口中心()
        errorCount = 0
        for i in range(10):
            self.F_打开道具()
            point = self.F_窗口内查找图片(道具图片, area=self.DaojuArea)
            if point != None:
                self.F_游戏光标移动到(point[0] + 5, point[1] + 5)
                time.sleep(0.2)
                self.utils.rightClick()
                time.sleep(0.1)
                return True
            else:
                if 是否行囊查找:
                    self.F_游戏光标移动到(self.DaojuArea[0] + 50, self.DaojuArea[1] + 214)
                    self.utils.click()
                    time.sleep(0.25)
                    point = self.F_窗口内查找图片(道具图片, area=self.DaojuArea)
                    if point != None:
                        self.F_游戏光标移动到(point[0], point[1])
                        self.utils.click()
                        self.F_游戏光标移动到(self.DaojuArea[0] + 5, self.DaojuArea[1] + 214)
                        time.sleep(0.3)
                        self.utils.click()
                        time.sleep(0.3)
                        self.utils.click()
                        time.sleep(0.25)
                        return True
                    else:
                        self.F_游戏光标移动到(self.DaojuArea[0] + 5, self.DaojuArea[1] + 214)
                        time.sleep(0.3)
                        self.utils.click()
                        time.sleep(0.25)
                else:
                    print('WARN: 未找到道具' + 道具图片 + '：' + str(errorCount))
                    time.sleep(0.25)

        messagebox.showinfo('严重错误', '查找道具失败-' + 道具图片)  
        sys.exit()

    def F_使用飞行符(self, 目的地):
        for i in range(10):
            if(self.F_获取当前地图() == 目的地):
                self.F_关闭道具()
                return True
            result = self.F_窗口内查找图片(IMAGES["飞行符打开界面"])
            if (result != None):
                飞行点击位置 = pointUtil.飞行传送点[目的地]['飞行符传送点'][1]
                self.F_游戏光标移动到(飞行点击位置[0], 飞行点击位置[1])
                self.utils.click()
                time.sleep(1.5) 
            else:
                self.F_使用道具(IMAGES["飞行符"])   

        messagebox.showinfo('严重错误', 'F_使用飞行符-' + 目的地)  
        sys.exit() 

    def F_使用飞行旗(self, 地图, 飞行点, 是否检验坐标=False):
        目的点 = pointUtil.飞行传送点[地图][飞行点]
        目的点坐标Str = 目的点[2]
        目的点旗子点 = 目的点[1]
        for i in range(10):
            pointStr = self.F_获取当前坐标()
            if(目的点坐标Str in pointStr):
                self.F_关闭道具()
                return True
            if(飞行点 == '飞行符传送点'):
                self.F_使用飞行符(地图)
                self.F_关闭道具()
                return True
            else:
                ret = self.F_使用道具(IMAGES["旗子" + 地图])
                if(ret == False):
                    飞行点 = '飞行符传送点'
                    continue;
                time.sleep(self.道具使用延时)
                time.sleep(0.25)
                self.F_游戏光标移动到(目的点旗子点[0], 目的点旗子点[1])
                self.utils.click()
                if(是否检验坐标==False):
                    time.sleep(0.25)
                    time.sleep(self.道具使用延时)
                    map = self.F_获取当前地图()
                    if(map == 地图):
                        self.F_关闭道具()
                        return True
            time.sleep(self.道具使用延时)
        messagebox.showinfo('严重错误', 'F_使用飞行旗-' + 地图)  
        sys.exit()

    def F_打开小地图(self):
        point = self.F_窗口内查找图片(IMAGES['小地图打开'])
        if(point):
            return True
        pyautogui.press('tab')
        time.sleep(0.25)
        self.F_鼠标移动到窗口中心()
    
    def F_关闭小地图(self):
        point = self.F_窗口内查找图片(IMAGES['小地图打开'])
        if(point):
            pyautogui.press('tab')
            time.sleep(0.25)
            return True
        
    def F_点击小地图出入口按钮(self):
        pyautogui.press('tab')
        time.sleep(0.25)
        point = self.F_窗口内查找图片(IMAGES['小地图出入口按钮'])
        if(point):
            self.F_游戏光标移动到(point[0], point[1])
            self.utils.click()
        pyautogui.press('tab')

    def F_获取小地图坐标(self):
        ret = self.utils.opOcrFont(
            [self.GameWindowArea[0], self.GameWindowArea[1], 800, 600],
            fontConfigs['小地图坐标文字集'],
            confidence=1
        )
        if(ret != None):
            ponit = ret.split(',')
            return ponit
        
    def count_different_chars(self, str1, str2):
        """
        判断两个长度相同的字符串中，不同字符的个数
        :param str1: 第一个字符串
        :param str2: 第二个字符串
        :return: 不同字符的个数
        """
        # 确保两个字符串长度相同
        if len(str1) != len(str2):
            raise ValueError("两个字符串的长度必须相等")
        
        # 逐字符比较并统计不同的字符
        count = sum(1 for a, b in zip(str1, str2) if a != b)
        
        return count
        
    def F_小地图寻路(self, 目标坐标, 是否关闭出入口=False,  检查是否到达指定坐标=True, 是否等待人物停止移动=True):
        目标坐标x = int(目标坐标[0])
        目标坐标y = int(目标坐标[1])
        检查次数 = 1
        if(检查是否到达指定坐标):
            检查次数 = 2
        if(是否等待人物停止移动 == False):
            检查次数 = 1
        for x in range(检查次数):
            if(x == 2):
                self.F_点击小地图出入口按钮()
            nowPoint = self.F_获取当前坐标()
            size1 = len(nowPoint)
            size2 = len(str(目标坐标[0]) + str(目标坐标[1]))

            if(size1 == size2):
                if(nowPoint == str(目标坐标[0]) + str(目标坐标[1])):
                    break 
                ret = self.count_different_chars(nowPoint, str(目标坐标[0]) + str(目标坐标[1])) 
                if(ret < 2):
                    break
            if(是否关闭出入口):
                self.F_点击小地图出入口按钮() 
            self.F_打开小地图()
            time.sleep(0.25)
            isFirstMove = 1
            for i in range(25):
                point = self.F_获取小地图坐标()
                if(point == None or len(point) < 2):
                    self.F_鼠标移动到窗口中心()
                    continue
                当前坐标x = 0
                当前坐标y = 0
                try:
                    当前坐标x = int(point[0])
                    当前坐标y = int(point[1])
                except:
                    continue
                if(目标坐标x == 当前坐标x and 目标坐标y == 当前坐标y):
                    pyautogui.click()
                    time.sleep(0.25)
                    pyautogui.click()
                    break
                cx = 目标坐标x - 当前坐标x
                cy = 当前坐标y - 目标坐标y
                if(isFirstMove < 2):
                    self.utils.move(cx / 2, cy / 2)
                    isFirstMove = isFirstMove + 1
                else:
                    if(cx > 20):
                        cx = 20
                    elif(cx < -20):
                        cx = -20
                    if(cy > 10):
                        cy = 10
                    elif(cy < -10):
                        cy = -10
                    self.utils.move(cx, cy)
                    if(abs(cx) < 20 and abs(cy) < 10):
                        pyautogui.click()
                    else:
                        pyautogui.click()
            time.sleep(2)
            if(检查是否到达指定坐标 == False):
                for i in range(25):
                    point = self.F_获取小地图坐标()
                    if(point == None or len(point) < 2):
                        self.F_鼠标移动到窗口中心()
                        continue
                    当前坐标x = 0
                    当前坐标y = 0
                    try:
                        当前坐标x = int(point[0])
                        当前坐标y = int(point[1])
                    except:
                        continue
                    if(目标坐标x == 当前坐标x and 目标坐标y == 当前坐标y):
                        pyautogui.click()
                        time.sleep(0.25)
                        pyautogui.click()
                        break
                    cx = 目标坐标x - 当前坐标x
                    cy = 当前坐标y - 目标坐标y
                    if(isFirstMove < 2):
                        self.utils.move(cx / 2, cy / 2)
                        isFirstMove = isFirstMove + 1
                    else:
                        if(cx > 20):
                            cx = 20
                        elif(cx < -20):
                            cx = -20
                        if(cy > 10):
                            cy = 10
                        elif(cy < -10):
                            cy = -10
                        self.utils.move(cx, cy)
                        if(abs(cx) < 20 and abs(cy) < 10):
                            pyautogui.click()
                        

            self.F_关闭小地图()
            if(是否等待人物停止移动):
                self.F_等待人物停止移动(是否要按F9=False) 
            if(x == 2):
                self.F_点击小地图出入口按钮()
        print('info: F_小地图寻路器成功')   
        if(是否关闭出入口):
            self.F_点击小地图出入口按钮()
        pyautogui.press('f9')
        return True

    #  ==================== 智能导航相关 ==============================

    def F_获取旗子最近导航点(self, 目的地, point):
        min_values = []
        mapPoints = pointUtil.飞行传送点[目的地]
        for key, item in mapPoints.items():
            min_values.append((abs(int(point[0]) - item[0][0]) + abs(int(point[1]) - item[0][1]), key))
        min_values.sort()
        min_key = min_values[0][1]
        return min_key

    # 智能导航到旗子4国
    def F_智能导航(self, 目的地, 目的点=None, point=None):
        if(目的地 == "天宫"):
            self.F_导航到天宫()
            return
        elif("江南野外" == 目的地):
           self.F_导航到江南野外()
           return
        elif("花果山" == 目的地):
           self.F_导航到花果山()
           return
        elif("五庄观" == 目的地):
           self.F_导航到五庄观()
           return
        elif("墨家村" == 目的地):
            # self.F_导航到墨家村()
            return
        elif("女儿村" == 目的地):
            self.F_导航到女儿村()
            return
        elif("大唐境外" == 目的地):
            self.F_导航到大唐境外()
            return
        elif("大唐国境" == 目的地):
            self.F_导航到大唐国境()
            return
        elif("北俱芦洲" == 目的地):
            self.F_导航到北俱芦洲()
            return
        elif("狮驼岭" == 目的地):
            self.F_导航到狮驼岭()
            return
        elif("麒麟山" == 目的地):
            self.F_导航到麒麟山()
            return
        elif("东海湾" == 目的地):
            self.F_导航到东海湾()
            return
        elif("普陀山" == 目的地):
            self.F_导航到普陀山()
            return
        elif("长寿郊外" == 目的地):
            self.F_导航到长寿郊外()
            return
        elif("化生寺" == 目的地):
            self.F_导航到化生寺()
            return
        elif("地府" == 目的地):
            self.F_导航到地府()
            return
        elif("地狱迷宫" == 目的地):
            self.F_导航到地狱迷宫三层()
            return
        elif("碗子山" == 目的地):
            self.F_导航到碗子山()
            return
        elif("波月洞" == 目的地):
            self.F_导航到波月洞()
            return
        elif("女娲神迹" == 目的地):
            self.F_导航到女娲神迹()
            return
        elif("海底迷宫" == 目的地):
            self.F_导航到海底迷宫()
            return
        if(point == None and 目的点==None):
            self.F_使用飞行符(目的地)
            return 
        if(point != None):
            目的点 = self.F_获取旗子最近导航点(目的地, point)
        self.F_使用飞行旗(目的地, 目的点)
        self.F_关闭道具()

    def F_导航到长寿郊外(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '长寿郊外'):
                return True
            elif(当前所在地图 == '长寿村'):
                self.F_小地图寻路([144, 5])
                self.F_游戏光标移动到(690, 507)
                self.utils.click()
                time.sleep(2)
            else:
                self.F_使用飞行旗('长寿村', '长寿郊外', 是否检验坐标=False)
                self.F_游戏光标移动到(690, 507)
                self.utils.click()
                time.sleep(2)
        return False

    def F_导航到天宫(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '天宫'):
                return True
            elif(当前所在地图 == '长寿郊外'):
                self.F_小地图寻路([28, 56])
                point = self.F_窗口内查找图片('window_cs_tg.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 5, point[1] + 5)
                    self.utils.click()
                    time.sleep(0.25)
                # self.F_游戏光标移动到(262, 224)
                # self.utils.click()
                point = self.F_窗口内查找图片('window_goto.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 5, point[1] + 2)
                    self.utils.click()
                    time.sleep(0.25)
            else:
                self.F_导航到长寿郊外()
        return False

    def F_导航到花果山(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '花果山'):
                return True
            elif(当前所在地图 == '傲来国'):
                self.F_小地图寻路([211, 142])
                time.sleep(0.25)
                self.F_游戏光标移动到(632, 103)
                self.F_游戏光标移动到(723, 84)
                self.utils.click()
                time.sleep(2)
            else:
                self.F_使用飞行旗('傲来国', '花果山')
                self.F_游戏光标移动到(632, 103)
                self.F_游戏光标移动到(723, 84)
                self.utils.click()
                time.sleep(2)
        return False  

    def F_导航到女儿村(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '女儿村'):
                return True
            elif(当前所在地图 == '傲来国'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(167, 203)
                self.utils.click()
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                
                self.F_游戏光标移动到(83, 161)
                self.utils.click()
                time.sleep(2)
                self.utils.click()
            else:
                self.F_使用飞行旗('傲来国', '女儿村', 是否检验坐标=False)
                self.F_游戏光标移动到(83, 151)
                self.utils.click()
                time.sleep(2)
        return False 
    
    def F_导航到麒麟山(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '麒麟山'):
                return True
            elif(当前所在地图 == '朱紫国'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(150, 197)
                self.utils.click()
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                pyautogui.press('f9')
                self.F_游戏光标移动到(35, 125)
                self.utils.click()
                time.sleep(2)
            else:
                self.F_使用飞行旗('朱紫国', '麒麟山', 是否检验坐标=False)
                time.sleep(0.25)
                pyautogui.press('f9')
                self.F_游戏光标移动到(35, 125)
                self.utils.click()
                time.sleep(2)
        return False

    def F_导航到东海湾(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '东海湾'):
                return True
            elif(当前所在地图 == '傲来国'):
                self.F_小地图寻路([177, 20], 是否开关出入口=True)
                self.F_游戏光标移动到(218, 361)
                self.utils.click()
                time.sleep(0.25)
                if(self.F_窗口内查找图片('window_goto.png')):
                    self.F_游戏光标移动到(191, 338)
                    self.utils.click()
                    time.sleep(2)
            else:
                self.F_使用飞行旗('傲来国', '东海湾')
                time.sleep(0.25)
        return False 
    
    def F_导航到北俱芦洲(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '北俱芦洲'):
                return True
            elif(当前所在地图 == '长寿郊外'):
                self.F_小地图寻路([64, 63], 是否等待人物停止移动=False)
                self.F_游戏光标移动到(316, 178)
                self.F_等待人物停止移动()
                self.utils.click()
                time.sleep(0.25)
                # self.F_游戏光标移动到(320, 180)
                # self.utils.click()
                # time.sleep(0.25)
                point=self.F_窗口内查找图片('window_goto.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 2, point[1] + 5)
                    self.utils.click()
                    time.sleep(0.25)
            else:
                self.F_导航到长寿郊外()
        return False

    def F_导航到海底迷宫(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '海底迷宫'):
                return True
            elif(当前所在地图 == '花果山'):
                self.F_小地图寻路([107, 7], 检查是否到达指定坐标=False)
                point = self.F_窗口内查找图片('window_hgs_hd.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 7, point[1] + 2)
                    self.utils.click()
                    time.sleep(0.25)
                # self.F_游戏光标移动到(260, 457)
                # self.utils.click()
                # time.sleep(0.25)
                point = self.F_窗口内查找图片('window_goto.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 2, point[1] + 2)
                    self.utils.click()
                    time.sleep(0.25)
            else:
                self.F_导航到花果山()
        return False

    def F_导航到女娲神迹(self):
        for x in range(6):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '女娲神迹'):
                return True
            elif(当前所在地图 == '北俱芦洲'):

                self.F_小地图寻路([21, 153], 是否等待人物停止移动=False)
                self.F_游戏光标移动到(264, 196)
                self.F_等待人物停止移动()
                self.utils.click()
                time.sleep(0.25)
                point = self.F_窗口内查找图片('window_goto2.png')
                if(point):
                    self.F_游戏光标移动到(point[0] + 5, point[1] + 5)
                    self.utils.click()
                    time.sleep(2)
            else:
                self.F_导航到北俱芦洲()
        return False
    
    def F_导航到化生寺(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 != '长安城'):
                return True
            else:
                ret = self.F_使用飞行旗('长安城', '化生寺', 是否检验坐标=False)
                if(ret):
                    self.F_游戏光标移动到(544, 67)
                    self.utils.click()
                    time.sleep(2)
                else:
                    time.sleep(0.25)
        return False

    def F_导航到江南野外(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '江南野外'):
                return True
            elif(当前所在地图 == '长安城'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(665, 439)
                self.utils.click()
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                # self.F_小地图寻路([535, 2])
                self.F_游戏光标移动到(716, 519)
                self.utils.click()
                time.sleep(2)
            else:
                ret = self.F_使用飞行旗('长安城', '江南野外', 是否检验坐标=False)
                if(ret):
                    self.F_游戏光标移动到(716, 519)
                    self.utils.click()
                    time.sleep(2)
                else:
                    time.sleep(0.25)
        return False

    def F_导航到大唐国境(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '大唐国境'):
                return True
            elif(当前所在地图 == '长安城'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(133, 430)
                self.utils.click()
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(128, 523)
                self.F_游戏光标移动到(67, 543)
                self.utils.click()
                time.sleep(2)
            else:
                ret = self.F_使用飞行旗('长安城', '大唐国境', 是否检验坐标=False)
                if(ret):
                    self.F_游戏光标移动到(128, 523)
                    self.F_游戏光标移动到(67, 543)
                    self.utils.click()
                    time.sleep(2)
                else:
                    time.sleep(0.25)
                self.F_关闭道具()
        return False

    def F_点击驿站老板(self):
        pyautogui.hotkey('alt', 'h')
        驿站老板位置 = None
        驿站老板图片集 =IMAGES["NPC驿站老板"]
        for x in range(4):
            for item in 驿站老板图片集:
                驿站老板位置 = self.F_窗口内查找图片(item, confidence=0.65, area=(303, 54, 379, 197))
                if 驿站老板位置 is not None:
                    self.F_游戏光标移动到(驿站老板位置[0] + 2, 驿站老板位置[1] + 5)
                    self.utils.doubleClick()
                    time.sleep(0.25)
                    if(self.F_窗口内查找图片('window_goto.png')):
                        self.F_游戏光标移动到(191, 332)
                        self.utils.click()
                        time.sleep(2)
                        return True
        print('ERROE：点击驿站老板失败')
        return False

    def F_点击傲来驿站老板(self):
        pyautogui.hotkey('alt', 'h')
        驿站老板位置 = None
        驿站老板图片集 =IMAGES["NPC驿站老板"]
        for x in range(4):
            for item in 驿站老板图片集:
                驿站老板位置 = self.F_窗口内查找图片(item, confidence=0.5, area=(85, 85, 358, 257))
                if 驿站老板位置 is not None:
                    self.F_游戏光标移动到(驿站老板位置[0] + 3, 驿站老板位置[1] + 2)
                    self.utils.doubleClick()
                    time.sleep(0.25)
                    if(self.F_窗口内查找图片('window_goto.png')):
                        self.F_游戏光标移动到(191, 338)
                        self.utils.click()
                        time.sleep(2)
                        return True
        if(self.F_窗口内查找图片('window_goto.png')):
            self.F_游戏光标移动到(191, 338)
            self.utils.click()
            time.sleep(2)
            return True
        print('ERROE：点击驿站老板失败')
        return False

    def F_导航到大唐国境2(self):
        while True:
            map = self.F_获取当前地图()
            if map == '大唐国境':
                break
            elif map == '长安城':
                self.F_小地图寻路([277, 36], 检查是否到达指定坐标=False)
                time.sleep(0.6)
                self.F_点击驿站老板()
                time.sleep(0.25)
                break
            else:
                self.F_使用飞行旗('长安城', '驿站', 是否检验坐标=False)
                time.sleep(0.25)
                self.F_点击驿站老板()
                time.sleep(0.25)

    def F_导航到普陀山(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '普陀山'):
                return True
            elif(当前所在地图 == '大唐国境'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(413, 430)
                self.utils.click()
                time.sleep(0.25)
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(405, 300)
                self.utils.click()
                time.sleep(self.道具使用延时)
                if(self.F_窗口内查找图片('window_goto.png')):
                    self.F_游戏光标移动到(191, 338)
                    self.utils.click()
                    time.sleep(2)
            else:
                self.F_导航到大唐国境()
        return False
    
    def F_导航到地府(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '地府'):
                return True
            elif(当前所在地图 == '大唐国境'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(224, 144)
                self.utils.click()
                pyautogui.press('tab')
                self.F_游戏光标移动到(370, 58)
                self.F_等待人物停止移动()
                self.utils.click()
                time.sleep(1)
                self.utils.click()
                time.sleep(1)
            else:
                self.F_导航到大唐国境2()
        return False
     
    def F_导航到地狱迷宫三层(self):
        self.F_关闭道具()
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '地府'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(256, 197)
                self.utils.click()
                self.utils.click()
                self.F_小地图寻路([32, 106], 检查是否到达指定坐标=True)
                self.F_游戏光标移动到(443, 105)
                self.utils.click()
                self.utils.click()
                time.sleep(2.5)
                self.F_小地图寻路([18, 7], 检查是否到达指定坐标=True)
                self.F_游戏光标移动到(183, 457)
                self.utils.click()
                self.utils.click()
                time.sleep(2.5)
                self.F_小地图寻路([110, 44], 检查是否到达指定坐标=True)
                self.F_游戏光标移动到(734, 410)
                self.utils.click()
                self.utils.click()
                time.sleep(2.5)
                break
            else:
                self.F_导航到地府()
        return False
    
    def F_导航到五庄观(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '五庄观'):
                return True
            elif(当前所在地图 == '大唐境外'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(686, 287)
                self.utils.click()
                time.sleep(0.25)
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(730, 190)
                self.utils.click()
                time.sleep(2)
            elif(当前所在地图 == '大唐国境'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(178, 412)
                self.utils.click()
                time.sleep(0.25)
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(72, 333)
                self.utils.click()
                time.sleep(0.25)
                self.F_游戏光标移动到(686, 287)
            else:
                self.F_导航到大唐国境()
        return False

    def F_导航到狮驼岭(self):
        self.F_导航到大唐境外()
        self.utils.click()
        time.sleep(5)
            

    def F_导航到大唐境外(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '大唐境外'):
                self.F_关闭道具()
                return True
            elif(当前所在地图 == '朱紫国'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(154, 450)
                self.utils.click()
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(116, 499)
                self.F_游戏光标移动到(67, 543)
                self.utils.click()
                time.sleep(2)
            else:
                ret = self.F_使用飞行旗('朱紫国', '大唐境外', 是否检验坐标=False)
                if(ret):
                    self.F_游戏光标移动到(116, 499)
                    self.F_游戏光标移动到(67, 543)
                    self.utils.click()
                    time.sleep(2)
                else:
                    time.sleep(0.25)
               
        return False

    def F_导航到波月洞(self):
        for x in range(5):
            self.F_导航到碗子山()
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '碗子山'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(415, 168)
                self.utils.click()
                time.sleep(0.25)
                pyautogui.press('tab')
                self.F_等待人物停止移动()
                self.F_游戏光标移动到(370, 97)
                self.utils.click()
                time.sleep(2)
                当前所在地图 = self.F_获取当前地图()
                if(当前所在地图 != '碗子山'):
                    break
           
        

    def F_导航到碗子山(self):
        for x in range(5):
            当前所在地图 = self.F_获取当前地图()
            if(当前所在地图 == '碗子山'):
                return True
            elif(当前所在地图 == '宝象国'):
                pyautogui.press('tab')
                self.F_游戏光标移动到(560, 469)
                self.utils.click()
                pyautogui.press('tab')
                self.F_游戏光标移动到(642, 469)
                self.F_游戏光标移动到(724, 535)
                self.F_等待人物停止移动()
                self.utils.click()
                time.sleep(2)
            else:
                ret = self.F_使用飞行旗('宝象国', '飞行符传送点', 是否检验坐标=False)
                if(ret):
                    pyautogui.press('tab')
                    self.F_游戏光标移动到(560, 469)
                    self.utils.click()
                    pyautogui.press('tab')
                    self.F_游戏光标移动到(642, 469)
                    self.F_游戏光标移动到(724, 535)
                    self.F_等待人物停止移动()
                    self.utils.click()
                    time.sleep(2)
                else:
                    time.sleep(0.25)

 # ========================== 战斗相关  =======================================

    def F_是否在战斗(self):  
        point = self.F_窗口内查找图片(IMAGES['战斗中标记'], area=(441, 561, 50, 40))
        if point != None:
            return True
        else:
            return False
    
    def F_关闭对话(self):
        time.sleep(0.3)
        point = self.F_窗口内查找图片('window-close.png', confidence=0.8)
        if(point != None):
            self.F_游戏光标移动到(point[0] + 10, point[1] + 5)
            time.sleep(0.1)
            self.utils.click()
            return True

    def F_铃铛自动战斗(self):
        finish = False
        count = 0
        while(finish == False):
            count = count + 1
            time.sleep(0.25)
            if(self.F_是否在战斗()):
                time.sleep(2)
                while(True):
                    print('进入战斗')
                    time.sleep(1)
                    if(self.F_是否结束战斗()):
                        finish = True
                        break
            else:
                if(count == 3):
                    PlaySound(projectPath + "\\" + "y913.wav", flags=1)


    def F_点击主怪自动战斗(self, key=None):
        finish = False
        count = 0
        imgPath = projectPath + "\images\\window_waring.png"
        while(finish == False):
            count = count + 1
            time.sleep(0.25)
            if(self.F_是否在战斗()):
                if(key):
                    pyautogui.press('f7')
                    self.F_游戏光标移动到(275,134)
                    pyautogui.press(key)
                    time.sleep(0.25)
                    self.utils.click()
                pyautogui.hotkey('alt', 'q')
                pyautogui.hotkey('alt', 'q')
                pyautogui.hotkey('alt', 'q')
                self.utils.rightClick()
                self.F_关闭对话()
                while(True):
                    print('进入战斗')
                    time.sleep(0.25)
                    location = pyautogui.locateOnScreen(imgPath, confidence=0.95)
                    if(location != None):
                        PlaySound(projectPath + "\images\\" + "wozhidao.wav", flags=1)
                        time.sleep(15)
                    point = self.F_窗口内查找图片('window_zidong2.png')
                    if(point):
                        print('发现自动')
                        pyautogui.hotkey('alt', 'q')
                        pyautogui.hotkey('alt', 'q')
                        pyautogui.hotkey('alt', 'q')
                    if(self.F_是否结束战斗()):
                        finish = True
                        break
            else:
                if(count == 3):
                    PlaySound(projectPath + "\images\\" + "wozhidao.wav", flags=1)

    def F_抓鬼自动战斗(self):
        finish = False
        count = 0
        while(finish == False):
            count = count + 1
            time.sleep(0.25)
            if(self.F_是否在战斗()):
                time.sleep(1)
                self.F_关闭对话()
                self.F_点击自动()
                self.F_鼠标移动到窗口中心()
                while(True):
                    time.sleep(0.25)
                    if(self.F_是否结束战斗()):
                        finish = True
                        break
            else:
                if(count == 3):
                    PlaySound(projectPath + "\\" + "y913.wav", flags=1)

    def F_点击战斗(self):
        pathMaybe = [[5, 78], [38, 78], [-20, 78], [3, 78]]
        for i in range(4):
            self.F_游戏光标移动到(574, 442)
            point = self.F_窗口内查找图片(IMAGES['狮子队标'])
            pyautogui.hotkey('alt', 'a')
            self.utils.rightClick()
            pathMaybeItem = pathMaybe[i]
            if(point == None):
                point = self.F_窗口内查找图片('window_zq.png')
                if(point):
                    point[0] = point[0] -10
                    point[1] = point[1] -90 
            if(point != None):
                pyautogui.hotkey('alt', '7')
                self.utils.rightClick()
                self.F_游戏光标移动到(point[0]+pathMaybeItem[0],
                               point[1] + pathMaybeItem[1])
                time.sleep(0.25)
                pyautogui.hotkey('alt', 'a')
                time.sleep(0.1)
                self.utils.click()
                time.sleep(1)
                if(self.F_是否在战斗()):
                    break
                else:
                    pyautogui.hotkey('alt', '1')
                    self.utils.rightClick()
    
    def F_是否结束战斗(self):
        ret = self.utils.op.FindMultiColor(
            self.GameWindowArea[0]+380, self.GameWindowArea[1]+520, self.GameWindowArea[0]+545, self.GameWindowArea[1]+600, 'c80000', '5|3|882800,8|2|881400,5|4|882800', 0.8, 0)
        if ret[1] > 0:
            return True
        else:
            return False

    def F_点击自动(self):
        point = self.F_窗口内查找图片('window_zidong.png')
        if(point):
            self.F_游戏光标移动到(point[0] + 5, point[1] + 2)
            self.utils.click()
        self.F_游戏光标移动到(669, 85)
        self.F_游戏光标移动到(669, 28)
        self.utils.click()



if __name__ == "__main__":
    mhWindow = MHWindow()
    # print('光标位置', mhWindow.F_获取游戏光标位置())
    # print('鼠标移动到窗口中心', mhWindow.F_鼠标移动到窗口中心())
    # mhWindow.F_游戏光标移动到(409, 188)
    # print('道具栏位置', mhWindow.F_窗口内查找图片(IMAGES["道具栏"]))
    # mhWindow.F_窗口区域截图('截图测试.png', (100, 100, 100, 100))
    # print(mhWindow.F_获取当前坐标())
    # print(mhWindow.F_获取当前地图())
    # mhWindow.F_打开道具()
    # mhWindow.F_关闭道具()
    # mhWindow.F_使用道具(IMAGES["摄妖香"])
    # mhWindow.F_使用飞行符('傲来国')
    # mhWindow.F_使用飞行旗('傲来国', '女儿村', False)
    # mhWindow.F_打开小地图()
    # print(mhWindow.F_获取小地图坐标())
    print(mhWindow.F_导航到海底迷宫())

