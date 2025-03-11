import requests

def fetch_car_search_results():
    url = "https://www.finn.no/mobility/search/api/search/SEARCH_ID_CAR_USED"
    params = {
        "make": "0.744",
        "page": "1"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "www.finn.no",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Chromium";v="112"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 QuarkPC/2.1.0.226"
    }

    try:
        # 禁用 SSL 验证
        response = requests.get(url, params=params, headers=headers, verify=False)
        if response.status_code == 200:
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

if __name__ == "__main__":
    fetch_car_search_results()