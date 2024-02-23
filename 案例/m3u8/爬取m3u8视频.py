import os
import requests
import aiohttp
import asyncio
import aiofiles
import re


async def download_ts_all(m3u8_index_url):
    timeout = aiohttp.ClientTimeout(total=1200)  # 设置超时时间为1200秒
    connector = aiohttp.TCPConnector(limit=50)  # 降低并发数量
    async with aiohttp.ClientSession(trust_env=True, connector=connector, timeout=timeout) as session:
        async with session.get(m3u8_index_url) as response:
            m3u8_data = await response.text()
            print("[INFO]:获取m3u8列表成功!")
            ts_list = re.findall(",\n(.*?)\n#", m3u8_data)
            print(ts_list)
            tasks = [asyncio.create_task(download_ts(ts_url, index, session)) for index, ts_url in enumerate(ts_list, start=1)]
            # tasks = []
            # for i in ts_list[0:1]:
            #     tasks.append(asyncio.create_task(download_ts(i, 1, session)))
            await asyncio.gather(*tasks)
    join_ts()




async def download_ts(ts_url, index, session):
    base_url = "https://ev-h.phncdn.com/hls/videos/202402/18/448335911/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_448335911.mp4.urlset/"
    url = base_url + ts_url
    url = url.replace("ev","cv")
    print(f"[INFO]开始下载: {url}")
    async with session.get(url,headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "authority": "ev-h.phncdn.com",
        "Origin":"https://cn.pornhub.com",
        "Referer":"https://cn.pornhub.com/"
    }) as response:
        async with aiofiles.open(f"爬取的ts片段/{index}.ts", 'wb') as f:
            await f.write(await response.read())
            print(f"[DOWN]下载完成: {url}")


def join_ts():
    total = len(os.listdir("爬取的ts片段"))
    with open("合并的视频/合并后的ts.mp4", "wb") as f:
        for i in range(total):
            with open(f"爬取的ts片段\\{i + 1}.ts", "rb") as f2:
                f.write(f2.read())
    print("[INFO]合并完成!")





if __name__ == '__main__':
    while True:
        html = requests.get("https://cn.pornhub.com/view_video.php?viewkey=65d23d9e3ed85&t=193").text
        # print(html)
        master_m3u8 = re.findall("\"videoUrl\":\"(.*?)\"",html)
        print("[INFO]:获取视频地址列表成功|", master_m3u8)
        master_m3u8 = master_m3u8[0].replace("\\","").replace("\"","")
        if "validfrom=" not in master_m3u8:
            print("[INFO]:取得视频地址成功|", master_m3u8)
            break
    match = re.search("/1080P_4000K_(\d+)\.mp4",master_m3u8).group(1)
    master_m3u8_url = re.sub("/1080P_4000K_\d+\.mp4",f"/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_{match}.mp4.urlset",master_m3u8)
    print("[INFO]:取得m3u8视频地址成功|", master_m3u8_url)
    text = requests.get(master_m3u8_url).text
    print(text)
    # index_m3u8 = re.search("index-f2-v1-a1.m3u8.*?\n", text).group(0).strip()
    # index_m3u8_url = "https://ev-h.phncdn.com/hls/videos/202402/18/448335911/,1080P_4000K,720P_4000K,480P_2000K,240P_1000K,_448335911.mp4.urlset/" + index_m3u8
    # print("[INFO]:取得m3u8索引地址成功|", index_m3u8_url)
    # asyncio.run(download_ts_all(index_m3u8_url))
    import subprocess
    from functools import partial
    subprocess.Popen = partial(subprocess.Popen, encoding='utf-8')
    os.system(f"N_m3u8DL-CLI_v3.0.2.exe {master_m3u8_url}")