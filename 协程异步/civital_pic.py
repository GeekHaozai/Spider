import time

import aiohttp
import asyncio
import aiofiles
import requests
import json
headers = {
    'authority': 'image.civitai.com',
    'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection':'close',
    'cookie': "__Host-next-auth.csrf-token=2be17ea3ca1ae16393d530a8dbbda23a4ae68eb7eed32448ecd1f0d5428d017a%7C65cf30913e98fe5453a408ff42854b954f73ac5a3b38d2c652a786c7824be0bb; __Secure-next-auth.callback-url=https%3A%2F%2Fcivitai.com; ref_landing_page=%2F; _uc_referrer=direct; cto_bundle=wvSznV9QWWJTUVN4VWJOWlFJT0NEaXR6SjBxTGFMMSUyQjNyJTJGcDBGU1E4MUc5S1dkQmpwUngyOWZ6ZExLdnhXNVVhQVNjN1NDVUkwRjclMkZQanV6Z1FjMWNXJTJCTlc0RG5aQTElMkZVeFZMOXZjS2QzMW9yWFV0ZEM5RlNJUzRXa2Nib1hVSFlyaGoxJTJGcnFScmo0OGU1Z25oR2RqRURWOUElM0QlM0Q; __gads=ID=6b9d47c3cb0a1232:T=1707117541:RT=1707118939:S=ALNI_MYCfhJXKho77TjsasU111Kw3cfabA; __gpi=UID=00000dbdbd290804:T=1707117541:RT=1707118939:S=ALNI_MY5hroT05CTrMl2fjhtBr1v4JNlpA; __eoi=ID=4c94eb4ac9747906:T=1707117541:RT=1707118939:S=AA-Afjau9ToXiDvA9h9XK6e0mEKd; __stripe_mid=4074c574-26c6-489d-b0cd-343cd62167c8940f26",
    'referer': 'https://civitai.com/',
    'sec-ch-ua': '^\\^Not.A/Brand^\\^;v=^\\^8^\\^, ^\\^Chromium^\\^;v=^\\^114^\\^, ^\\^Microsoft',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '^\\^Windows^\\^',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
    'Referer': 'https://civitai.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
    'content-type': 'application/json',
    'if-modified-since': 'Mon, 05 Feb 2024 09:56:53 GMT',
}
CIVITAI_API = "https://civitai.com/api/trpc/image.getInfinite?input="
PARAMS = {"json":{"period":"AllTime","periodMode":"published","sort":"Most Reactions","view":"feed","types":["image"],"tags":[2309],"cursor":"209:75:119:4716219"}}
FOLDER_PATH = r"C:\Users\DELL123\Desktop\图库\civitai\异步"

requests.packages.urllib3.disable_warnings()
# 或者
# import urllib3
# urllib3.disable_warnings()
# 或者
# import logging
# logging.captureWarnings(True)

def get_pic_lists(url,nextCursor,num_wanted,current_num):
    try:
        params = {"json":{"period":"AllTime","periodMode":"published","sort":"Most Reactions","view":"feed","types":["image"],"tags":[2309],"cursor":nextCursor}}
        params = json.dumps(params)
        response = requests.get(url+params, params=params,headers=headers,verify=False)
        data = response.json()
        nextCursor = data["result"]["data"]["json"]["nextCursor"]
        print("[INFO]:获取nextCursor成功|",nextCursor)
        for each_pic in data["result"]["data"]["json"]["items"]:
            if each_pic["name"] is None:
                continue
            pic_url = "https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/"+each_pic["url"]+"/"+each_pic["name"]
            pattern = each_pic["mimeType"]
            if pattern.endswith("png"):
                pic_info = (pic_url,"png")
            if pattern.endswith("jpeg"):
                pic_info = (pic_url,"jpg")
            pic_info_list.append(pic_info)
            current_num += 1
            if current_num >= num_wanted:
                return
        return get_pic_lists(url,nextCursor,num_wanted,current_num)
    except Exception as e:
        print("[ERROR]:An error occurred:", e)
        # 如果发生异常，进行重试
        time.sleep(1)  # 在重试之前等待一段时间
        get_pic_lists(url,nextCursor,num_wanted,current_num)

async def download_pic(pic_info, folder_path,index):
    pic,pic_pattern = pic_info
    file_path = rf"{folder_path}\{index}.{pic_pattern}"
    try:
        async with aiohttp.ClientSession(trust_env=True) as session:
            print(pic)
            async with session.get(pic) as response:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await response.read())
                    print(f"[INFO]:{index}.{pic_pattern}下载完成")
                    await session.close()
    except Exception as e:
        print("[ERROR]:An error occurred:", e)
        # 如果发生异常，进行重试
        await asyncio.sleep(1)  # 在重试之前等待一段时间
        await download_pic(pic_info, folder_path,index)


async def main():
    global pic_info_list
    pic_info_list = []
    get_pic_lists(CIVITAI_API,"209:75:119:4716219",1000,0)
    print("[INFO]:获取图片列表成功|",pic_info_list)
    tasks = [download_pic(pic_info, FOLDER_PATH, index) for index, pic_info in enumerate(pic_info_list, start=1)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())