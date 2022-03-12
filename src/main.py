import feedparser

feed_list = [
    {'name': 'samourai_wallet', 'type': 'reddit',
        'url': 'https://www.reddit.com/r/AskReddit/new/.rss'},

    {'name': 'samourai_wallet', 'type': 'article',
        'url': 'https://medium.com/feed/@SamouraiWallet'},

    {'name': 'samourai_wallet', 'type': 'twitter',
        'url': 'https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1'},

    {'name': 'samourai_wallet', 'type': 'youtube',
        'url': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCb4Y89L9Bokuo6OWqjAhMoA'},
]

# ==== start test ====
d = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCb4Y89L9Bokuo6OWqjAhMoA',
                     modified='Sat, 12 Mar 2022 18:20:43 GMT')
d2 = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UCb4Y89L9Bokuo6OWqjAhMoA',
                     modified=d.feed.modified)
with open('./entry', 'a') as f:
    for e in d2.entries:
        f.write(e.title)
        f.write('\n')
print('done')
# ===== end test =====


def format_item(item, type, name):
    description = '{item.link}\n#{type} #{name}'
    print(description)
    return ''


def get_data(url, name):
    return ''


def listener():
    for feed in feed_list:
        modified = get_modified(feed['name'])
        p = feedparser.parse(feed['url'], get_modified(feed['name'], modified))

        write_modified(p.feed.modified)


def write_modified(name, modified):
    with open('./modified.txt', 'r') as fr:
        lines = fr.read().splitlines()

        for i in len(lines):
            if lines[i].startswith(name):
                lines[i] = '{name}::{modified}'

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
