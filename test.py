import requests
import json
import time

# https://ai.google.dev/tutorials/python_quickstart
def gemini(question):
    headers = {
        'Content-Type': 'application/json',
    }
    params = {'key':'AIzaSyBTEwaRhEP8icZSU2MPEDmBP1kXhSKJgWY'}
    data_dic = {"contents":{"parts":{"text":question}}}
    data = json.dumps(data_dic)
    response = requests.post('https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent', headers=headers, params=params, data=data)
    print(response.text)

def download_pic():
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309091b) XWEB/8531",
        "checkversion":"2",
        "uid":"928248",
        "minishell":"wxtuitushe",
        "xweb_xhr":"1",
        "token": "o2kzw5IdEaiClfzZh_qT0tJp0gTk",
        "appkey":"wxf020dc26b2582428",
        "Referer": "https://servicewechat.com/wxf020dc26b2582428/2/page-frame.html"
    }

    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888'
    }
    index = 1
    for page in range(1,1000):
        data = {
            "ucode": 25846139,
            "creator_id": 47246,
            "page": page,
            "limit": 24,
            "type": 1,
            "is_vertical": "",
            "type_id": 0,
            "nonce": "eljlmp47brdgso6mlflejps6k5c6nj35",
            "sign": "11a2d0af9668397bae0728002d66c76d",

        }
        r = requests.post(url="https://pushpic-api.us0.me/center/mini/creator/getImageList", headers=headers, data=data,
                          proxies=proxies, verify=False)
        print(r.json())
        for pic in r.json()['data']:
            each_url = pic['img']
            with open(f"C:\\Users\\DELL123\\Desktop\\图库\\头像\\{index}.jpg","wb") as f:
                f.write(requests.get(each_url).content)
                print(f"[INFO]第{index}张下载完毕")
                index += 1


if __name__ == '__main__':
    # download_pic()
    for i in range(1,10):
        print(i)