import { GetUpdates } from "./utils.js";
import feeds from "./feeds.js";

export default function() {
    var feedList = feeds;

    var twitterSamourai = GetUpdates(feedList.medium_samourai);
    twitterSamourai.forEach((item) => {
        item.content = item.content + "\n\n" + "#twitter #samourai_wallet\n" + item.link;
    });
}
