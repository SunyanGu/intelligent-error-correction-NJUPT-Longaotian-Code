import collections

# f = open('./start_list2.txt','r')
# f1 = open('./word_word_num3.txt','r')
# f2 = open('./new_trans.txt','w')
# word_list = []
# word_dict = collections.defaultdict(lambda :str(0.0))
#
# for i in f:
#     a = i.strip().split()
#     word_list.append(a[0])
#
# for i in f1:
#     a = i.strip().split()
#     word_dict[a[0]+a[1]] = a[2]
# for i in word_list:
#     for j in word_list:
#         f2.write(i + ' '+j + ' '+word_dict[i+j])
#         f2.write('\n')

import time
# def create_pinyin_word_dict():
#     f = open('./word_pinyin_num2.txt','r')
#     #f2 = open('./word_pinyin_dict','w')
#     pinyin_word_dict = collections.defaultdict(lambda :[])
#     for i in f:
#         a = i.strip().split()
#         pinyin_word_dict[a[1]].append(a[0])
#     #print(pinyin_word_dict)
#
#     return pinyin_word_dict
# start = time.time()
# create_pinyin_word_dict()
# print(time.time() - start)
# def create_word_score_dict():
#     f = open('./start_list2.txt','r')
#     word_score_dict = {}
#     for i in f:
#         a = i.strip().split()
#         word_score_dict[a[0]] = a[1]
#     print(word_score_dict)
#     return word_score_dict
# start = time.time()
# create_word_score_dict()
# print(time.time() - start)