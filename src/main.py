from importlib.resources import path
from os import PRIO_USER, path, mknod
from xml.etree import ElementTree
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
            format_item(i, fkey)


# ==== start test ====
# init()
# listener()

url = feeddic['samourai_wallet_twitter']['url']
d = feedparser.parse(url)
item = d.entries[4]
tweet = get_entry(item, 'description')
print(tweet)

for img in re.findall('<img .*?>', tweet):
    imgl = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', img).group()
    tweet = tweet.replace(img, f'[image]({imgl})')
    continue
for anc in re.findall('<a .*?>', tweet):
    ancl = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', anc).group()
    tweet = tweet.replace(anc, f'[link]({ancl})')
    continue
tweet = tweet.replace('<br />', '\n')
print(tweet)
# soup = BeautifulSoup(tweet, 'html.parser')
# img = soup.select('img')
# [i['src'] for i in img if i['src']]
# img['src']

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
