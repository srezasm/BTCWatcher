from rfeed import Item
import feedparser as feedParser
feed = feedParser.parse(
    "https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1")


def update_twitter_samouraiWallet():
    last_id
    last_items = []

    # loop from top(newest) of the feed items
    for item in feed.entries:

        # if the last item's id was the same as last_id
        # either we are at the top of the items and no new item has recorded in the feed_items
        # or we have some new items in the feed_items
        if item.id == last_id:

            # check if last_items is empty or not
            if len(last_items) != 0:
                feed_items = []

                # loop over last_items and format them into Item class
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
        # add new items to last_items in reverse order; so the new items will be first to be written in feed.rss
        last_items.insert(0, item)

    last_id = feed.entries[0].id
