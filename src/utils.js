import Parser from "rss-parser";
import * as fs from "fs";
const lastIdsFileName = "lastIds.txt";
const idSplitter = " |$plit| ";

//! Possible bug => check for nullable fields like guid

export function ReadLastId(name) {
    if (!fs.existsSync(lastIdsFileName)) return "";

    const content = fs.readFileSync(lastIdsFileName).toString().split("\n");
    content.forEach((line) => {
        if (line.startsWith(name)) {
            return line.split(idSplitter);
        }
    });

    return "";
}

export function WriteLastId(name, id) {
    var content = fs.readFileSync(lastIdsFileName).toString().split("\n");
    var newContent = [];

    if (content.length != 0) {
        content.forEach((line) => {
            if (line.startsWith(name)) {
                newContent.push(name + idSplitter + id);
            } else {
                newContent.push(line);
            }
        });
    } else newContent.push(name + idSplitter + id);

    fs.writeFileSync(lastIdsFileName, newContent.join("\n"));
}

export function GetUpdates(feedAddress) {
    var feed = new Parser().parseURL(feedAddress).then((items) => {
        console.log(items);
    });

    const lastId = ReadLastId(feedAddress);

    var feedItems = feed.items;
    var newItems = [];

    // Find the index of last recorded item from feed
    // ├── If the index was 0 => feed hasn't updated since last check
    // ├── If the lastId was empty => feed is being read for firat time OR
    //     it has no item in it
    var lastItemIndex = -1;
    for (let i = 0; i < feedItems.length; i++) {
        const item = feedItems[i];

        if (i == 0 && item.guid == lastId) {
            return [];
        } else if (item.guid == lastId) {
            lastItemIndex = i;
            break;
        }

        if (lastId == "") {
            lastItemIndex = i + 1;
            break;
        }
    }

    WriteLastId(feedAddress, newItems[0].guid);
    return newItems;
}
