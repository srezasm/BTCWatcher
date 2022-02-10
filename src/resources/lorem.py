from rfeed import Item
import feedparser as feedParser
feed = feedParser.parse(
    "https://lorem-rss.herokuapp.com/feed?unit=second")


def lorem_update():
    last_id
    last_items = []

    for item in feed.entries:

        if item.id == last_id:
            if len(last_items) != 0:
                feed_items = []

                for li in last_items:
                    desc = li.description + "\n"
                    desc += "\n" + "#twitter #samourai_wallet"
                    desc += "\n" + li.link

                    feed_item = Item(title=li.title,
                                     description=desc,
                                     link=li.link,
                                     author=li.author,
                                     guid=li.guid,
                                     pubDate=li.published)

                    feed_items.append(feed_item)

                return feed_items

        last_items.insert(0, item)

    last_id = feed.entries[0].id
