import { GetUpdates } from "./utils.js";
import feeds from "./feeds.js";

export default function () {
    var feedList = feeds;
    
    //#region twitter samourai
    var twitterSamourai = GetUpdates(feedList.twitter_samourai);
    twitterSamourai.forEach((item) => {
        item.title = item.title + "\n\n" + "#twitter #samourai_wallet\n" + item.link;
    });
    //#endregion

    //#region medium samourai
    var mediumSamourai = GetUpdates(feedList.medium_samourai);
    mediumSamourai.forEach((item) => {
        item.title = item.title + "\n\n" + "#article #samourai_wallet" + item.link;
    });
    //#endregion


    //#region youtube samourai
    var youtubeSamourai = GetUpdates(feedList.youtube_samourai);
    youtubeSamourai.forEach(item => {
        item.title = item.title + "\n\n" + "#youtube #samourai_wallet" + item.link;
    });
    //#endregion
}
