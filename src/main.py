from importlib.resources import path
from os import path, mknod
import feedparser
from globaldic import *
from feedfilehandler import *
from utils import *


def init():
    if not path.exists(filedic['ids']):
        mknod(filedic['ids'])
    if not path.exists(filedic['etags']):
        mknod(filedic['etags'])
    if not path.exists(filedic['modifieds']):
        mknod(filedic['modifieds'])

    if not path.exists(filedic['feed']):
        with open(filedic['feed'], 'w') as fw:
            fw.write('<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>BTC Watcher</title><link>https://t.me/BTCWatcher</link><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/><description>A simple watch tower rss.feed over bitcoin nice resources</description><generator>SReza S</generator><language>en</language><lastBuildDate>Sun, 13 Mar 2022 13:16:22 GMT</lastBuildDate><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/></channel></rss>')


def listener():
    # iterate over feeds in feeddic and get their data using get_data
    # this function should be called every 15min to update the feed
    for fkey in feeddic:
        feed = feeddic[fkey]

        p = feedparser.parse(feed['url'])
        newitems = fetch_new_items(feed['name'], p.entries)

        # may be used later ¯\_(ツ)_/¯
        if hasattr(p, 'etag'):
            write_etag(p.modified)
        if hasattr(p, 'modified'):
            write_modified(p.modified)

        for i in newitems:
            format_item(i, feed['name'], feed['tags'])


# ==== start test ====
# init()
# listener()

# d = feedparser.parse(feed_dic[0]['url'])
# d2 = feedparser.parse(feed_dic[3]['url'],
#                      etag='')
# with open('./entry', 'a') as f:
#     for e in d2.entries:
#         f.write(e.title)
#         f.write('\n')
#
#     f.write(str(d.status) + '\n')
#     f.write(d.etag + '\n')
#     f.write(d.modified + '\n')

# file = minidom.parse(
#     file='/home/srezas/Programming/jsWorkspace/BTCWatcher/src/feed.rss')
# title = file.getElementsByTagName('title')
# print(title[0].data)

# ===== end test =====
