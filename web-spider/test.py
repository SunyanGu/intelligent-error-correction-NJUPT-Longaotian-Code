from baidu_spider import baike_list
import requests
from bs4 import BeautifulSoup
import pymongo
import re
#
# classify_list = []
# for i in baike_list:
#     classify_list.append('http://baike.baidu.com'+i)
#
# web_page = requests.get('http://baike.baidu.com/view/27948.htm')
# web_page.encoding = 'utf-8'
# soup = BeautifulSoup(web_page.text,'lxml')
# title = soup.title.text
# print(title[:-5])
# total = soup.select('.main-content')
# for i in total:
#
#     print(i.text)

Client = pymongo.MongoClient('localhost', 27017)
baidu = Client['baidu']
baike = baidu['baike']
baike_url2 = baidu['baike_url2']

print(baike.count())
print(baike_url2.count())

# for i in baike.find():
#     print(i)