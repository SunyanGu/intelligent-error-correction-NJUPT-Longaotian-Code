
import re
import collections
import jieba
import time
import pypinyin
class _2_gram_model(object):
    def __init__(self,sentence):
        self.homophonesPath = './Homophones.txt'
        self.stopWordPath2 = './stopword.txt'
        self._1_gramePath = './_1_Gram_stop4.txt'
        self.filepath = './duizhaobiao.txt'
        self.sentence = sentence
        self.specialword = './special_word3.txt'

    def create_word_list(self):
        word_list = []
        word_list2 = []


        sentence = self.sentence.replace('/','')
        sentence = 'begin.'+ sentence +'end'
        seg_list = jieba.cut(sentence, cut_all=False)
        stop_list2 = [line.strip() for line in open(self.stopWordPath2,'r').readlines()]

        a = "/ ".join(seg_list)
        a = a.split('/')
        for i in a:
            if i.strip() not in stop_list2:
                word_list.append(i.strip())
            else:
                pass
        for i in word_list:
            num = re.sub('[0-9]+','number',i)
            word_list2.append(num)
        return word_list2

    def create_word_list_original(self):
        word_list = []
        seg_list = jieba.cut(self.sentence, cut_all=False)
        a = "/ ".join(seg_list)
        a = a.split('/')
        for i in a:
            word_list.append(i.strip())
        return word_list

    def creat_homophones_list(self):
        spell_list = []
        f = open(self.homophonesPath, 'r')
        for i in f:
            a = i.strip().split('    ')
            spell_list.append(a[0])
        return spell_list

    def is_have_homophones(self,word):
        word_str = ''
        spell_list = self.creat_homophones_list()
        word = re.findall('[\u4E00-\u9FA5]+|B|E',word, re.S)

        if word != []:
            word_pinyin = pypinyin.lazy_pinyin(word[0])
            for i in word_pinyin:
                word_str += i + ' '
            if word_str.strip() in spell_list:
                return word_str.strip()
            else:
                return False
        else:
            return False

    def create_homophones_dict(self):
        homophonesTable = open(self.homophonesPath,'r')
        homophonesDict = collections.defaultdict(lambda :[])
        for i in homophonesTable:
            homophonesList = i.strip().split('    ')
            for j in range(1,len(homophonesList)):
                homophonesDict[homophonesList[0]].append(homophonesList[j])
        return homophonesDict

    def create_dual_character(self):
        word_list = self.create_word_list()
        Three_word_list = []
        for i in range(1,len(word_list)-1):
            Three_word_list.append([word_list[i-1]] + [word_list[i]] + [word_list[i+1]])
        return Three_word_list

    def create_dual_list(self):
        Three_word_list = self.create_dual_character()
        homophonesDict1 = self.create_homophones_dict()
        homophonesDict = collections.defaultdict(lambda :[])
        synonymy_match = collections.defaultdict(lambda :[])

        for i in Three_word_list:
            word_spell = self.is_have_homophones(i[1])
            if word_spell != False:
                homophonesDict[i[1]] = homophonesDict1[word_spell]
        for j in Three_word_list:
            for item in homophonesDict[j[1]]:
                synonymy_match[j[1]].append([j[0]]+[item]+[j[2]])
        return synonymy_match

    def create_1_gram_dict(self):
        f = open(self._1_gramePath,'r')
        _1_gram_dict = collections.defaultdict(lambda :1)
        for i in f:
            a = i.strip().split()
            _1_gram_dict[a[0]] = a[1]
        return _1_gram_dict

    def is_change(self,num_word_w_sub, num_word_w_plus, num_word2_w_sub, num_word2_w_plus,num_word_first,num_word,num_word2):
        P_word = float(num_word_w_sub)/float(num_word_first)*float(num_word_w_plus)/float(num_word)
        P_word2 = float(num_word2_w_sub)/float(num_word_first)*float(num_word2_w_plus)/float(num_word2)
        if P_word<P_word2:
            return True,P_word2
        else:
            return False,0.0

    def is_change2(self,num_word_w_sub,num_word_w_plus,num_word2_w_sub,num_word2_w_plus,num_word3_w_sub,num_word3_w_plus,num_word_first,num_word, num_word2,num_word3):
        P_word = float(num_word_w_sub)/float(num_word_first)*float(num_word_w_plus)/float(num_word)
        P_word2 = float(num_word2_w_sub)/float(num_word_first)*float(num_word2_w_plus)/float(num_word2)
        P_word3 = float(num_word3_w_sub)/float(num_word_first)*float(num_word3_w_plus)/float(num_word3)

        if P_word > P_word2 and P_word > P_word3:
            return 1,P_word
        elif P_word2 > P_word and P_word2 > P_word3:
            return 2,P_word2
        else:
            return 3,P_word3



    def calculate_word_max(self):
        synonymy_match = self.create_dual_list()
        w = collections.defaultdict(lambda :{})

        word_list = []
        for word,comb in list(synonymy_match.items()):
            w_sub_num = {}
            w_plus_num = {}
            for i in comb:
                w_sub = i[0]+i[1]
                w_plus = i[1]+i[2]
                if w_sub in _2_gram_dict:
                    w_sub_num[i[0]+ ' '+i[1]] = float(_2_gram_dict[w_sub])
                else:
                    w_sub_num[i[0]+ ' '+i[1]] = 0.0001

                if w_plus in _2_gram_dict:
                    w_plus_num[i[1]+ ' '+i[2]] = float(_2_gram_dict[w_plus])
                else:
                    w_plus_num[i[1]+ ' '+i[2]] = 0.0001

            for i,j in w_sub_num.items():
                word_list.append(i + '   '+str(j))
            for i,j in w_plus_num.items():
                word_list.append(i + '   '+str(j))

            w_sub_max =max(w_sub_num.items(), key=lambda x: x[1])
            w_plus_max =max(w_plus_num.items(), key=lambda x: x[1])

            w[word]['w_sub'] = w_sub_max
            w[word]['w_plus'] = w_plus_max
        return w,word_list

    def make_result(self):
        word_dict = collections.defaultdict(lambda:0.0001)
        result_dict = {}
        result_dict2 = collections.defaultdict(lambda:0.0)
        w, word_list = self.calculate_word_max()
        _1_gram_dict = self.create_1_gram_dict()
        for i in word_list:
            word_dict[i.split('   ')[0]] = i.split('   ')[1]
        for word1,word2 in w.items():     #还没有考虑到word2['w_plus'][0].split()[0] 和 word1 != word2['w_sub'][0].split()[1] 不想等的情况
            if word2['w_plus'][1] == 0.0001 and word2['w_sub'][1] == 0.0001:
                continue
            elif word1 != word2['w_plus'][0].split()[0] and word1 != word2['w_sub'][0].split()[1]:

                if word2['w_plus'][0].split()[0] != word2['w_sub'][0].split()[1]:
                    Word1_1 = word1 + ' ' + word2['w_plus'][0].split()[1]   #几分网页
                    Word1_2 = word2['w_sub'][0].split()[0] + ' ' + word1  #兑换几分
                    Word2  = word2['w_sub'][0].split()[0] + word2['w_plus'][0].split()[0] #兑换计分
                    Word3 = word2['w_sub'][0].split()[1] + word2['w_plus'][0].split()[1] #积分网页
                    num_word_w_sub = word_dict[Word1_2]
                    num_word_w_plus = word_dict[Word1_1]
                    num_word2_w_sub = word_dict[Word2]
                    num_word2_w_plus = word_dict[word2['w_plus'][0]]
                    num_word3_w_sub = word_dict[word2['w_sub'][0]]
                    num_word3_w_plus = word_dict[Word3]
                    num_word_first = _1_gram_dict[word2['w_sub'][0].split()[0]]  #兑换
                    num_word = _1_gram_dict[word1]   #几分
                    num_word2 = _1_gram_dict[word2['w_plus'][0].split()[0]]   #计分
                    num_word3 = _1_gram_dict[word2['w_sub'][0].split()[1]]  # 积分
                    number,P = self.is_change2(num_word_w_sub,num_word_w_plus,num_word2_w_sub,num_word2_w_plus,num_word3_w_sub,num_word3_w_plus,num_word_first,num_word, num_word2,num_word3)
                    if number == 2:
                        result_dict[word1] = word2['w_plus'][0].split()[0]
                        p = P
                        result_dict2[word2['w_plus'][0].split()[0]] = p
                    elif number == 3:
                        result_dict[word1] = word2['w_sub'][0].split()[1]
                        p = P
                        result_dict2[word2['w_sub'][0].split()[1]] = p

                else:
                    Word1 = word1+ ' ' +word2['w_plus'][0].split()[1]
                    Word2 = word2['w_sub'][0].split()[0] +' '+ word1
                    num_word_w_sub = word_dict[Word2]
                    num_word_w_plus = word_dict[Word1]
                    num_word2_w_sub = word_dict[word2['w_sub'][0]]
                    num_word2_w_plus = word_dict[word2['w_plus'][0]]
                    num_word_first = _1_gram_dict[word2['w_sub'][0].split()[0]]
                    num_word = _1_gram_dict[word1]
                    num_word2 = _1_gram_dict[word2['w_sub'][0].split()[1]]
                    is_change,P = self.is_change(num_word_w_sub, num_word_w_plus, num_word2_w_sub, num_word2_w_plus,num_word_first,num_word,num_word2)
                    if  is_change== True:
                        result_dict[word1] = word2['w_plus'][0].split()[0]
                        p = P
                        result_dict2[word2['w_plus'][0].split()[0]] = p

            elif word1 != word2['w_plus'][0].split()[0] and word1 == word2['w_sub'][0].split()[1]:
                Word1 = word1+ ' ' +word2['w_plus'][0].split()[1]
                Word2 = word2['w_sub'][0].split()[0] +' '+ word2['w_plus'][0].split()[0]
                num_word_w_sub = word_dict[word2['w_sub'][0]]
                num_word_w_plus = word_dict[Word1]
                num_word2_w_sub = word_dict[Word2]
                num_word2_w_plus = word_dict[word2['w_plus'][0]]
                num_word_first = _1_gram_dict[word2['w_sub'][0].split()[0]]
                num_word = _1_gram_dict[word1]
                num_word2 = _1_gram_dict[word2['w_plus'][0].split()[0]]
                is_change, P = self.is_change(num_word_w_sub, num_word_w_plus, num_word2_w_sub, num_word2_w_plus,num_word_first, num_word, num_word2)
                if is_change == True:
                    result_dict[word1] = word2['w_plus'][0].split()[0]
                    p = P
                    result_dict2[word2['w_plus'][0].split()[0]] = p

            elif word1 != word2['w_sub'][0].split()[1] and word1 == word2['w_plus'][0].split()[0]:
                Word1 = word2['w_sub'][0].split()[0] +' '+ word1
                Word2 = word2['w_sub'][0].split()[1]+ ' ' +word2['w_plus'][0].split()[1]
                num_word_w_sub = word_dict[Word1]
                num_word_w_plus = word_dict[word2['w_plus'][0]]
                num_word2_w_sub = word_dict[word2['w_sub'][0]]
                num_word2_w_plus = word_dict[Word2]
                num_word_first = _1_gram_dict[word2['w_sub'][0].split()[0]]
                num_word = _1_gram_dict[word1]
                num_word2 = _1_gram_dict[word2['w_sub'][0].split()[1]]
                is_change, P = self.is_change(num_word_w_sub, num_word_w_plus, num_word2_w_sub, num_word2_w_plus,num_word_first, num_word, num_word2)
                if is_change == True:
                    result_dict[word1] = word2['w_sub'][0].split()[1]
                    p = P
                    result_dict2[word2['w_sub'][0].split()[1]] = p

        for danzi in list(result_dict2.keys()):
            if len(danzi) == 1:
                result_dict2.pop(danzi)
        if result_dict2 != {}:
            result = max(result_dict2.items(),key=lambda x:x[1])
        else:
            result = ('None',0)
        return result

    def out_put_right_sentence(self):
        result_dict = self.make_result()
        word_list = self.create_word_list_original()
        right_sentence = ''
        for i in word_list:
            if i in result_dict:
                right_sentence += result_dict[i]
            else:
                right_sentence+=i


