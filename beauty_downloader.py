# coding: utf-8

import craw as cw
import requests
import multiprocessing
import os
import re
import urllib
import sys
from time import sleep
requests.packages.urllib3.disable_warnings()


# 下載正妹圖2
def example6(argv):
    start = int(argv[1])
    end = int(argv[2])
    pps = int(argv[3])
    board_waiting_list = cw.GetBoardURL("Beauty", start, end)
    for boardurl in board_waiting_list:
        sleep(1)
        boardhtml = cw.GetHTML(boardurl)
        print boardurl
        post_waiting_list = cw.GetPostURL(boardhtml)
        for pourl in post_waiting_list:
            sleep(1)
            try:
                posthtml = cw.GetHTML(pourl)
                post = cw.Post(posthtml)
            except:
                continue
            if post.point() >= pps:
                try:
                    post_download(post)
                    p = multiprocessing.Process(target=post_download,
                                                args=(post,))
                    p.run()
                    print "downloading..."+post.info[2]
                except:
                    print "error for download "+pourl+" "+post.info[2]


def post_download(post):
    dir_name = post.info[2]
    html = post.content
    pic_regex = re.compile(
        u'<img src="(.+[{jpg}{png}])" alt'
    )

    if not os.path.exists(dir_name):
        try:
            os.mkdir(dir_name)
        except:
            print "error could not mkdir"

    pic_urls = pic_regex.findall(html)
    for i in range(len(pic_urls)):
        pic_urls[i] = u'http:'+pic_urls[i]

    for i in pic_urls:
        p = multiprocessing.Process(target=download_pic, args=(i, dir_name))
        p.start()
    p.join


def download_pic(pic_url, dir):
    try:
        pic_name = dir + '/' + pic_url.split('/')[-1]
        urllib.urlretrieve(pic_url, pic_name)
    except IOError as ioerr:
        print "IOError in download picture: " + pic_url + ioerr


def main():
    print sys.argv
    example6(sys.argv)

if __name__ == "__main__":
    main()
