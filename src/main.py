from importlib.resources import path
from os import path, mknod
import feedparser
from configs import *
from feedfilehandler import *
from utils import *
import sched
import time


def init():
    if not path.exists(filedic['ids']):
        mknod(filedic['ids'])
    if not path.exists(filedic['etags']):
        mknod(filedic['etags'])
    if not path.exists(filedic['modifieds']):
        mknod(filedic['modifieds'])

    if not path.exists(filedic['feed']):
        with open(filedic['feed'], 'w') as fw:
            fw.write('<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>BTC Watcher</title><link>https://t.me/BTCWatcher</link><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/><description>A simple watch tower rss.feed over bitcoin nice resources</description><generator>SReza S</generator><language>en</language><lastBuildDate>Sun, 13 Mar 2022 13:16:22 GMT</lastBuildDate><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/></item><item><title>first default post</title><description>default</description><link>https://t.me/MyBtcFeeds</link><pubDate>Mon, 09 Aug 2021 12:17:40 GMT</pubDate><guid>960acfb7-e4cc-43c7-ba8d-d88b4590648b</guid></item></channel></rss>')


init()
sch = sched.scheduler(time.time, time.sleep)


def listener():
    # iterate over feeds in feeddic and get their data using get_data
    # this function should be called every 15min to update the feed
    for fkey in feeddic:
        feed = feeddic[fkey]

        p = feedparser.parse(feed['url'])
        newitems = fetch_new_items(fkey, p.entries)

        # may be used later ¯\_(ツ)_/¯
        if hasattr(p, 'etag'):
            write_etag(fkey, p.etag)
        if hasattr(p, 'modified'):
            write_modified(fkey, p.modified)

        for i in newitems:
            format_item(i, fkey)


sch.enter(60, 1, listener())
sch.run()
