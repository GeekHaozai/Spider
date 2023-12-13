import requests
import re

session = requests.session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
}
# 首先登录vpn
def vpn_login(username="2022212288", password="WenHao0425"):
    url = "https://webvpn.bupt.edu.cn/do-login"
    data = {"username": username, "password": password}
    r = session.post(url, data=data)

# 然后登录信息门户
def menghu_login(username="2022212288", password="WenHao0425"):
    megnhu_exe_url = "https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694"
    r = session.get(megnhu_exe_url,headers={"Referer":"https://webvpn.bupt.edu.cn/"})
    execution = re.findall("\"execution\" value=\"(.*?)\"", r.text)[0]
    print("[INFO]:成功获取execution:||",execution)
    menghu_login_url = "https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login"
    res = session.post(menghu_login_url,data={"username": username, "password": password, "submit": "登录", "type":"username_password", "execution": execution, "_eventId": "submit"},headers={"Referer":"https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694"})

def btn_down():
    session.get("https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/beiyou.html")

def get_book_info():
    book_url = "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b//reader-borrowinfo.json?vpn-12-o1-opac.bupt.edu.cn:8080"
    books = session.post(book_url,headers={"Referer":"https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/reader-borrowinfo.html"})
    return books.json()

if __name__ == '__main__':
    vpn_login()
    menghu_login()
    btn_down()
    books = get_book_info()['data']
    for book in books:
        print(book['title'],"||",book['mydate'],"||",book['guoqi'])
