import requests

cookies = {
    'wengine_vpn_ticketwebvpn_bupt_edu_cn': '6cb0a4c071f87006',
    'heartbeat': '1',
    'show_faq': '0',
    'show_vpn': '0',
    'refresh': '1',
}

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Referer': 'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/cas/login-normal.html',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = (
    ('vpn-1', ''),
    ('captchaId', '9821440381'),
)

response = requests.get('https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/captcha', headers=headers, params=params, cookies=cookies)

