import json
import time
import ddddocr
import csv
from loguru import logger
import requests
import re

class BuptWeb:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

class LoginHelper:
    def __init__(self, session):
        self.session = session
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def vpn_login(self, username, password):
        url = "https://webvpn.bupt.edu.cn/do-login"
        data = {
            " auth_type": "local",
            "username": username,
            "sms_code": "",
            "password": password,
            "captcha": "",
            "needCaptcha": "false",
            "captcha_id": "54GSJFNziB41KuS"
        }
        res = self.session.post(url, data=data)
        logger.info("登录结果:" + str(res.json()))
        if '需要确认登录' in res.text:
            confirm_url = "https://webvpn.bupt.edu.cn/do-confirm-login"
            res = self.session.post(confirm_url)
            logger.info("确认登录结果:" + str(res.json()))
        logger.info("取得cookie成功:" + str(self.session.cookies))

    # 教育系统登录加密逻辑在这
    # var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    # function encodeInp(input) {
    #     var output = "";
    #     var chr1, chr2, chr3 = "";
    #     var enc1, enc2, enc3, enc4 = "";
    #     var i = 0;
    #     do {
    #         chr1 = input.charCodeAt(i++);
    #         chr2 = input.charCodeAt(i++);
    #         chr3 = input.charCodeAt(i++);
    #         enc1 = chr1 >> 2;
    #         enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
    #         enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
    #         enc4 = chr3 & 63;
    #         if (isNaN(chr2)) {
    #             enc3 = enc4 = 64
    #         } else if (isNaN(chr3)) {
    #             enc4 = 64
    #         }
    #         output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
    #         chr1 = chr2 = chr3 = "";
    #         enc1 = enc2 = enc3 = enc4 = ""
    #     } while (i < input.length);
    #     return output
    # }
    @staticmethod
    def encode_inp(input: str):
        key_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        output = ""
        i = 0
        chr1 = input[i] if i < len(input) else "a"
        i += 1
        chr2 = input[i] if i < len(input) else "a"
        i += 1
        chr3 = input[i] if i < len(input) else "a"
        i += 1
        enc1 = ord(chr1) >> 2
        enc2 = ((ord(chr1) & 3) << 4) | (ord(chr2) >> 4)
        enc3 = ((ord(chr2) & 15) << 2) | (ord(chr3) >> 6)
        enc4 = ord(chr3) & 63
        if not chr2.isdigit():
            enc3 = enc4 = 64
        elif not chr3.isdigit():
            enc4 = 64
        output = output + key_str[enc1] + key_str[enc2] + key_str[enc3] + key_str[enc4]
        chr1 = chr2 = chr3 = ""
        enc1 = enc2 = enc3 = enc4 = ""
        while i < len(input):
            chr1 = input[i] if i < len(input) else "￥"
            i += 1
            chr2 = input[i] if i < len(input) else "￥"
            i += 1
            chr3 = input[i] if i < len(input) else "￥"
            i += 1

            enc1 = ord(chr1) >> 2 if chr1 != "￥" else 0
            if chr1 != "￥" and chr2 != "￥":
                enc2 = ((ord(chr1) & 3) << 4) | (ord(chr2) >> 4)
            elif chr1 != "￥" and chr2 == "￥":
                enc2 = (ord(chr1) & 3) << 4
            elif chr1 == "￥" and chr2 != "￥":
                enc2 = ord(chr2) >> 4
            else:
                enc2 = 0
            if chr2 != "￥" and chr3 != "￥":
                enc3 = ((ord(chr2) & 15) << 2) | (ord(chr3) >> 6)
            elif chr2 != "￥" and chr3 == "￥":
                enc3 = (ord(chr2) & 15) << 2
            elif chr2 == "￥" and chr3 != "￥":
                enc3 = ord(chr3) >> 6
            else:
                enc3 = 0
            enc4 = ord(chr3) & 63 if chr3 != "￥" else 63
            if not chr2.isdigit():
                enc3 = enc4 = 64
            elif not chr3.isdigit():
                enc4 = 64
            output = output + key_str[enc1] + key_str[enc2] + key_str[enc3] + key_str[enc4]
            chr1 = chr2 = chr3 = ""
            enc1 = enc2 = enc3 = enc4 = ""
        return output

    @staticmethod
    def get_encoded(username, password):
        account = LoginHelper.encode_inp(username)
        passwd = LoginHelper.encode_inp(password)
        encoded = account + "%%%" + passwd
        return encoded

    def edu_login(self, username, password):
        url = "https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xk/LoginToXk"
        data = {
            "userAccount": username,
            "userPassword": "",
            "encoded": LoginHelper.get_encoded(username, password)
        }
        res = self.session.post(url, data=data)
        result = "成功" if "成绩证明" in res.text else "失败"
        logger.info("教育管理系统登录结果:" + str(result) + str(res.status_code))
        logger.info("cookie状态:" + str(self.session.cookies))

    def menghu_login(self, username, password):
        menghu_url = self.session.get("https://webvpn.bupt.edu.cn/user/portal_groups").json()
        menghu_url = "https://webvpn.bupt.edu.cn" +menghu_url["data"][0]["resource"][0]["redirect"]
        logger.success("获取信息门户url成功:" + menghu_url)
        cookies = {

            'show_vpn': '0',
            'heartbeat': '1',
            'show_faq': '0',
            'refresh': '1',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',

        }

        response = self.session.get(
            menghu_url,
            headers=headers, cookies=cookies)
        # print(response.text)
        execution = re.findall("\"execution\" value=\"(.*?)\"", response.text)[0].strip()
        logger.info("成功获取execution:||" + execution)
        captcha_id = re.findall(r"id: '(\d+)'",response.text,re.DOTALL)[0]  # 4707540463
        print(captcha_id)
        if captcha_id:
            logger.info("获取captchaId:" + captcha_id)
            pic = self.session.get(
                f"https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/captcha?vpn-1&captchaId={captcha_id}&r=45738")
            ocr = ddddocr.DdddOcr()
            captcha = ocr.classification(pic.content)
            logger.success("验证码识别结果:" + captcha)
            res = self.session.post('https://webvpn.bupt.edu.cn/wengine-vpn/input',
                                    data='{"name":"","type":"text","value":"' + captcha + '"}', )
            logger.debug("input请求结果:" + res.text)
        else:
            captcha = None
        menghu_login_url = "https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login"
        tushu_login_url = "https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login"
        data = {
            'username': username,
            'password': password,
            "captcha": captcha,
            'submit': '登录',
            'type': 'username_password',
            'execution': execution,
            '_eventId': 'submit'
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Type': 'application/json' 就是这里有问题
            'Origin': 'https://webvpn.bupt.edu.cn',
            'Referer': 'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        cookies = {
            'show_vpn': '0',
            'heartbeat': '1',
            'show_faq': '0',
            'refresh': '1',
        }
        response = self.session.post(menghu_login_url, data=data,headers=headers,cookies=cookies)
        ress = self.session.post(tushu_login_url,data={
            'username': username,
            'password': password,
            "captcha": captcha,
            'submit': '登录',
            'type': 'username_password',
            'execution': execution,
            '_eventId': 'submit'
        },headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Type': 'application/json' 就是这里有问题
            'Origin': 'https://webvpn.bupt.edu.cn',
            'Referer': "https://webvpn.bupt.edu.cn/http/77726476706e69737468656265737421f1e2559469327d406a468ca88d1b203b/authserver/login?service=http%3A%2F%2Fopac.bupt.edu.cn%3A8080%2Fbeiyou.html",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        },cookies=cookies)
        print(ress.text)
        print(response.headers)
        print(response.status_code)
        if "移动校园" in response.text:
            logger.error("登录失败")
            # print(response.text)
            # return attempt_login(response.text)
        else:
            logger.success("门户登录成功")
            # print(response.text)
            # self.session.p
            return True

    def get_book_info(self):
        self.session.get(
            "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/beiyou.html")
        # 按下button
        book_url = "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b//reader-borrowinfo.json?vpn-12-o1-opac.bupt.edu.cn:8080"
        books = self.session.post(book_url, headers={
            "Referer": "https://webvpn.bupt.edu.cn/http-8080/77726476706e69737468656265737421ffe7409f69327d406a468ca88d1b203b/reader-borrowinfo.html"})
        print(books.text)
        return books.json()