def create_2_gram_dict():
    f = open('./_2_Gram_stop2.txt', 'r')
    _2_gram_dict = collections.defaultdict(lambda: 0.0001)
    for i in f:
        a = i.strip().split()
        _2_gram_dict[a[0] + a[1]] = a[2]
    return _2_gram_dict

def get_3word_embeddig(word,sentence):
    b = re.findall(u"[\u4e00-\u9fa5]+", sentence, re.S)
    for sentence2 in b:
        if len(sentence2) >= 5:
            if len(word) == 3:
                word_pinyin = pypinyin.lazy_pinyin(word)
                list_word2 = []
                loc_cont = []
                sentence_pinyin = pypinyin.lazy_pinyin(sentence2)
                for i in range(len(sentence_pinyin)-2):
                    list_word = []
                    list_word.append(sentence_pinyin[i])
                    list_word.append(sentence_pinyin[i + 1])
                    list_word.append(sentence_pinyin[i + 2])
                    list_word2.append(list_word)

                for i in range(len(list_word2)):
                    if word_pinyin == list_word2[i]:
                        loc_cont.append(i)
                for i in loc_cont:
                    pinyin2 = sentence2[i] + sentence2[i + 1] + sentence2[i + 2]
                    if word == pinyin2:
                        continue
                    else:
                        return word
            if len(word) == 4:
                word_pinyin = pypinyin.lazy_pinyin(word)
                list_word2 = []
                loc_cont = []
                sentence_pinyin = pypinyin.lazy_pinyin(sentence2)
                for i in range(len(sentence_pinyin) - 3):
                    list_word = []
                    list_word.append(sentence_pinyin[i])
                    list_word.append(sentence_pinyin[i + 1])
                    list_word.append(sentence_pinyin[i + 2])
                    list_word.append(sentence_pinyin[i + 3])
                    list_word2.append(list_word)
                for i in range(len(list_word2)):
                    if word_pinyin == list_word2[i]:
                        loc_cont.append(i)
                for i in loc_cont:
                    pinyin2 = sentence2[i] + sentence2[i + 1] + sentence2[i + 2] + sentence2[i+3]
                    if word == pinyin2:
                        continue
                    else:
                        return word

            if len(word) == 5:
                word_pinyin = pypinyin.lazy_pinyin(word)
                list_word2 = []
                loc_cont = []
                sentence_pinyin = pypinyin.lazy_pinyin(sentence2)
                for i in range(len(sentence_pinyin) - 4):
                    list_word = []
                    list_word.append(sentence_pinyin[i])
                    list_word.append(sentence_pinyin[i + 1])
                    list_word.append(sentence_pinyin[i + 2])
                    list_word.append(sentence_pinyin[i + 3])
                    list_word.append(sentence_pinyin[i + 4])
                    list_word2.append(list_word)

                for i in range(len(list_word2)):
                    if word_pinyin == list_word2[i]:
                        loc_cont.append(i)
                for i in loc_cont:
                    pinyin2 = sentence2[i] + sentence2[i + 1] + sentence2[i + 2] + sentence2[i+3] + sentence2[i+4]
                    if word == pinyin2:
                        continue
                    else:
                        return word

