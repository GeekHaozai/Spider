import time
import traceback
import requests
from 北邮抢课.bupt import LoginHelper, LibraryInfoHandler
import loguru

search_or_not = True
# 首先登录vpn
def sendbook():
    global search_or_not
    session = requests.session()
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    }
    lh = LoginHelper(session)
    lh.vpn_login(2022212288, "WenHao0425")
    lh.menghu_login(username="2022212288", password="WenHao0425*.*")
    lih = LibraryInfoHandler(session)
    if search_or_not:
        lih.get_new_book_info("马斯克")
        search_or_not = False
    books = lih.get_book_info()
    lih.send_mail(books)

while True:
    try:
        sendbook()
        break
    except Exception as e:
        loguru.logger.error(e)
        loguru.logger.error(traceback.format_exc())
        time.sleep(5)
        continue
