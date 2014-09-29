#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("UTF-8")  # @UndefinedVariable
from text_taster.Tokenizer import Tokenizer
import math

def create_tokenizer():
    tokenizer = Tokenizer()
    for line in open("study/delemeters.txt", "r").readlines():
        if len(line) > 0:
            tokenizer.add_delimiter(unicode(line.strip()))
    for line in open("study/stop.txt", "r").readlines():
        if len(line) > 0:
            tokenizer.add_stop(unicode(line.strip()))
    return tokenizer



if __name__ == "__main__":
    counter = {}
    total = 0
    tokenizer = create_tokenizer()


    for line in open("study/study.txt",'r').readlines():
        total += 1
        token = line.split("\t")
        category = token[1].strip()

        for s in tokenizer(token[0]):
            if not s in counter:
                # counter[s] = {}
                counter[s] = {"$TOTAL": 0}

            if not category in counter[s]:
                counter[s][category] =  0

            counter[s]["$TOTAL"] += 1
            counter[s][category] += 1

    fw = file("output/result.txt", 'w')
    for k in counter:
        if len(k)<=0:
            continue
        for k2 in counter[k]:
            if k2 == '$TOTAL':
                continue

            tf = counter[k][k2]
            idf = (1 + math.log(counter[k]["$TOTAL"]/counter[k][k2]))
            tfidf = tf * idf

            fw.write("%s\t%s\t%f\n" % (k, k2, tfidf))
            # print k, ">>>>", k2, tf, idf, tfidf
            # print k, k2, counter[k][k2], counter[k]["$TOTAL"]
    fw.close()
    print "ok. result ==> " ,total