from baidu_spider import baike_list,header
import requests
from bs4 import BeautifulSoup
import pymongo
import re

f1 = open('./url_more.txt','r')
f2 = open('./url_more2.txt','w')

url_list = []
for url in f1:
    url_list.extend(url.split())
for url in url_list:
    url2 = 'http://baike.baidu.com' + url
    web_page = requests.get(url2,headers = header)
    web_page.encoding = 'utf-8'
    soup = BeautifulSoup(web_page.text, 'lxml')
    total = soup.select('.main-content')
    for i in total:
        a = re.findall(r'href="/view/(.*?)"', str(i), re.S)
        if len(a) == 0:
            pass
        else:
            for j in a:
                print('http://baike.baidu.com/view/' + j)
                f2.write(j)
                f2.write('\n')
                f2.flush()