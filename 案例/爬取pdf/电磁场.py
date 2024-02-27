import requests

session = requests.Session()
session.headers = {
    'authority': 'wqbook.wqxuetang.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'cookie': 'gidf=b67af69f024eeb2bb79ed073e8b328e9; _gid=1762065271813574656; _gidv=1a125f67fc99fa7175bc9163a4fab68c; SERVERID=6fc737dbf667df8d4b087cce0d5a7f68|1708948253|1708948212; SERVERCORSID=6fc737dbf667df8d4b087cce0d5a7f68|1708948253|1708948212',
    'referer': 'https://wqbook.wqxuetang.com/deep/m/read/pdf?bid=12311',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

params = (
    ('bid', '12311'),
    ('pnum', '24'),
    ('k', 'eyJ1IjoiM3MvdjBkVFozbTA9IiwiaSI6IlpwZGNLeW9NcUM0SEp5UFhGVXJ1a1NOYzZ6TmRHT3RjTXpHdnAzUDBMdlJhUFlzRmdyYms4UT09IiwidCI6Inh6dytCWEN2bVFUeDkrbHR1NEppT1E9PSIsImIiOiJZTU55Sk1MeEpWST0iLCJuIjoic1U2NEE4MGVtL2s9IiwicyI6IjNzL3YwZFRaM20wPSIsImQiOiJVSkVtbWRGeFVNQ0FhUXg5SW9RTXNjQVI0cXFjUkhjVEFCVWFoMDY5Q1I4TWtaYTlPdDhxODZLZ3k0ajZSc2JHIiwieCI6ImlmOVpKVlA5cHlyNTlRQUhDSnlNZGQ2Sy8yM0FhYWh2TDNuWEpxNzZUbERVTHJSU2N4ZnRSdz09In0='),
)

response = session.get('https://wqbook.wqxuetang.com/deep/v1/positions/page', params=params)
print(response.text)
response = session.get("https://wqbook.wqxuetang.com/deep/page/once/get?pnum=30&bid=12311&k=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwIjozMCwidCI6MTcwODk1MDMzNjAwMCwiYiI6MTIzMTEsInciOjEwMDAsImsiOiJ7XCJ1XCI6XCIzcy92MGRUWjNtMD1cIixcImlcIjpcIlpwZGNLeW9NcUM0SEp5UFhGVXJ1a1NOYzZ6TmRHT3RjTXpHdnAzUDBMdlJhUFlzRmdyYms4UT09XCIsXCJ0XCI6XCJ6azVJSmVvd0lQNml1RkJMNmZmL213PT1cIixcImJcIjpcIllNTnlKTUx4SlZJPVwiLFwiblwiOlwic1U2NEE4MGVtL2s9XCIsXCJzXCI6XCIzcy92MGRUWjNtMD1cIixcImRcIjpcIlVKRW1tZEZ4VU1DQWFReDlJb1FNc2NBUjRxcWNSSGNUQUJVYWgwNjlDUjhNa1phOU90OHE4NktneTRqNlJzYkdcIixcInhcIjpcIk94dE5VQlB5dGUyczJrSitZQmQxN0psZDVGZTJsSW9hZW5Zamo1Qk1nNld6ZjcwcHJEU0hkUT09XCJ9Iiwiem4iOjEsImlhdCI6MTcwODk1MDMzNn0.yZ61eRFKGb-FdY8eLVPGPw9nbX7HzkTAcXj8hditGRY")
print(response.text)