# https://ctbpsp.com/#/
import requests
import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://ctbpsp.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
response = requests.get('https://ctbpsp.com/cutominfoapi/recommand/type/5/pagesize/10/currentpage/2', headers=headers)
base_result = str(response.text)
print(base_result)
key = "1qaz@wsx".encode("utf-8")
print(key)
des = DES.new(key=key, mode=DES.MODE_ECB)
result = des.decrypt(base64.b64decode(base_result)).decode("utf-8")
# result = unpad(result, DES.block_size).decode("utf-8")
print(result)