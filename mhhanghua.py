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

while True:
    time.sleep(2)
    pyautogui.press('up') 
    pyautogui.press('enter')     
    time.sleep(300)