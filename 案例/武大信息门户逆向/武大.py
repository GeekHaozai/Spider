import base64
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = "Lfv6VSaZZ1COibHO"

def rds(length: int):
    chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    ret_str = ""
    for i in range(length):
        ret_str += chars[random.randint(0, len(chars) - 1)]
    return ret_str


def gas(data, key0, iv0):
    key0 = key0.strip()
    aes = AES.new(key=key0.encode(), mode=AES.MODE_CBC, iv=iv0.encode())
    enc_pwq = aes.encrypt(pad(data.encode('utf-8'), 16))
    print(base64.b64encode(enc_pwq).decode('utf-8'))
    return base64.b64encode(enc_pwq).decode('utf-8')

def enc_pwd(pwd):
    return gas(rds(64) + pwd, key, rds(16))

pwd = "123456"
print(enc_pwd(pwd))




