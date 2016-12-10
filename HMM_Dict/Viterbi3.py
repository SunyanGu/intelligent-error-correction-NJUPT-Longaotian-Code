import collections
import time

def init_states():
    word_list = []
    f = open('./word_pinyin_num2.txt','r')
    for i in f:
        b = i.split()
        word_list.append(b[0])
    return word_list

def get_pinyin_all():
    f = open('word_pinyin_dict.txt','r')
    pinyin_list = []
    for i in f:
        a = i.strip().split(' ')
        pinyin_list.append(a[0])
    return set(pinyin_list)

def init_start():
    a = collections.defaultdict(lambda :0)
    f = open('./start_list2.txt','r')
    for i in f:
        b = i.split()
        a[b[0]] = b[1]
    return a

def init_trans():
    a = collections.defaultdict(lambda :{})
    f = open('./new_trans.txt','r')
    for i in f:
        b = i.split()
        a[b[0]][b[1]] = b[2]
    return a

def init_emission():
    a = collections.defaultdict(lambda :{})
    f = open('./word_pinyin_num2.txt','r')
    pinyin_set = get_pinyin_all()
    for i in f:
        b = i.split()
        #print(b)
        for j in pinyin_set:
            if j == b[1]:
                a[b[0]][b[1]] = b[2]
            else:
                a[b[0]][j] = 0
    return a

def print_dptable(V):
    for i in range(len(V)): print ("%7d" % i,)
    for t in V:
        d = sorted(t.items(), key=lambda t: t[1], reverse=True)

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}
    for y in states:
        V[0][y] = float(start_p[y]) * float(emit_p[y][obs[0]])
        path[y] = [y]
    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            (prob, state) = max([(float(V[t-1][y0]) * float(trans_p[y0][y]) * float(emit_p[y][obs[t]]), y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        # Don't need to remember the old paths
        path = newpath
    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

def create_pinyin_word_dict():
    f = open('./word_pinyin_num2.txt','r')
    pinyin_word_dict = collections.defaultdict(lambda :[])
    for i in f:
        a = i.strip().split()
        pinyin_word_dict[a[1]].append(a[0])
    return pinyin_word_dict

def create_word_score_dict():
    f = open('./start_list2.txt','r')
    word_score_dict = {}
    for i in f:
        a = i.strip().split()
        word_score_dict[a[0]] = a[1]
    #print(word_score_dict)
    return word_score_dict

def init_states_word(pinyin_list):
    pinyin_word_dict = create_pinyin_word_dict()
    word_score_dict = create_word_score_dict()
    start_dict = {}
    start_list = []
    for i in pinyin_list:
        start_list.extend(pinyin_word_dict[i])
    for j in start_list:
        start_dict[j] = word_score_dict[j]
    # print(start_dict)
    # print(start_list)
    return start_dict,start_list

def init_trans_word(pinyin_list):
    start_dict,start_list = init_states_word(pinyin_list)
    init_tran = init_trans()
    trans_dict = collections.defaultdict(lambda :{})
    for i in start_list:
        for j in start_list:
            trans_dict[i][j] = init_tran[i][j]
    return trans_dict

def init_emition_word(pinyin_list):
    emission = init_emission()
    start_dict,start_list = init_states_word(pinyin_list)
    emition_dict = collections.defaultdict(lambda :{})
    for i in start_list:
        for j in pinyin_list:
            emition_dict[i][j] = emission[i][j]
    return emition_dict




if __name__ == '__main__':
    start = time.time()
    string = input('input:')
    pinyin_list = string.split()
    start_probability,states = init_states_word(pinyin_list)
    transition_probability = init_trans_word(pinyin_list)
    emission_probability = init_emition_word(pinyin_list)
    print(viterbi(pinyin_list, states, start_probability, transition_probability, emission_probability))
    end = time.time()
    print(end - start)
