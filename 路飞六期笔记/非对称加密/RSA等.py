from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

# key = RSA.generate(2048)
# private_key = key.export_key()
# print(private_key.decode('utf-8'))
# with open('private.pem', 'wb') as f:
#     f.write(private_key)
# public_key = key.publickey().export_key()
# with open('public.pem', 'wb') as f:
#     f.write(public_key)
# print(public_key.decode('utf-8'))

public_ley = RSA.importKey(open('public.pem').read())  # 可以导入字节也可以导入字符串
rsa = PKCS1_v1_5.new(key=public_ley)
enc = rsa.encrypt("我喜欢你".encode('utf-8'))
result = base64.b64encode(enc).decode('utf-8')
print(result)  # 不是纯数学算法的话每次结果都掺杂随机的东西所以每次都不相同