from playwright.sync_api import sync_playwright

import requests

def fetch_car_search_results():
    # 目标 URL
    url = "https://www.finn.no/mobility/search/api/search/SEARCH_ID_CAR_USED"
    params = {
        "make": "0.744",  # 品牌参数
        "page": "1"       # 页码参数
    }

    # 设置请求头，模拟浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # 发送 GET 请求
        response = requests.get(url, params=params, headers=headers)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析 JSON 响应
            json_data = response.json()
            print("成功获取 JSON 数据：")
            print(json_data)
            return json_data
        else:
            print(f"请求失败，状态码：{response.status_code}")
            print(f"响应内容：{response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求异常：{e}")
        return None

def get_html_after_click():
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)  # headless=False 会打开浏览器窗口
        context = browser.new_context()
        page = context.new_page()

        # 访问目标网址
        page.goto("https://www.finn.no/mobility/search/car")
        page.wait_for_load_state("networkidle")

        # 删除 id 为 sp_message_container_1258793 的 div
        page.evaluate('''() => {
            const div = document.getElementById('sp_message_container_1258793');
            if (div) {
                div.remove();
            }
        }''')

        # 修改 body 的 overflow 和 position 样式，并添加 !important
        page.evaluate('''() => {
            document.body.setAttribute('style', 'overflow: unset !important; position: unset !important;');
        }''')

        # 查找所有匹配 "Vis alle" 的按钮并点击第一个
        vis_alle_buttons = page.locator("text=Vis alle")  # 定位所有 "Vis alle" 按钮
        if vis_alle_buttons.count() > 0:  # 确保至少找到一个按钮
            vis_alle_buttons.first.scroll_into_view_if_needed()  # 滚动到第一个按钮的位置
            vis_alle_buttons.first.click()  # 点击第一个按钮

        button = page.locator('//button[.//h3[contains(text(), "Merke")]]')
        if button.count() > 0:  # 确保找到按钮
            print("找到包含 'Merke' 的按钮")

            # 获取同级的下一个 div
            next_div = page.locator('//button[.//h3[contains(text(), "Merke")]]/following-sibling::div[1]')
            if next_div.count() > 0:  # 确保找到下一个 div
                print("找到同级的下一个 div")
                links_map = {}
                a_tags = next_div.locator('a')  # 定位所有 <a> 标签
                for i in range(a_tags.count()):  # 遍历所有 <a> 标签
                    href = a_tags.nth(i).get_attribute('href')  # 获取 href
                    text = a_tags.nth(i).inner_text()  # 获取文字内容
                    if href and text:  # 确保 href 和 text 都存在
                        links_map[href] = text  # 添加到字典

                # 打印结果
                print("提取的链接和文字内容：")
                for href, text in links_map.items():
                    print(f"{href}: {text}")
                # 获取 div 的内容或属性
                # div_content = next_div.inner_text()
                # print("下一个 div 的内容：", div_content)
            else:
                print("未找到同级的下一个 div")
        else:
            print("未找到包含 'Merke' 的按钮")

        # 获取页面的 HTML 内容
        html_content = page.content()

        # 关闭浏览器
        browser.close()

        return html_content

# 调用函数并打印返回的 HTML
html = fetch_car_search_results()
print(html)
