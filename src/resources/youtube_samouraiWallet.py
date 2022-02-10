import feedparser as feedParser
feed = feedParser.parse("https://www.youtube.com/feeds/videos.xml?channel_id=UCb4Y89L9Bokuo6OWqjAhMoA")

entry = feed.entries[0]
desc = entry.title + "\n"
desc += "\n" + "#youtube #samourai_wallet"
desc += "\n" + entry.link
print(desc)
