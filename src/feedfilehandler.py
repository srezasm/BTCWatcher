import re
from uuid import uuid4
from xml.dom.minidom import Element
import xml.etree.ElementTree as etree
from globaldic import *
from utils import *


def format_item(item, key):
    if 'twitter' in key:
        __format_twitter__(item, key)
    else:
        __format_default__(item, key)


def __format_default__(item, key):
    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())

    link = get_entry(item, 'link')

    tags = feeddic[key]['tags']
    hashtags = '#' + ' #'.join(tags)

    description = link + '\n' + hashtags + '\n' + pubt

    new_item(get_entry(item, 'title'), description, link, tags, pubt)


def __format_twitter__(item, key):
    pubt, link, hashtags, tweet, description = ''
    feed = feeddic[key]

    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())

    tags = feed['tags']
    hashtags = '#' + ' #'.join(tags)

    tweet = get_entry(item, 'description')

    if tweet.startswith('🔁'):
        # tweet = tweet.replace('<br />', ':\n', 1)
        link = f'[{get_entry(item, "link")}](ReTweet Link)'
    else:
        link = f'[{get_entry(item, "link")}](Tweet Link)'

    for img in re.findall('<img .*?>', tweet):
        imgl = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', img).group()
        tweet = tweet.replace(img, f'[image]({imgl})')
    for vid in re.findall('<video .*?>', tweet):
        vidl = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', vid).group()
        tweet = tweet.replace(vid, f'[link]({vidl})')
    for anc in re.findall('<a .*?/>', tweet):
        ancl = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', anc).group()
        if(re.match('twitter.com/*./status/', ancl)):
            tweet = tweet.replace(anc, f'[quted tweet link]({ancl})')
        else:
            tweet = tweet.replace(anc, f'[link]({ancl})')
    tweet = tweet.replace('<br />', '\n')

    description = tweet + \
        '\n\n' + link + '\n' + hashtags + '\n' + pubt

    new_item(get_entry(item, 'title'), description, link, tags, pubt)


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

    # todo: change feed.test.rss to feed.rss
    # parsed = minidom.parse(file_dic['test_feed'])
    # with open(filedic['test_feed'], 'rt') as f:
    #     tree = etree.ElementTree.parse(source=f)
    #     index = tree.childNodes.index('item')
    #     tree.insert(index, item)
    #     tree.set('lastBuildDate', get_current_time())

    # todo: change feed.test.rss to feed.rss
    # with open(filedic['test_feed'], 'wb') as f:
    #     etree.ElementTree(tree).write(f)
