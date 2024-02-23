import base64

str1 = "你好啊"
base_str1 = base64.b64encode(str1.encode("utf-8")).decode()  # 一定是4的倍数
print(base_str1)
print(base64.b64decode(base_str1.encode()).decode("utf-8"))
print(base64.b64decode(base_str1).decode("utf-8"))