# 进入选课页面获取信息
class InfoGetter:
    def __init__(self, session):
        self.session = session

    # 还得有些步骤才能进入
    def get_in_xuanke(self):
        data = {"name": "", "type": "button", "value": " 进入选课 "}
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/json'
        }
        res = self.session.post("https://webvpn.bupt.edu.cn/wengine-vpn/input", data=json.dumps(data), headers=headers)
        # logger.info("进入选课页面结果:" + str(res.status_code)+"\n"+res.text)
        res = self.session.get(
            "https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxk/xsxk_index?jx0502zbid=FE81621AE8DC45C18202DB2101EFB209")
        if "选课结果查看及退选" in res.text:
            logger.info("进入选课页面成功")

    def get_info(self, start, url, category):
        data = {
            'sEcho': '1',
            'iColumns': '11',
            'sColumns': '',
            'iDisplayStart': str(start),
            'iDisplayLength': '15',
            'mDataProp_0': 'kch',
            'mDataProp_1': 'kcmc',
            'mDataProp_2': 'fzmc',
            'mDataProp_3': 'ktmc',
            'mDataProp_4': 'xf',
            'mDataProp_5': 'skls',
            'mDataProp_6': 'sksj',
            'mDataProp_7': 'skdd',
            'mDataProp_8': 'xqmc',
            'mDataProp_9': 'ctsm',
            'mDataProp_10': 'czOper'
        }
        response = self.session.post(url, data=data)
        result = re.sub(r"\n", "", response.text)
        result = json.loads(re.sub("<script>.*</script>", "", result))
        logger.info(f"{category}选课信息:" + str(result))
        for ke in result['aaData']:
            # 原谅我为了记忆使用中文变量名
            课程编号 = ke['kch']
            课程名称 = ke['kcmc']
            分组名 = ke['fzmc']
            合班名称 = ke['ktmc']
            学分 = ke['xf']
            上课老师 = ke['skls']
            上课时间 = ke['sksj']
            上课地点 = ke['skdd']
            上课校区 = ke['xqmc']
            时间冲突 = ke['ctsm']
            kcid = ke["jx02id"]
            jxid = ke["jx0404id"]
            logger.info(
                [课程编号, 课程名称, 分组名, 合班名称, 学分, 上课老师, 上课时间, 上课地点, 上课校区, 时间冲突, kcid,
                 jxid])
            with open(f"{category}选课信息.csv", "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [课程编号, 课程名称, 分组名, 合班名称, 学分, 上课老师, 上课时间, 上课地点, 上课校区, 时间冲突, kcid,
                     jxid])
        total = max(result['iTotalRecords'], result['iTotalDisplayRecords'])
        if start + 15 < total:
            self.get_info(start+15, url, category)

    # 选修选课信息
    def get_xuanxiu(self):
        start = 0
        with open("选修选课信息.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["课程编号", "课程名称", "分组名", "合班名称", "学分", "上课老师", "上课时间", "上课地点", "上课校区",
                 "时间冲突", "kcid", "jxid"])
        data = {
            'sEcho': '1',
            'iColumns': '11',
            'sColumns': '',
            'iDisplayStart': str(start),
            'iDisplayLength': '15',
            'mDataProp_0': 'kch',
            'mDataProp_1': 'kcmc',
            'mDataProp_2': 'fzmc',
            'mDataProp_3': 'ktmc',
            'mDataProp_4': 'xf',
            'mDataProp_5': 'skls',
            'mDataProp_6': 'sksj',
            'mDataProp_7': 'skdd',
            'mDataProp_8': 'xqmc',
            'mDataProp_9': 'ctsm',
            'mDataProp_10': 'czOper'
        }
        url = 'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/xsxkXxxk'
        self.get_info(start, url=url, category="选修")
        logger.success("选修选课信息已输出为csv文件")

    # 公选课选课信息
    def get_public_course(self):
        start = 0
        with open("公选课选课信息.csv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["课程编号", "课程名称", "分组名", "合班名称", "学分", "上课老师", "上课时间", "上课地点", "上课校区",
                 "时间冲突", "kcid", "jxid"])
        url = 'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/xsxkGgxxkxk'
        self.get_info(start, url=url, category="公选课")
        logger.success("公选课选课信息已输出为csv文件")


