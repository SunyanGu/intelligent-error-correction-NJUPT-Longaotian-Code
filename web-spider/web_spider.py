from baidu_spider import baike_list,header
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
import time
import pymongo



# print(len(url_list))
# print(len(set(url_list)))

# for url in set(url_list):
#     web_page = requests.get(url,headers = header)
#     web_page.encoding = 'utf-8'
#     soup = BeautifulSoup(web_page.text, 'lxml')
#     title = soup.title.text
#     print(title[:-5])
#     a = open('D:\研究生课题\自然语言处理\百度百科爬虫\文本{}.txt'.format(title[:-5]),'w')
#     total = soup.select('.main-content')
#     for i in total:
#         a.write(i.text)

def web_spider(url):
    try:
        web_page = requests.get(url,headers = header)
        time.sleep(0.5)
        web_page.encoding = 'utf-8'
        soup = BeautifulSoup(web_page.text, 'lxml')
        title = soup.title.text
        print(title[:-5])
        # a = open('D:\研究生课题\自然语言处理\百度百科爬虫\文本\{}.txt'.format(title[:-5]),'w')
        total = soup.select('.main-content')[0]
        baike.insert_one({'url':url.strip(),'title':title,'content':total.text})
    except:
        pass

#主函数
if __name__ == "__main__":


    Client = pymongo.MongoClient('localhost', 27017)
    baidu = Client['baidu']
    baike = baidu['baike']
    baike_url2 = baidu['baike_url2']
    baike_url = baidu['baike_url']

    baidubaike_list = []
    for i in baike.find():
        baidubaike_list.append(i['url'])

    url_list = []
    for i in baike_url2.find():
        url_list.append(i['url'])

    print('start')
    spider_list = set(url_list) - set(baidubaike_list)

    print(baike_url.count())
    print(len(set(url_list)))
    print(len(set(baidubaike_list)))
    print(len(spider_list))


    #初始化进程池
    pool = Pool()
    #多进程爬取
    pool.map(web_spider,spider_list)
    pool.close()
    pool.join()



# Client = pymongo.MongoClient('localhost', 27017)
# baidu = Client['baidu']
# baike = baidu['baike']
#
# for i in baike.find():
#     print(i)