from rfeed import Feed
from resources.twitter_samouraiWallet import update_twitter_samouraiWallet
from resources.lorem import lorem_update

# file = open("feed.rss", "w")
# updates = []

# while 1:
#     twitter_samouraiWallet = update_twitter_samouraiWallet()

#     updates.append(twitter_samouraiWallet)

#     feed = Feed(
#         title="BTC Watcher",
#         link="https://t.me/BTCWatcher",
#         description="A simple watch tower rss.feed for bitcoin nice resources",
#         items=updates
#     )

# file.write(feed.rss())

file = open("feed.rss", "w")
updates = []

while 1:
    twitter_samouraiWallet = lorem_update

    updates.append(twitter_samouraiWallet)

    feed = Feed(
        title="BTC Watcher",
        link="https://t.me/BTCWatcher",
        description="A simple watch tower rss.feed for bitcoin nice resources",
        items=updates
    )

    file.write(feed.rss())