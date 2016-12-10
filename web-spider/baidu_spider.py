import requests
from bs4 import BeautifulSoup
import pymongo
import re



baidu_baike_url = 'http://baike.baidu.com/'

header ={'Cookie':'pgv_pvi=6360424448; pgv_si=s9654364160; BDRCVFR[eZLhj6h0pMs]=mbxnW11j9Dfmh7GuZR8mvqV; BAIDUID=5A8A31B2EF21B08CF496323589D7615E:FG=1; BIDUPSID=1DCC9FED944475A796BF9CB2AF004435; PSTM=1466592037; H_PS_PSSID=18285_1453_19033_20317_18280_20368_17944_20388_19690_20415_19861_15082_11985; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1466590792; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1466592068',
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}

web_page = requests.get(baidu_baike_url,headers = header)
web_page.encoding = 'utf-8'
soup = BeautifulSoup(web_page.text,'lxml')
total = soup.select('.column')
total_list = []
for i in total:
    #print(i)
    total_list.extend(re.findall('href=\"(.*?)\"',str(i),re.S))
#print(total_list)

baike_list = ['/fenlei/%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9', '/fenlei/%E5%8E%86%E5%8F%B2%E4%BA%BA%E7%89%A9', '/fenlei/%E6%96%87%E5%8C%96%E4%BA%BA%E7%89%A9', '/fenlei/%E8%99%9A%E6%8B%9F%E4%BA%BA%E7%89%A9', '/fenlei/%E7%BB%8F%E6%B5%8E%E4%BA%BA%E7%89%A9', '/fenlei/%E8%AF%9D%E9%A2%98%E4%BA%BA%E7%89%A9', '/fenlei/%E5%8A%A8%E7%89%A9', '/fenlei/%E6%A4%8D%E7%89%A9', '/fenlei/%E8%87%AA%E7%84%B6%E7%81%BE%E5%AE%B3', '/fenlei/%E8%87%AA%E7%84%B6%E8%B5%84%E6%BA%90', '/fenlei/%E8%87%AA%E7%84%B6%E7%8E%B0%E8%B1%A1', '/fenlei/%E7%BE%8E%E6%9C%AF', '/fenlei/%E6%88%8F%E5%89%A7', '/fenlei/%E8%88%9E%E8%B9%88', '/fenlei/%E6%91%84%E5%BD%B1', '/fenlei/%E6%9B%B2%E8%89%BA', '/fenlei/%E4%B9%A6%E7%94%BB', '/fenlei/%E5%BB%BA%E7%AD%91', '/fenlei/%E8%AF%AD%E8%A8%80', '/fenlei/%E4%BD%93%E8%82%B2%E7%BB%84%E7%BB%87', '/fenlei/%E4%BD%93%E8%82%B2%E5%A5%96%E9%A1%B9', '/fenlei/%E4%BD%93%E8%82%B2%E8%AE%BE%E6%96%BD', '/fenlei/%E4%BD%93%E8%82%B2%E9%A1%B9%E7%9B%AE', '/fenlei/%E7%BB%84%E7%BB%87%E6%9C%BA%E6%9E%84', '/fenlei/%E6%94%BF%E6%B2%BB', '/fenlei/%E5%86%9B%E4%BA%8B', '/fenlei/%E6%B3%95%E5%BE%8B', '/fenlei/%E6%B0%91%E6%97%8F', '/fenlei/%E4%BA%A4%E9%80%9A', '/fenlei/%E7%BB%8F%E6%B5%8E', '/fenlei/%E5%90%84%E5%9B%BD%E5%8E%86%E5%8F%B2', '/fenlei/%E5%8E%86%E5%8F%B2%E4%BA%8B%E4%BB%B6', '/fenlei/%E5%8E%86%E5%8F%B2%E8%91%97%E4%BD%9C', '/fenlei/%E6%96%87%E7%89%A9%E8%80%83%E5%8F%A4', '/fenlei/%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92', '/fenlei/%E5%9C%B0%E5%BD%A2%E5%9C%B0%E8%B2%8C', '/fenlei/%E7%A7%91%E7%A0%94%E6%9C%BA%E6%9E%84', '/fenlei/%E4%BA%92%E8%81%94%E7%BD%91', '/fenlei/%E8%88%AA%E7%A9%BA%E8%88%AA%E5%A4%A9', '/fenlei/%E5%8C%BB%E5%AD%A6', '/fenlei/%E7%94%B5%E5%AD%90%E4%BA%A7%E5%93%81', '/fenlei/%E5%8A%A8%E6%BC%AB', '/fenlei/%E7%94%B5%E5%BD%B1', '/fenlei/%E7%94%B5%E8%A7%86%E5%89%A7', '/fenlei/%E5%B0%8F%E8%AF%B4', '/fenlei/%E7%94%B5%E8%A7%86%E8%8A%82%E7%9B%AE', '/fenlei/%E6%BC%94%E5%87%BA', '/fenlei/%E7%BE%8E%E5%AE%B9', '/fenlei/%E6%97%B6%E5%B0%9A', '/fenlei/%E6%97%85%E6%B8%B8']
#print(len(baike_list))

