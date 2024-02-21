import json
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')

import execjs
import requests

# print(execjs.get().name)
with open("网易.js","r", encoding="utf-8") as f:
    js_code = f.read()

ctx = execjs.compile(js_code)
def get_song(song_id:str):
    id = {
    "ids": f"[{song_id}]",
    "level": "standard",
    "encodeType": "aac",
    "csrf_token": ""
}
    id = json.dumps(id)

    para = ctx.call("get_param", id)
    encText = para["encText"]
    encSecKey = para["encSecKey"]
    data = {"params":encText,"encSecKey":encSecKey}
    print(data)
    headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
                "Referer": "https://music.163.com/",
                "Cookie":"NMTID=00O_XfrKaFe1qV7-EU7rk5ZyE6gOpEAAAGNUGB0PA; _iuqxldmzr_=32; _ntes_nnid=3d9bc9e49fa1c2f09915a910542c68a5,1706450515403; _ntes_nuid=3d9bc9e49fa1c2f09915a910542c68a5; WEVNSM=1.0.0; WNMCID=lrbrtg.1706450515710.01.0; WM_TID=muII0cj0mTZFAERRQRfFgWLAGmmgpg4u; ntes_utid=tid._.uDQOyvfQo8FAUgUFAVfF1GeFXynjgyfs._.0; sDeviceId=YD-ae5e5B9eRfdBQ1RUUAeAeTliVgs8Iwun; __snaker__id=KkUsbE2q0RRPmkMX; JSESSIONID-WYYY=l5uYqs%2F72ZVC83QDOViTumr4ZpgP0KYNJPKx9%5CICkd7%2BglEvdEw2Rjhi5UHNJJUqy0yllEN7%5CcynbbGKJCICm799ZfN%2Bem%2B9Uh1ODHfyiJ%2BazSXf%2BrroRY1GNVhBwC3fWb3hWfjZePX446EJRFrt92RCGgaF51HY0%5C%2Fgb45ahQc7i4Pw%3A1708528067704; WM_NI=sDKAzs04jjK1gxCCPdOIDfyKu1TNpXJbWRr4DrL1wQViR4qH%2FDWCQhoO5Jd8PmccBAm%2FJrOxH0dE0jeOYodKzAC199G2s%2Bsl1N2zO7j757L0Wj3ecHOIGwZb8cznvqCTdFU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee99ed6b8392e5a3d834a7868ea7d45b938a9e87d534b699b8a3f26ef594b792cd2af0fea7c3b92ab19c85a2f979f4eca68bca3ba5a88da4d3708d978c87fc41b7ef9caff3548abe99b3f14088ae84d2f65b96b79ed5f444ed9c99a4d464ad91fbabe73494b3ad84c14baff18693ce748cf0aca6b362a7919790e741ba9f8dd2bc3385eebdccf268f392fe9bce3daae9fbd8cf3c95b6fd86e2448d978998d96afcbdb68ff57b818caca7d837e2a3; gdxidpyhxdE=NduVBLjxW%2BoOMNKvNo0bMtufpEhrlk%2F7Eu0jYf%2FjfvVfx5QnU0uK8LNfhdCnal37fdPAQH3PWZsA04q2siBsSk90UCUijTdRvo4NrCEpQLM68or2GU4hpDvwafpBWwpyau2o5G%5CUXPxKIZYkXBMW8AmtEn%2FslQyKUxmv%5C9WqeYpO3ChW%3A1708527179560; playerid=49858713"
    }
    # with open("music.m4a","wb") as f:
    r = requests.post("https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=",
                          data=data,
                      headers=headers)
    print(r.status_code)
    print(r.text)


if __name__ == '__main__':
    get_song("1353212443")
