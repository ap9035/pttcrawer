
# coding: utf-8

# In[1]:
"""
簡單的文字探勘，在文檔案中找出現次數最多的字詞
"""


import re
import numpy as np
import codecs


# 輸入html碼，去除一些符號，並藉由postminding函數來進行分析
def htmlmind(webhtml, m, M):
    p = re.compile(u'[\w<>="()\-!|\?&}\+#{\',;\[\] :./\t\n\r\f\v推]')
    article = re.sub(p, '', webhtml)
    data = postminding(article, m, M)
    return data


# 輸入html，並取得其中某文字的出現次數
def GetWordFreq(webhtml, word):
    p = re.compile(word)
    words = re.findall(p, webhtml)
    return len(words)


# 輸入一文章，並根據詞彙最小長度和最大長度進行分析，回傳文字與次數
def postminding(mystr, min_len, max_len):
    N = len(mystr)
    mydict = dict()
# 建立字典
    for char_len in range(min_len, max_len):
        for locate in range(N):
            if char_len+locate < N:
                keyword = mystr[locate:locate+char_len+1]
                mydict[keyword] = [0, keyword]

# 對字典中得值進行累加
    for char_len in range(min_len, max_len):
        for locate in range(N):
            if char_len+locate < N:
                keyword = mystr[locate:locate+char_len+1]
                mydict[keyword][0] += 1

    data = np.array(mydict.values())
    data = sorted(data, key=lambda x: x[0])
    return data


def main():
    p = re.compile(r'[ :./\t\n\r\f\v推]')

    f = codecs.open("test.dat", "r", "utf-8")
    mystr = f.read().strip('\n')
    mystr = re.sub(p, '', mystr)

    print mystr
    data = postminding(mystr, 1, 3)
    if data is not []:
        for i in range(1, 11):
            print data[-i][1], "\t", data[-i][0]
    f.close()


if __name__ == "__main__":
    main()
