
# coding: utf-8

# In[1]:

import re
import urllib2
from datetime import datetime
import requests
requests.packages.urllib3.disable_warnings()


class Post:

    def __init__(self, htmlstr):
        Post_regex = re.compile(
            r'</span><span class="article-meta-value">(.{1,100})</span></div>')
        article_meta_info = Post_regex.findall(htmlstr)
        Stime = article_meta_info[3]
        date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
        info = article_meta_info
        info[-1] = date_object
        self.info = info
        self.content = htmlstr
        self.pushlist = GetPush(htmlstr)

    def point(self):
        counter = 0
        for i in self.pushlist:
            counter += i.point
        return counter


class pushinfo:

    def __init__(self, olist, year):
        self.status = olist[0]
        self.name = olist[1]
        self.content = olist[2]
        self.time = datetime.strptime(olist[3]+year, '%m/%d %H:%M%Y')
        self.point = self.p(olist[0])

    def p(self, x):
        return {
            u'推': 1,
            u'噓': -1,
            u'→': 0,
        }[x]


#取得該貼文的時間戳記
def GetPostTime(htmlstr):
    Post_regex = re.compile(
        r'</span><span class="article-meta-value">(.{1,100})</span></div>')
    article_meta_info = Post_regex.findall(htmlstr)
    Stime = article_meta_info[3]
    date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
    return date_object


#取得該貼文的作者資訊（可被Post取代）
def GetPostInfo(htmlstr):
    Post_regex = re.compile(
        r'</span><span class="article-meta-value">(.{1,100})</span></div>')
    article_meta_info = Post_regex.findall(htmlstr)
    Stime = article_meta_info[3]
    date_object = datetime.strptime(Stime, '%a %b %d %H:%M:%S %Y')
    info = article_meta_info
    info[-1] = date_object
    return info


# 取得該html中所有的推文，並回傳類別
def GetPush(webhtml):
    pushre = re.compile(
        u'push-tag">(.+) </span>.+push-userid">(.+)</span>.+push-content">: (.+)</span>.+"push-ipdatetime"> (.+)')
    mylist = re.findall(pushre, webhtml)
    postdate = GetPostTime(webhtml)
    year = str(postdate.year)
    pushlist = []
    for i in mylist:
        try:
            push = pushinfo(i, year)
            pushlist.append(push)
        except:
            print "error to add push"
    return pushlist


# 由看板取得文章的連結
def GetPostURL(boardhtml):
    Post_regex = re.compile(r'<a href="(.{1,200}\.html)">')
    urls = Post_regex.findall(boardhtml)
    for i in range(len(urls)):
        urls[i] = "https://www.ptt.cc/"+urls[i]
    return urls


# 取得看板的網址
def GetBoardURL(BoardName, Start, End):
    head = "https://www.ptt.cc/bbs/"+BoardName+"/index"
    retlist = []
    for i in range(Start, End):
        URL = head+str(i)+".html"
        retlist.append(URL)
    return retlist


# 取得該網址的HTML碼
def GetHTML(URL):
    content = urllib2.urlopen(URL).read()
    return content.decode('utf8')


# 取得需要驗證的版面的html碼
def Get18HTML(URL):
    payload = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    rs = requests.session()
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
    res = rs.get(URL, verify=False)
    return res.text


def main():
    html = GetHTML("https://www.ptt.cc/bbs/C_Chat/M.1452691553.A.187.html")
    for i in GetPush(html):
        print i.name, i.content, i.status


if __name__ == "__main__":
    main()
