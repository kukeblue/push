import pyautogui
import utils
import time
import os
from qiniu import Auth, put_file
import requests
import json

# ========== 配置部分 ==========
# 七牛云 AccessKey 和 SecretKey

def login(account):
    pyautogui.moveTo(1071, 688)
    ACCESS_KEY = 'RTGyt7Ic-zM8lIY1JjBt8NyBN-a77WMvpDtKqkdw'
    SECRET_KEY = 'FDXk8_mUDPCPexslldeu4_ttyVFXJ3P1TzHB9I04'
    BUCKET_NAME = 'yemait'
    BASE_URL = 'https://upload.cyuandao.com'
    SAVE_PATH_PREFIX = '_nuxt'

    # ========== 截图部分 ==========
    # 构造目标图像路径
    projectPath = utils.projectPath
    imgPath = os.path.join(projectPath, "images", "mh_login_1.png")
    imgPath2 = os.path.join(projectPath, "images", "captured_region2.png")

    location = pyautogui.locateOnScreen(imgPath2, confidence=0.8)
    if location is None:
        print("❌ 未找到图像，无法截图1")
        exit()

    left, top = location.left, location.top
    print(f"✅ 找到图像顶点坐标：({left}, {top})")
    pyautogui.click(left, top)
    # 查找图像位置
    time.sleep(2)  # 等待界面加载
    location = pyautogui.locateOnScreen(imgPath, confidence=0.8)

    if location is None:
        print("❌ 未找到图像，无法截图2")
        exit()

    left, top = location.left, location.top
    print(f"✅ 找到图像顶点坐标：({left}, {top})")

    # 截图区域并保存为本地文件
    screenshot = pyautogui.screenshot(region=(left, top, 171, 199))
    save_filename = f"window_qr_login_{int(time.time())}.png"
    local_path = os.path.join(projectPath, "images", save_filename)
    screenshot.save(local_path)
    print(f"📸 截图保存至：{local_path}")

    # ========== 七牛上传部分 ==========
    # 初始化七牛身份验证
    q = Auth(ACCESS_KEY, SECRET_KEY)

    # 构造远程路径（保存在七牛 _nuxt 目录下）
    key = f"{SAVE_PATH_PREFIX}/{save_filename}"

    # 获取上传凭证
    token = q.upload_token(BUCKET_NAME, key, 3600)

    # 上传文件
    ret, info = put_file(token, key, local_path)

    # 结果处理
    if info.status_code == 200:
        public_url = f"{BASE_URL}/{key}"
        print(f"✅ 上传成功，图片链接：{public_url}")




    authorization = "hmp_c1251436e793a2ae658855b07b27ca536965b77e03852fa44f8f9175bc1b10a1"

    url = "https://api.hamibot.com/v1/devscripts/688dadfdf01d0aa374a6eab7/run"

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json"
    }

    payload = {
        "devices": [{"_id": "688daca84435f5fa177fda03"}],
        "vars": {
            "account": account,
            "imageUrl": public_url
        }
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload)  # or use json=payload directly
    )

    print(response.status_code)

    time.sleep(20)
    pyautogui.click()
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)

login('c*com@163.com')
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)
login('c*om2@163.com')
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)
login('c*om4@163.com')
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)
login('c*om5@163.com')
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)
login('c*om8@163.com')
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)

import glob

def delete_qr_login_images():
    projectPath = utils.projectPath
    images_dir = os.path.join(projectPath, "images")
    
    # 查找所有以 window_qr_login_ 开头的图片
    files_to_delete = glob.glob(os.path.join(images_dir, "window_qr_login_*.png"))
    
    # 删除找到的文件
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"🗑️ 已删除: {file_path}")
        except Exception as e:
            print(f"❌ 删除 {file_path} 时出错: {e}")

# 在脚本最后调用这个函数
delete_qr_login_images()
time.sleep(3)
pyautogui.hotkey('ctrl', 'tab')