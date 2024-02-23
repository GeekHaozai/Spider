from urllib.parse import quote, quote_plus, urlencode, unquote, unquote_plus, urljoin

a = urlencode({"a": "我是谁"})
b = quote("我是谁")
c = quote_plus("我是谁")
print(a, b, c)
base_url = "https://www.baidu.com/s/a"
u1 = "c/d/e.html"
u2 = "/c/d/e.html"
print(urljoin(base_url, u1))
print(urljoin(base_url, u2))