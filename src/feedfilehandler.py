from uuid import uuid4
import xml.etree.ElementTree as etree
from globaldic import *
from utils import *


def format_item(item, name, tags):
    pubt = 'published: '
    if (hasattr(item, 'published')):
        pubt += item.published
    else:
        pubt += strftime('%a, %d %b %Y %X GMT', gmtime())

    link = get_entry(item, 'link')

    hashtags = '#' + ' #'.join(tags)

    description = link + '\n' + hashtags + '\n' + pubt

    newitem = new_item(get_entry(item, 'title'), description, link, tags, pubt)
    
    return newitem


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
    with open(filedic['test_feed'], 'rt') as f:
        tree = etree.ElementTree.parse(source=f)
        index = tree.childNodes.index('item')
        tree.insert(index, item)
        tree.set('lastBuildDate', get_current_time())

    # todo: change feed.test.rss to feed.rss
    with open(filedic['test_feed'], 'wb') as f:
        etree.ElementTree(tree).write(f)
