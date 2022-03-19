import re
from uuid import uuid4
import xml.etree.ElementTree as etree
from configs import *
from utils import *


def format_item(item, key):
    if 'twitter' in key:
        __format_twitter__(item, key)
    else:
        __format_default__(item, key)


def __format_default__(item, key):
    itempubt = ''

    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
        itempubt = item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())
        itempubt = strftime('%a, %d %b %Y %X GMT', gmtime())

    link = f'[{get_entry(item, "link")}](Link)'

    tags = feeddic[key]['tags']
    hashtags = '#' + ' #'.join(tags)

    description = get_entry(item, 'title') + '\n\n' + \
        link + '\n' + hashtags + '\n' + pubt

    new_item(get_entry(item, 'title'), description,
             get_entry(item, 'link'), tags, itempubt)


def __format_twitter__(item, key):
    itempubt = ''
    link = ''

    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
        itempubt = item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())
        itempubt = strftime('%a, %d %b %Y %X GMT', gmtime())

    tags = feeddic[key]['tags']
    hashtags = '#' + ' #'.join(tags)

    tweet = get_entry(item, 'description')

    if tweet.startswith('🔁'):
        # tweet = tweet.replace('<br />', ':\n', 1)
        link = f'[{get_entry(item, "link")}](ReTweet Link)'
    else:
        link = f'[{get_entry(item, "link")}](Tweet Link)'

    for img in re.findall('<img .*?>', tweet):
        imgl = re.search(
            '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', img).group()
        tweet = tweet.replace(img, f'[image]({imgl})')
    for vid in re.findall('<video .*?>', tweet):
        vidl = re.search(
            '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', vid).group()
        tweet = tweet.replace(vid, f'[link]({vidl})')
    for anc in re.findall('<a .*?/>', tweet):
        ancl = re.search(
            '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', anc).group()
        if(re.match('twitter.com/*./status/', ancl)):
            tweet = tweet.replace(anc, f'[quted tweet link]({ancl})')
        else:
            tweet = tweet.replace(anc, f'[link]({ancl})')
    tweet = tweet.replace('<br />', '\n')

    description = tweet + \
        '\n\n' + link + '\n' + hashtags + '\n' + pubt

    new_item(get_entry(item, 'title'), description,
             get_entry(item, "link"), tags, itempubt)


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

    with open(filedic['test_feed'], 'r') as fr:
        f = fr.read()
        i = f.index('<item>')
        istr = etree.tostring(item).decode("utf-8")
        nwf = f[:i] + istr + f[i:]

        with open(filedic['test_feed'], 'w') as fw:
            fw.write(nwf)
