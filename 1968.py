import requests
from bs4 import BeautifulSoup
import json

link1968 = "https://1968.freeway.gov.tw/api/getIncidentData?"
parmas = {'action': 'incident', 'area': 'A', 'freewayid': '1', 'expresswayid': '0'}
headers = '''
GET /api/getIncidentData?action=incident&area=A&freewayid=1&expresswayid=0 HTTP/1.1
Host: 1968.freeway.gov.tw
Connection: keep-alive
sec-ch-ua: " Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"
Accept: */*
X-Requested-With: XMLHttpRequest
sec-ch-ua-mobile: ?1
User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://1968.freeway.gov.tw/n_notify
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: gacid=2645ab48-8c41-4dfc-b492-4ebe55f26f99; 1968_session=eyJpdiI6IlRHRWZDQ0RkaFwvOTBiaWtINlVaY1h3PT0iLCJ2YWx1ZSI6ImJsRFhlaEEyUm12NEFjZlZwekRNZFlOWXdwTlNnTXRrKzkzbjJCNWxITFlvK2ZLckl1ZEJEWDF5VlFvN01ic0siLCJtYWMiOiJmZDQxYTNjMGQ1OWViOGFiNDQyMGQ3MzlmZDA4NDI1NDVlZTc5OWZhZGQ0ZmI3ZDE4N2Q1MzM2YzJlZTgwYzMyIn0%3D
'''


def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


headers = str2obj(headers, '\n', ': ')


crawler = requests.get(link1968, params=parmas, headers=headers)
get_all = BeautifulSoup(crawler.text, 'html.parser')
print(json.loads(get_all.text))
with open("1968_crawler.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(json.loads(get_all.text), ensure_ascii=False, indent=2))  # ensure_ascii 不要將原始中文編碼  #indent 按照指定格式縮進