if __name__ == "__main__":
    start = time.time()
    test_file = './zhongxing_test3.txt'
    f_test = open(test_file,'r')
    f_stopword = open('stopword.txt', 'r')
    f_duoyinzi = open('duoyinzi.txt','r')  # 3和5需要试一下好坏
    f_word = open('special_word.txt', 'r')  # 3和5需要试一下好坏
    f_sentence = open('zhongxing_test.txt', 'r', encoding='utf-8')
    f_result = open('result.txt','w')

    duoyinzi_dict = {}
    word_dict = {}
    stop_word_list = []
    print('inin date... ...')
    for i in f_duoyinzi:
        a = i.strip().split()
        duoyinzi_dict[a[0]] = a[1]

    for i in f_stopword:
        stop_word_list.append(i.strip())

    for i in f_word:
        word_dict_split = i.strip().split('    ')
        word_dict[word_dict_split[0]] = word_dict_split[1]
    _2_gram_dict = create_2_gram_dict()
    zhongjian = time.time()
    zhongjian = zhongjian - start
    print('The initialization is completed.Spend %f seconds',zhongjian)
    cnt = 0
    for i in f_test:
        b = ''
        a = i.strip().split(' ')

        if len(a)>2:
            cnt2 = cnt
            for number in range(1, len(a) - 1):
                b = b + a[number]
            for duoyinzi, zhengquezi in duoyinzi_dict.items():
                if duoyinzi in b:
                    cnt += 1
                    f_result.write('多音字    '+zhengquezi + '    ' + a[-1]+'\n')
                    print('多音字    '+zhengquezi + '    ' + a[-1])
                    print(cnt)
                    break
            for j in word_dict:
                result = get_3word_embeddig(j, b)
                if result != None:
                    cnt += 1
                    f_result.write('特殊词语    '+result+'    '+a[-1]+'\n')
                    print('特殊词语    '+result+'    '+a[-1])
                    print(cnt)
                    break

            if cnt2 != cnt:
                continue
            gram_model = _2_gram_model(b)
            result_dict = gram_model.make_result()
            if result_dict[0]==a[-1]:
                cnt+=1
                f_result.write('N元模型    '+result_dict[0] +'    '+a[-1]+'\n')
                print('N元模型    '+result_dict[0] +'    '+a[-1])
                print(cnt)
            elif result_dict[0] == None:
                f_result.write('语句无错    ' + result_dict[0] + '    ' + a[-1]+'\n')
                print('语句无错    ' + result_dict[0] + '    ' + a[-1])
                print(cnt)
            else :
                f_result.write('分词错误    ' + result_dict[0] + '    ' + a[-1]+'\n')
                print('分词错误    '+result_dict[0] +'    '+a[-1])
                print(cnt)
            # print(a[-1])
    print(cnt)
    print(time.time()-start)