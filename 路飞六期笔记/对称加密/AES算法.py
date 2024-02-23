# pip install pycryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
# CBC , IV16字节
aes = AES.new(b'1234567891234567', mode=AES.MODE_CBC, IV=b'1234567890123456')
dec_aes = AES.new(b'1234567891234567', mode=AES.MODE_CBC, IV=b'1234567890123456')
# ECB
# aes_ecb = AES.new('This is a key', mode=AES.MODE_ECB)
s = "我喜欢你".encode("utf-8")
bs = pad(s,16)
enc_text = aes.encrypt(bs)
print(base64.b64encode(enc_text).decode('utf-8'))
final = base64.b64encode(enc_text).decode('utf-8')

# 解密
dec_text = dec_aes.decrypt(base64.b64decode(final.encode("utf-8")))
dec_text = unpad(dec_text,16)
print(dec_text.decode("utf-8"))

# 如果遇到16进制的iv，需要转换成bytes(16进制转换为ascii，比如64就是十进制100，对应‘d'，两个16进制对应一个ascii)
# ascii是一个字节，但是只用了前0-127个编码，后面的是扩展ascii，也就是16进制00-7f是可打印ascii，80-ff是不可打印ascii
import binascii
b = binascii.a2b_hex("64642183")
print(b)