#-*- coding: utf-8 -*-
import sys
from extractor import create_tokenizer
from flask import Flask, request
reload(sys)
sys.setdefaultencoding("UTF-8")  # @UndefinedVariable

class CategoryMaker:
    def __init__(self, filename='output/result.txt'):
        self.score_dict = {}
        self.tokenizer = create_tokenizer()
        for line in open(filename, "r").readlines():
            token = line.split("\t")
            word, category, score  = (unicode(token[0].strip()), unicode(token[1].strip()), float(token[2].strip()))
            if not word in self.score_dict:
                self.score_dict[word] = {category: score}
            else:
                self.score_dict[word].update({category: score})

    def __call__(self, text, limit=1):
        cate_score = {} # category, score
        history = []
        for token in self.tokenizer(text):
            if token in self.score_dict:
                for cate in self.score_dict[token]:
                    if not cate in cate_score:
                        cate_score[cate] = 0.0
                    cate_score[cate] += self.score_dict[token][cate]
                    history.append( (token, cate, self.score_dict[token][cate]) )
                    # print ">>>", token, cate, cate_score[cate]
        if len(cate_score)<limit:
            limit = len(cate_score)
        if len(cate_score)>=limit:
            r=[(w, cate_score[w]) for w in sorted(cate_score, key=cate_score.get, reverse=True)]
            return r[:limit], history


app = Flask(__name__)
extract_category = CategoryMaker()



@app.route("/",  methods=['GET', 'POST'])
def extract():
    text = request.args.get(u"title", "")
    rsb = """
    샘플</br/>
    [소프시스]위더스 컴퓨터책상 1260 /사무용 책상/컴퓨터 테이블/디자인가구<br/><br/>
    [F/W신상] 균일가! 4900원+무료배송/패션양말 4족/9족세트/국내생산/발목/스포츠/캐릭터/페이크삭스/아동<BR/><BR/>
    [무료배송/프리미엄 고급 셀카봉 4종 풀세트 추가금X] 프리미엄 셀카봉 + 고급 거치대 + 리모컨 + 클립 가로 세로촬영 셀카봉 알루미늄 셀카봉 셀카촬영 휴대폰 셀프촬영 셀카포드 셀카리모콘 셀카스틱<Br/>


    <form>제품소개: <input type='text' name='title'/><input type='submit'/><br/>
    """


    if text and len(text) > 0:
        category, history = extract_category(text.strip(), 5)
        if category and category[0]:
            result_cate = category[0][0]
            result_score = category[0][1]

            rsb += "'%s'의 카테고리 분석결과<br/>" % (text)
            rsb += "==================================<br/>"
            rsb += "[후보카테고리]<br/>"
            rsb += "==================================<br/>"
            for k in category:
                rsb += "> %s (score: %f)<br/>" % k

            rsb += "<br/>==================================<br/>"
            rsb += "[단어점수]<br/>"
            rsb += "==================================<br/>"
            for l in history:
                rsb += "> %s => %s (score: %f)<br/>" % l
    rsb += "</form>"
    return rsb


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9977)
    # print extract("미샤 타임 레볼루션 베스트 셀러 특별 기획 세트")
    # category = CategoryMaker()
    # cnt_s = 0
    # cnt_f = 0
    # for line in open('study/answer.txt', "r").readlines():
    #     token = line.split("\t")
    #
    #     c = category(token[0].strip())
    #     if c:
    #         c = c[0]
    #     if c and str(token[1].strip())!=str(c[0][0].strip()):
    #         cnt_f += 1
    #         # print "[기대:%s / 추출:%s <%f>] %s" % (token[1].strip(), str(c[0][0]), c[0][1], token[0].strip())
    #     else:
    #         cnt_s += 1
    #
    #
    # print "성공: ", cnt_s, "실패: ", cnt_f, "성공률: ", (100*cnt_s/(cnt_s+cnt_f)),"%"



    # cnt_s = 0
    # cnt_f = 0
    # for line in open('study/study.txt', "r").readlines():
    #     token = line.split("\t")
    #
    #     c = category(token[0].strip())
    #     if c and str(token[1].strip())!=str(c[0][0].strip()):
    #         cnt_f += 1
    #         # print "[기대:%s / 추출:%s <%f>] %s" % (token[1].strip(), str(c[0][0]), c[0][1], token[0].strip())
    #     else:
    #         cnt_s += 1
    #
    #
    # print "성공: ", cnt_s, "실패: ", cnt_f, "성공률: ", (100*cnt_s/(cnt_s+cnt_f)),"%"






    # test = category("[H몰] 베네피트 7001 아르덴 숄더/크로스백")
    # test = category("미샤 타임 레볼루션 베스트 셀러 특별 기획 세트")
    # test = category("[위더스]위더스 PM책상 1260/책상/의자/책장/공부상/큰사이즈/무료배송",10)
    #
    # print "최종결과는?"
    # for r in test:
    #     print str(r[0]), str(r[1])
