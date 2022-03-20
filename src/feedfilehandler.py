import re
from uuid import uuid4
import xml.etree.ElementTree as etree
from configs import *
from log import log_info
from utils import *
from logging import *


def format_item(item, key):
    if 'twitter' in key:
        log_info('formatting tweeter')
        __format_twitter__(item, key)
    if 'github_release' in key:
        log_info('formatting github release')
        __format_github_release__(item, key)
    else:
        log_info('formatting default')
        __format_default__(item, key)


def __format_default__(item, key):
    itempubt = ''

    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
        itempubt = item.published
    else:
        pubt += get_current_time()
        itempubt = get_current_time()

    link = f'[{get_entry(item, "link")}](Link)'

    tags = feeddic[key]['tags']
    hashtags = '#' + ' #'.join(tags)

    description = f'{feeddic[key]["name"]}: {get_entry(item, "title")}\n\n{link}\n{hashtags}\n{pubt}'

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

    description = f'{tweet}\n\n{link}\n{hashtags}\n{pubt}'

    new_item(get_entry(item, 'title'), description,
             get_entry(item, "link"), tags, itempubt)


def __format_github_release__(item, key):
    itempubt = ''

    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
        itempubt = item.published
    else:
        pubt += get_current_time()
        itempubt = get_current_time()

    link = f'[{get_entry(item, "link")}](Link)'

    tags = feeddic[key]['tags']
    hashtags = '#' + ' #'.join(tags)

    content = get_entry(item, 'description')
    content = content.replace('<ul>', '')
    content = content.replace('</ul>', '')
    content = content.replace('<li>', '- ')
    content = content.replace('</li>', '')
    if '@' in content:
        for unametxt in re.findall('<a.*?a>', content):
            unamel = re.search(
                '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', unametxt).group()
            uname = re.search('\B@((?!.*(-){2,}.*)[a-z0-9][a-z0-9-]{0,38}[a-z0-9])', unametxt).group()
            content = content.replace(unametxt, f'[{uname}]({unamel})')
    for anc in re.findall('<a.*?a>', content):
        ancl = re.search(
            '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', anc).group()
        content = content.replace(anc, f'[link]({ancl})')

    content = content.strip()

    description = f'**{feeddic[key]["name"]} Release: {get_entry(item, "title")}**\n{content}\n\n{link}\n{hashtags}\n{pubt}'

    new_item(f'{feeddic[key]["name"]} {get_entry(item, "title")}', description,
             get_entry(item, 'link'), tags, itempubt)


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

        log_info(f'writing item: {gui.text}')
        with open(filedic['test_feed'], 'w') as fw:
            fw.write(nwf)
