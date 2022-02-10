import feedparser as feedParser
feed = feedParser.parse("https://medium.com/feed/@SamouraiWallet")

entry = feed.entries[0]
desc = entry.title + "\n"
desc += "\n" + "#article #samourai_wallet"
desc += "\n" + entry.link
print(desc)
print(entry.guid)