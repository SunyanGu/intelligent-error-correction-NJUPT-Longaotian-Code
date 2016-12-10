from baidu_spider import baike_list,header
import requests
from bs4 import BeautifulSoup

classify_list = []
num = 0
classify_list_all = []
for i in baike_list:
    classify_list.append('http://baike.baidu.com'+i)
# print(classify_list)
f = open('./url.txt','w')

for url in classify_list:
    for i in range(1,1000):
        url_next = url + '?index={}'.format(i)
        web_page = requests.get(url_next,headers = header)
        soup = BeautifulSoup(web_page.text,'lxml')
        if soup.select('.page') == []:
            classify_list_all.append(url_next)
            f.write(str(url_next))
            f.write('\n')
            f.flush()
            break
        elif soup.find(id='next-span') == None:
            classify_list_all.append(url_next)
            f.write(str(url_next))
            f.write('\n')
            f.flush()
            #print(len(classify_list_all))
        else:
            classify_list_all.append(url_next)
            f.write(str(url_next))
            f.write('\n')
            f.flush()
            break
print(classify_list_all)




