from hashlib import md5

obj = md5()
obj.update(b"Hello World")
result = obj.hexdigest()  # 32位16进制
print(result)

