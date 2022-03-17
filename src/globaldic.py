# [rsshub](rsshub.app) is in priority because of [etag and modified](https://pythonhosted.org/feedparser/http-etag.html)
feeddic = {
    'reddit_test': {
        'tags': ['reddit', 'test'],
        'url': 'https://www.reddit.com/r/AskReddit/new/.rss'
    },

    'samourai_wallet_medium': {
        'tags': ['article', 'medium', 'samourai_wallet'],
        'url': 'https://medium.com/feed/@SamouraiWallet'
    },

    'samourai_wallet_twitter': {
        'tags': ['twitter', 'samourai_wallet'],
        'url': 'https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1'
    },

    'samourai_wallet_youtube': {
        'tags': ['youtube', 'samourai_wallet'],
        'url': 'https://rsshub.app/youtube/channel/UCb4Y89L9Bokuo6OWqjAhMoA'
    },
}

filedic = {
    'ids': './ids.txt',
    'etags': './etags.txt',
    'modifieds': './modifieds.txt',
    'feed': './feed.rss',
    'test_feed': 'feed.test.rss'
}
