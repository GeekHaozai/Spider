import requests

def rss(session:requests.Session):
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows'
    pass

session = requests.Session()
rss(session)
print(session.headers)