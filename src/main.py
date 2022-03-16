from importlib.resources import path
from operator import imod
from time import gmtime, strftime
from uuid import uuid4
from xml.dom import minidom
from os import path, mknod
import feedparser
import xml.etree.ElementTree as etree


# [rsshub](rsshub.app) is in priority because of supporting [etag and modified](https://pythonhosted.org/feedparser/http-etag.html)
feed_dic = [
    # {'name': 'reddit', 'type': 'reddit',
    #     'url': 'https://www.reddit.com/r/AskReddit/new/.rss'},

    {'name': 'samourai_wallet', 'type': 'article',
        'url': 'https://medium.com/feed/@SamouraiWallet'},

    # {'name': 'samourai_wallet', 'type': 'twitter',
    #     'url': 'https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1'},

    # {'name': 'samourai_wallet', 'type': 'youtube',
    #     'url': 'https://rsshub.app/youtube/channel/UCb4Y89L9Bokuo6OWqjAhMoA'},
]


file_dic = {
    'ids': './ids.txt',
    'etags': './etags.txt',
    'modifieds': './modifieds.txt',
    'feed': './feed.rss',
    'test_feed': 'feed.test.rss'
}


def init():
    if not path.exists(file_dic['ids']):
        mknod(file_dic['ids'])
    if not path.exists(file_dic['etags']):
        mknod(file_dic['etags'])
    if not path.exists(file_dic['modifieds']):
        mknod(file_dic['modifieds'])

    if not path.exists(file_dic['feed']):
        with open(file_dic['feed'], 'w') as fw:
            fw.write('<rss xmlns:atom="http://www.w3.org/2005/Atom" version="2.0"><channel><title>BTC Watcher</title><link>https://t.me/BTCWatcher</link><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/><description>A simple watch tower rss.feed over bitcoin nice resources</description><generator>SReza S</generator><language>en</language><lastBuildDate>Sun, 13 Mar 2022 13:16:22 GMT</lastBuildDate><atom:link href="https://t.me/BTCWatcher" rel="self" type="application/rss+xml"/></channel></rss>')


def listener():
    for feed in feed_dic:
        items = get_data(feed)

        for i in items:
            ni = new_item(get_entry(i, 'title'),
                          get_entry(i, 'description'),
                          get_entry(i, 'link'),
                          get_entry(i, 'categories', True),
                          get_entry(i, 'published'))

            push_item(ni)


def get_data(feed):
    p = feedparser.parse(feed['url'])
    new_items = fetch_new_items(feed['name'], p.entries)

    formatted_items = []
    for i in new_items:
        formatted_items.append(format_item(i, feed['type'], feed['name']))

    # may be used later ¯\_(ツ)_/¯
    if hasattr(p, 'etag'):
        write_etag(p.modified)
    if hasattr(p, 'modified'):
        write_modified(p.modified)

    return formatted_items


def fetch_new_items(name, items: list):
    with open(file_dic['ids']) as fr:
        old_lines = fr.read().splitlines()
        old_ids = []
        new_lines = old_lines.copy()
        
        isn = False
        for ol in old_lines:
            if ol.startswith(name): isn = True

        if not isn:
            ii = []
            for i in items:
                ii.append(i.id)

            new_lines.append(name + '::' + '::'.join(ii))
            with open(file_dic['ids'], 'w') as fw:
                fw.write('\n'.join(new_lines))
            return items

        # fill the old_ids with current feed ids
        for ol in old_lines:
            if ol.startswith(name):
                old_ids.extend(ol.split('::'))
                old_ids.pop(0)

        # fill new_items
        new_items = items.copy()
        for id in old_ids:
            for it in items:
                if id == it.id:
                    new_items.remove(it)

        # fill new_ids
        new_ids = []
        for ni in new_items:
            new_ids.append(ni.id)

        # fill new_lines
        for i in range(len(new_lines)):
            nl = new_lines[i]

            if nl.startswith(name):
                new_lines[i] = nl + '::' + '::'.join(new_ids)

        # write new_lines into ids.text
        with open(file_dic['ids'], 'w') as fw:
            fw.write('\n'.join(new_lines))

        return new_items


# region xml handling

def format_item(item, type, name):
    pubt = '\npublished: '
    if (hasattr(item, 'published')):
        pubt += item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())

    link = get_entry(item, 'link') + '\n'

    item['description'] = link + '#' + type + ' #' + name + pubt
    return item


def new_item(title: str, description: str, link: str, categories: list, pubdate: str):
    item = etree.Element('item')

    tt = etree.SubElement(item, 'title')
    tt.text = title

    dc = etree.SubElement(item, 'description')
    dc.text = description

    ln = etree.SubElement(item, 'link')
    ln.text = link

    for category in categories:
        ct = etree.SubElement(item, 'category')
        ct.text = category

    pd = etree.SubElement(item, 'pubDate')
    pd.text = pubdate

    gui = etree.SubElement(item, 'guid')
    gui.text = str(uuid4())

    return item


def push_item(item):
    # todo: change feed.test.rss to feed.rss
    # parsed = minidom.parse(file_dic['test_feed'])
    with open(file_dic['test_feed'], 'rt') as f:
        tree = etree.ElementTree.parse(source=f)
        index = tree.childNodes.index('item')
        tree.insert(index, item)
        tree.set('lastBuildDate', get_current_time())


    # todo: change feed.test.rss to feed.rss
    with open(file_dic['test_feed'], 'wb') as f:
        etree.ElementTree(tree).write(f)


# endregion


# region etag

def write_etag(name, etag):
    with open(file_dic['etags']) as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = '{name}::{etag}'

        fw = open(file_dic['etags'], 'w')
        fw.write('\n'.join(lines))
        fw.close()


def get_etag(name):
    with open(file_dic['etags']) as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]

# endregion


# region modified

def write_modified(name, modified):
    with open(file_dic['modifieds']) as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = '{name}::{modified}'

        fw = open(file_dic['modifieds'], 'w')
        fw.write('\n'.join(lines))
        fw.close()


def get_modified(name):
    with open(file_dic['modifieds']) as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]

# endregion


# returns current time with feed format
def get_current_time():
    # https://datatracker.ietf.org/doc/html/rfc2822
    return strftime('%a, %d %b %Y %X GMT', gmtime())


# prevents possible errors if the called entry doesn't exist
def get_entry(item, enty_name: str, is_list=False):
    return item[enty_name] if hasattr(item, enty_name) else ([] if is_list else '')


# ==== start test ====
init()
listener()

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
