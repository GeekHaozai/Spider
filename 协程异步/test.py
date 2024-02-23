import asyncio

import aiofiles
import aiohttp
async def get_baidu(session,wd):
    async with session.get(f'https://www.baidu.com?wd={wd}') as response:
        async with aiofiles.open(f'测试/{wd}.html', 'wb') as f:
            await f.write(await response.read())
        print(response.status)

async def main():
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = [get_baidu(session,wd) for wd in range(10)]
        print(tasks)
        await asyncio.gather(*tasks)

asyncio.run(main())