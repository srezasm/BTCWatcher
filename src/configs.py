# [rsshub](rsshub.app) is in priority because of [etag and modified](https://pythonhosted.org/feedparser/http-etag.html)
feeddic = {
    'reddit_test': {
        'name': 'ask reddit',
        'tags': ['reddit', 'test'],
        'url': 'https://www.reddit.com/r/AskReddit/new/.rss'
    },

    'samourai_wallet_medium': {
        'tags': ['article', 'medium', 'samourai_wallet'],
        'url': 'https://medium.com/feed/@SamouraiWallet'
    },

    'samourai_wallet_twitter': {
        'name': 'samourai wallet',
        'tags': ['twitter', 'samourai_wallet'],
        'url': 'https://rsshub.app/twitter/user/SamouraiWallet/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },

    'samourai_wallet_youtube': {
        'name': 'samourai wallet',
        'tags': ['youtube', 'samourai_wallet'],
        'url': 'https://rsshub.app/youtube/channel/UCb4Y89L9Bokuo6OWqjAhMoA'
    },
}

filedic = {
    'ids': './ids.txt',
    'etags': './etags.txt',
    'modifieds': './modifieds.txt',
    'feed': './feed.rss',
    'test_feed': './feed.test.rss'
}
