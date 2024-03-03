import requests
import re
import send_email
import datetime
from loguru import logger
from 案例.北邮抢课.bupt import LoginHelper

def calcu(back_time:str):
    today = str(datetime.date.today())
    back_time = back_time.replace("/","-")
    date_format = '%Y-%m-%d'
    today = datetime.datetime.strptime(today, date_format)
    back_time = datetime.datetime.strptime(back_time, date_format)
    day_left = (back_time - today).days
    return day_left
def send_mail(books):
    books = books['data']
    book_info = []
    count = 1
    day_left = 999
    panduan_guoqi = 1
    for book in books:
        print(book['title'], "||", book['mydate'], "||", book['guoqi'])
        if (book['guoqi'] == 1):
            guoqi = "已过期"
            if(panduan_guoqi):
                book_info.append("\n以下是已经过期的书籍，主人请尽快归还哦")
                panduan_guoqi = 0
        else:
            guoqi = "未过期"
            if (calcu(book['mydate']) <= 1):
                # renew(book["libraryId"],book["bookBarcode"],book["departmentId"],vpn_ticket)
                pass
            if (calcu(book['mydate']) < day_left):
                day_left = calcu(book['mydate'])

        book_info.append(f"{count}. {book['title']}\n是否已经过期:{guoqi}\n还书时间:{book['mydate']}")
        count += 1
    print("[INFO]:最近需要还书日期||",day_left)
    email_title = f"主人，你还有{day_left}天就要还书啦~"
    if (day_left == 1):
        email_title = f"主人，你还有1天就要还书啦~,如果今天不能按时归还，将自动为您续期哦~"
    elif (day_left == 0):
        email_title = f"主人，不能自动续借啦~，快去还书吧~"
    send_email.send_mail(email_title, "\n".join(book_info).strip())



session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
}
# 首先登录vpn
def sendbook():
    lh = LoginHelper(session)
    lh.vpn_login(2022212288, "WenHao0425")
    lh.menghu_login(username="2022212288", password="WenHao0425*.*")
    books = lh.get_book_info()
    send_mail(books)

while True:
    try:
        sendbook()
        break
    except:
        continue

def btn_down():
    session.get("https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/beiyou.html")

def get_book_info():
    book_url = "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b//reader-borrowinfo.json?vpn-12-o1-opac.bupt.edu.cn:8080"
    books = session.post(book_url,headers={"Referer":"https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/reader-borrowinfo.html"})
    # print(books.text)
    return books.json()

def calcu(back_time:str):
    today = str(datetime.date.today())
    back_time = back_time.replace("/","-")
    date_format = '%Y-%m-%d'
    today = datetime.datetime.strptime(today, date_format)
    back_time = datetime.datetime.strptime(back_time, date_format)
    day_left = (back_time - today).days
    return day_left

def renew(libraryId,bookBarcode,departmentId,vpn_ticket):
    xujie_url = "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b//xujie.json?vpn-12-o1-opac.bupt.edu.cn:8080"
    cookies = {
        'show_vpn': '0',
        'heartbeat': '1',
        'show_faq': '0',
        'wengine_vpn_ticketwebvpn_bupt_edu_cn': vpn_ticket,
        'refresh': '1',
    }
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://webvpn.bupt.edu.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/reader-borrowinfo.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    data = {
        'libraryId': libraryId,
        'bookBarCode': bookBarcode,
        'departmentId': departmentId
    }
    requests.post(xujie_url,headers=headers, cookies=cookies, data=data)


# if __name__ == '__main__':
#     send_mail()