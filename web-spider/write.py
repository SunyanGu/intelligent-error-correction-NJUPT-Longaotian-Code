import pymongo
import re

Client = pymongo.MongoClient('localhost', 27017)
baidu = Client['baidu']
baike = baidu['baike']
baike_url = baidu['baike_url']
print(baike.count())

f = open('./test.txt','w')

for i in baike.find():
    #print(i['content'])
    a = i['content'].split()
    for j in a:
        if len(j) > 10:
            b = re.sub('\\\|[a-zA-Z]|\[|\]|\"|\"|:|\)|\(|\.|\{|\};','',j)
            b = re.sub('[0-9][0-9][0-9][0-9][0-9][0-9]+','',b)
            b = re.sub('\d{4}年\d+月\d+日','',b)
            #print(b)
            if len(b)>10:
                print(b)
                try:
                    f.write(b)
                except:
                    print('asdf')
                f.write('\n')
                f.flush()
