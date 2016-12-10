import pymongo


Client = pymongo.MongoClient('localhost', 27017)
baidu = Client['baidu']
baike = baidu['baike']
baike_url = baidu['baike_url']
print(baike.count())

# for i in baike.find():
#     baike_url.insert_one({'url':i['url']})


for i in baike.find():
    a = len(i['content'])
    #print(a)
    if a < 400:
        print(i['url'])
        baike.remove({'_id':i['_id']})
print(baike.count())