class ChooseCourseHelper:
    def __init__(self, session):
        self.session = session

    def choose_course(self, kcid: str, jxid: str):
        params = {
            'vpn-12-o2-jwgl.bupt.edu.cn': '',
            'kcid': kcid,
            'cfbs': "null",
            'jx0404id': jxid,
            'xkzy': '',
            'trjf': '',
            '_': str(int(time.time() * 1000))
        }
        response = self.session.get(
            'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/xxxkOper',
            params=params)
        if "错误" in response.text:
            response = self.session.get(
            'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/ggxxkxkOper',
            params=params)
        logger.info("选课结果:" + response.json()["message"])

    def unchoose_course(self, jxid: str):
        params = {
            'vpn-12-o2-jwgl.bupt.edu.cn': '',
            'jx0404id': jxid,
            'tkyy': '',
            '_': str(int(time.time() * 1000)),
        }
        response = self.session.get(
            'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkjg/xstkOper',
            params=params)
        logger.info("退课结果:" + response.json()["success"])


if __name__ == '__main__':
    # session = httpx.Client(trust_env=True)
    session = requests.Session()
    lh = LoginHelper(session=session)
    ig = InfoGetter(session=session)
    cc = ChooseCourseHelper(session=session)
    lh.vpn_login(2022212288, "WenHao0425")
    lh.edu_login("2022212288", "20040425")
    ig.get_in_xuanke()
    # ig.get_xuanxiu()
    # ig.get_public_course()
    while True:
        try:
            kcid = input("请输入需要选课的kcid:")
            if kcid == ":q":
                break
            jxid = input("请输入需要选课的jxid:")
            if jxid == ":q":
                break
            cc.choose_course(kcid, jxid)
        except:
            kcid = input("请输入需要选课的kcid:")
            if kcid == ":q":
                break
            jxid = input("请输入需要选课的jxid:")
            if jxid == ":q":
                break
            cc.choose_course(kcid, jxid)
