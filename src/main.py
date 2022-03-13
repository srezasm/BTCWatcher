from email.utils import getaddresses
from lib2to3.pgen2.token import NEWLINE
from traceback import print_tb
import feedparser

# sience [rsshub](rsshub.app) project supports [etag and modified](https://pythonhosted.org/feedparser/http-etag.html) features, using rsshub is in priority
feed_dic = [
    {'name': 'samourai_wallet', 'type': 'reddit',
        'url': 'https://www.reddit.com/r/AskReddit/new/.rss'},

    {'name': 'samourai_wallet', 'type': 'article',
        'url': 'https://medium.com/feed/@SamouraiWallet'},

    {'name': 'samourai_wallet', 'type': 'twitter',
        'url': 'https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1'},

    {'name': 'samourai_wallet', 'type': 'youtube',
        'url': 'https://rsshub.app/youtube/channel/UCb4Y89L9Bokuo6OWqjAhMoA'},
]

# ==== start test ====
d = feedparser.parse(feed_dic[0]['url'])

d2 = feedparser.parse(feed_dic[3]['url'],
                     etag='')

print('has etag') if hasattr(d, 'etag') else print('doesn\'t have etag')
    

# with open('./entry', 'a') as f:
#     for e in d2.entries:
#         f.write(e.title)
#         f.write('\n')
#
#     f.write(str(d.status) + '\n')
#     f.write(d.etag + '\n')
#     f.write(d.modified + '\n')

print('done')
# ===== end test =====


def listener():
    for feed in feed_dic:
        items = get_data(feed)

def format_item(item, type, name):
    item.description = '{item.link}\n#{type} #{name}'
    return item

def get_data(feed):
    p = feedparser.parse(feed['url'])
    new_items = filter_new_items(feed['name'], p.entries)

    formatted_items = []
    for i in new_items.items:
        formatted_items.append(format_item(i, feed['type'], feed['name']))
    
    # may be used later ¯\_(ツ)_/¯
    if hasattr(p, 'etag'): write_etag(p.modified)
    if hasattr(p, 'modified'): write_modified(p.modified)

    return formatted_items

def filter_new_items(name, items):
    with open('./ids.txt', 'r') as fr:
        # for first time, return all items
        if name not in fr.read():
            return items

        old_lines = fr.read().splitlines()
        old_ids = []

        # fill the old_ids
        for l in old_lines:
            if l.startswith(name):
                old_ids.append(l.split('::'))
                old_ids.pop(0)

        # fill new_items
        new_items = [items]
        for id in old_ids:
            for it in items:
                if id == it.id:
                    new_items.remove(it)

        # fill new_ids
        new_ids = []
        for ni in new_items:
            new_ids.append(ni.id)

        # fill new_lines
        new_lines = [old_lines]
        for l in new_lines:
            if l.startswith(name):
                l += '::' + '::'.join(new_ids)

        # write new_lines into ids.text
        with open('./ids.txt', 'w') as fw:
            for nl in new_lines:
                print(nl, file=fw)

        return new_items

#region etag

def write_etag(name, etag):
    with open('./etag.txt', 'r') as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = '{name}::{etag}'

        fw = open('./etag.txt', 'w')
        fw.write('\n'.join(lines))
        fw.close()

def get_etag(name):
    with open('./etag.txt', 'r') as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]

#endregion

#region modified

def write_modified(name, modified):
    with open('./modified.txt', 'r') as fr:
        lines = fr.read().splitlines()

        for ni in len(lines):
            if lines[ni].startswith(name):
                lines[ni] = '{name}::{modified}'

        fw = open('./modified.txt', 'w')
        fw.write('\n'.join(lines))
        fw.close()

def get_modified(name):
    with open('./modified.txt', 'r') as fr:
        lines = fr.read().splitlines()

        if name not in fr.read():
            return ''

        else:
            for l in lines:
                if l.startswith(name):
                    return l.split('::')[1]

#endregion