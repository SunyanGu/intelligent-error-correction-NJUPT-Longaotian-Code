import jieba


f = open('./fenci_fullmode2.txt','w')
f2 = open('./test.txt','r')


# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# a = "/ ".join(seg_list)
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print(a)
# f.write(a)

for i in f2:
    seg_list = jieba.cut(i,cut_all=True)
    a = "/ ".join(seg_list)
    print(a)
    f.write(a)
    f.write('\n')
    f.flush()