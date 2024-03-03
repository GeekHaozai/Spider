import smtplib
import datetime
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.application import MIMEApplication


def send_mail(email_title,book_info):
    # 接收人
    areceiver = "1700118540@qq.com"

    # 抄送人，多个抄送人用逗号隔开
    acc = ["270006718@qq.com"]

    # 邮件主题
    asubject = email_title

    # 发送人
    from_addr = "1700118540@qq.com"

    # 邮箱授权码
    password = "ribszzbgguyddffc"

    msg = MIMEMultipart()
    msg["subject"] = Header(asubject, "utf-8")
    msg["to"] = areceiver
    msg["Cc"] = ','.join(acc)
    msg["from"] = "1700118540@qq.com"

    # 文件内容
    body = book_info
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # # 添加附件，可以是word、excel、图片
    # woword = MIMEApplication(open(path_new, "rb").read(), "base64")
    #
    # # 重要：防止文件变成乱码bin文件，此列必须添加
    # woword.add_header("Content-Disposition", "attachment", "文件名" + ".docx")
    # msg.attach(woword)

    # 发送qq
    smtp_server = "smtp.qq.com"
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    server.sendmail(from_addr, areceiver.split(",") + acc, msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_mail()