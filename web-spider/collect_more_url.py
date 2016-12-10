from baidu_spider import baike_list,header
import requests
from bs4 import BeautifulSoup
import pymongo
import re

f = open('./url.txt','r')
f1 = open('./url_more.txt','w')

url_list = []
for url in f:
    url_list.extend(url.split())
for url in url_list:
    web_page = requests.get(url,headers = header)
    web_page.encoding = 'utf-8'
    soup = BeautifulSoup(web_page.text, 'lxml')
    href = soup.select('.list')
    for i in href:
        f1.write(re.findall(r'class="title nslog:7450" href="(.*?)"',str(i),re.S)[0])
        f1.write('\n')
        f1.flush()