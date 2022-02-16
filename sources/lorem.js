const fs = require("fs");
const Parser = require("rss-parser");
const { ReadLastId, WriteLastId } = require("../utils");

export async function GetLoremUpdates() {
    const feedName = "twitter_samouraiWallet";

    let parser = new Parser();
    let feed = await parser.parseURL("https://www.reddit.com/r/AskReddit/new/.rss");

    const lastId = await ReadLastId(feedName);
    
    var feedItems = feed.items;
    var newItems = [];

    var lastItemIndex = -1;
    for (let i = 0; i < feedItems.length; i++) {
        const item = feedItems[i];

        if (i == 0 && item.guid == lastId) {
            return [];
        } else if (item.guid == lastId) {
            lastItemIndex = i;
            break;
        } else if (i == feedItems.length - 1) {
            lastItemIndex = i + 1;
            break;
        }
    }

    for (let i = 0; i < feedItems.length; i++) {
        const item = feedItems[i];
        if (lastItemIndex != i) {
            item.content = item.content + "\n\n" + "#twitter #samourai_wallet\n" + item.link;
            newItems.push(item);
        } else {
            break;
        }
    }

    WriteLastId(feedName, newItems[0].guid);
    return newItems;
}
