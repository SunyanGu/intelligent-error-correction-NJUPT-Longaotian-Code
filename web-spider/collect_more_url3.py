from baidu_spider import baike_list,header
import requests
from bs4 import BeautifulSoup
import pymongo
import re

Client = pymongo.MongoClient('localhost', 27017)
baidu = Client['baidu']
baike_url = baidu['baike_url']
baike_url2 = baidu['baike_url2']

url_list = []

for i in baike_url.find():
    url_list.append(i['url'])


for url in list(set(url_list))[40000:]:
    web_page = requests.get(url,headers = header)
    web_page.encoding = 'utf-8'
    soup = BeautifulSoup(web_page.text, 'lxml')
    total = soup.select('.main-content')
    for i in total:
        a = re.findall(r'href="/view/(.*?)"', str(i), re.S)
        if len(a) == 0:
            pass
        else:
            for j in a:
                print(j)
                p = 'http://baike.baidu.com/view/' + j
                baike_url2.insert_one({'url': p})
# for i in baike_url.find():
#     url_list.append(i['url'])
# print(len(set(url_list)))
# print(baike_url.count())