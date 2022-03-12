import feeds from "./feeds.js";
import Parser from "rss-parser";
import * as fs from "fs";
import { format } from "path";

feedList = [
    { name: "samourai_wallet", type: "article", feedUrl: "https://www.reddit.com/r/AskReddit/new/.rss" },
    // "https://medium.com/feed/@SamouraiWallet",
    // "https://rsshub.app/twitter/user/SamouraiWallet/showEmojiForRetweetAndReply=1&excludeReplies=1&showTimestampInDescription=1",
    // "https://www.youtube.com/feeds/videos.xml?channel_id=UCb4Y89L9Bokuo6OWqjAhMoA",
];

function index() {
    console.log("test");
    // setInterval(() => {
    // Listener();
    // }, 300000);
}

function FormatItem(item, type, name) {
    var item = {};
    item.title = item.title;
    item.content = `${item.link}\n#${type} #${name}`;
    item.link = item.link;
    item.pubDate = item.pubDate;
}

// Get raw new data
function GetData(url, name) {
    var feed = new Parser().parseURL(url); //.then((items) => {
    //    console.log(items);
    //});

    feed.items.forEach((item) => {
        var isLastId = IsLastId(item.guid, name);
    });
}

// Use GetData and format its items using FormatItem
function Listener() {
    feedList.forEach((info) => {
        var newItems = GetData(info.feedUrl, info.name);

        newItems.forEach((item) => {
            FormatItem(item, info.type, info.type);
        });
    });
}

// Get last guid and save nwe guid
function IsLastId(id, name) {
    const idLine = `${name}::${id}`;

    var fileContent = fs.readFileSync(lastIdsFileName).toString();
    var fileLines = fileContent.split("\n");

    var newContent = [];

    if (!fileContent.includes(name)) {
        newContent.push(fileLines);
        newContent.push(idLine);

        fs.writeFileSync("./lastIds.txt", newContent.join("\n"));

        return true;
    }

    fileLines.forEach(line => {
        if (!line.startsWith(name)) continue;

        if (line.startsWith(name)) {
            if (line.includes(id))
                return true;
            else {
                newContent.pop();
                newContent.push(idLine);
                newContent.push(fileLines.slice(Math.max(fileLines.length - fileLines.indexOf(line))));
                
            }
        }
    });

    fs.writeFileSync("./lastIds.txt", newContent.join("\n"));
    return true;
}
