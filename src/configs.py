# [rsshub](rsshub.app) is in priority because of [etag and modified](https://pythonhosted.org/feedparser/http-etag.html)
feeddic = {
    # blog
    'samourai_wallet_medium': {
        'name': 'Samourai Wallet',
        'tags': ['blog', 'samourai_wallet'],
        'url': 'https://medium.com/feed/@SamouraiWallet'
    },

    'that_one_privacy_girl': {
        'name': 'That One Privacy Girl',
        'tags': ['blog', 'that_one_privacy_girl'],
        'url': 'https://enegnei.github.io/This-Month-In-Bitcoin-Privacy/feed.xml'
    },

    'bitcoin_dev_blog': {
        'name': 'Bitcoin Dev',
        'tags': ['blog', 'bitcoin_dev'],
        'url': 'https://bitcoin-dev.blog/feed.xml'
    },

    'muun_blog': {
        'name': 'Muun Blog',
        'tags': ['blog', 'muun_blog'],
        'url': 'https://blog.muun.com/rss/'
    },

    'seth_for_privacy_blog': {
        'name': 'Seth For Privacy',
        'tags': ['blog', 'seth_for_privacy'],
        'url': 'https://blog.sethforprivacy.com/index.xml'
    },

    'bitcoin_core_meetings': {
        'name': 'Bitcoin Core Mittings',
        'tags': ['blog', 'bitcoin_core', 'meetings'],
        'url': 'https://bitcoincore.org/en/meetingrss.xml'
    },

    # release
    'sparrow_wallet_github_release': {
        'name': 'Sparrow Wallet',
        'tags': ['wallet', 'release', 'sparrow_wallet'],
        'url': 'https://github.com/sparrowwallet/sparrow/releases.atom'
    },

    'electrum_wallet_github_release': {
        'name': 'Electrum Wallet',
        'tags': ['wallet', 'release', 'electrum_wallet'],
        'url': 'https://github.com/spesmilo/electrum/tags.atom'
    },

    'bitcoin_core_release': {
        'name': 'Bitcoin Core',
        'tags': ['release', 'bitcoin_core'],
        'url': 'https://bitcoincore.org/en/releasesrss.xml'
    },


    # twitter
    'samourai_wallet_twitter': {
        'name': 'Samourai Wallet',
        'tags': ['twitter', 'samourai_wallet'],
        'url': 'https://rsshub.app/twitter/user/SamouraiWallet/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },

    'in3rsha_twitter': {
        'name': 'Greg Walker',
        'tags': ['twitter', 'in3rsha'],
        'url': 'https://rsshub.app/twitter/user/in3rsha/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },
    
    'aantonop_twitter': {
        'name': 'Andreas',
        'tags': ['twitter', 'aantonop'],
        'url': 'https://rsshub.app/twitter/user/aantonop/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },
    
    '0xB10C_twitter': {
        'name': 'b10c',
        'tags': ['twitter', '0xB10C'],
        'url': 'https://rsshub.app/twitter/user/0xB10C/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },
    
    'LukeDashjr_twitter': {
        'name': '@LukeDashjr@BitcoinHackers.org on Mastodon',
        'tags': ['twitter', 'LukeDashjr'],
        'url': 'https://rsshub.app/twitter/user/LukeDashjr/excludeReplies=1&showEmojiForRetweetAndReply=1'
    },

    # youtube
    'samourai_wallet_youtube': {
        'name': 'Samourai Wallet',
        'tags': ['youtube', 'samourai_wallet'],
        'url': 'https://rsshub.app/youtube/channel/UCb4Y89L9Bokuo6OWqjAhMoA'
    },

    # podcast
    'lightning_junkies_podcast': {
        'name': 'Lightning Junkies',
        'tags': ['podcast', 'lightning_junkies'],
        'url': 'https://lightningjunkies.net/rss/'
    },

    'stephan_livera_podcast': {
        'name': 'Stephan Livera Podcast',
        'tags': ['podcast', 'stephan_livera'],
        'url': 'https://anchor.fm/s/7d083a4/podcast/rss'
    },

    'opt_out_podcast': {
        'name': 'Opt Out',
        'tags': ['podcast', 'opt_out'],
        'url': 'https://feeds.buzzsprout.com/1790481.rss'
    },

}

filedic = {
    'ids': './ids.txt',
    'etags': './etags.txt',
    'modifieds': './modifieds.txt',
    'feed': './feed.rss',
}
