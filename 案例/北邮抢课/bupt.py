import json
import prettytable
import httpx
from loguru import logger
import requests
import re

class LoginHelper:
    def __init__(self, session):
        self.session = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        self.session.headers = self.headers

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


# 进入选课页面获取信息
class InfoGetter:
    def __init__(self, session):
        self.session = session

    # 还得有些步骤才能进入
    def get_in_xuanke(self):
        data = {"name":"","type":"button","value":" 进入选课 "}
        headers = {
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Content-Type': 'application/json'
        }
        res = self.session.post("https://webvpn.bupt.edu.cn/wengine-vpn/input",data=json.dumps(data),headers=headers)
        # logger.info("进入选课页面结果:" + str(res.status_code)+"\n"+res.text)
        res = self.session.get("https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxk/xsxk_index?jx0502zbid=FE81621AE8DC45C18202DB2101EFB209")
        if "选课结果查看及退选" in res.text:
            logger.info("进入选课页面成功")


    # 选修选课
    def get_xuanxiu(self):
        start = 0
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

        response = session.post(
            'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/xsxkXxxk',data=data)
        logger.info("选修选课信息:" + str(response.json()))
        table = prettytable.PrettyTable(
            ['课程编号', '课程名称', '分组名', '合班名称', '学分', '上课老师', '上课时间', '上课地点', '上课校区',
             '时间冲突'])
        for ke in response.json()['aaData']:
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
            table.add_row([课程编号, 课程名称, 分组名, 合班名称, 学分, 上课老师, 上课时间, 上课地点, 上课校区, 时间冲突])
        total = max(response.json()['iTotalRecords'], response.json()['iTotalDisplayRecords'])
        start += 15
        while start<total:
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
            response = session.post(
                'https://webvpn.bupt.edu.cn/https/77726476706e69737468656265737421fae0469069327d406a468ca88d1b203b/jsxsd/xsxkkc/xsxkXxxk',
                data=data)
            result = re.sub(r"\n", "", response.text)
            result = re.sub("<script>.*</script>", "", result).replace(" ","").replace("<br>","\n")
            json_res = json.loads(result)
            logger.info("选修选课信息:" + str(json_res))
            table = prettytable.PrettyTable(
                ['课程编号', '课程名称', '分组名', '合班名称', '学分', '上课老师', '上课时间', '上课地点', '上课校区',
                 '时间冲突'])
            for ke in json_res['aaData']:
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
                table.add_row(
                    [课程编号, 课程名称, 分组名, 合班名称, 学分, 上课老师, 上课时间, 上课地点, 上课校区, 时间冲突])
            start += 15
        table.align = "c"
        print(table)

class ChooseCourseHelper:
    def __init__(self, session):
        self.session = session


if __name__ == '__main__':
    # session = httpx.Client(trust_env=True)
    session = requests.Session()
    lh = LoginHelper(session=session)
    ig = InfoGetter(session=session)
    cc = ChooseCourseHelper(session=session)
    lh.vpn_login(2022212288, "WenHao0425")
    lh.edu_login("2022212288", "20040425")
    ig.get_in_xuanke()
    ig.get_xuanxiu()
