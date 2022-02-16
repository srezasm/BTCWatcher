const fs = require("fs");
const lastIdsFileName = "lastIds.txt";
const idSplitter = " |$plit| ";

export async function ReadLastId(name) {
    const content = await fs.readFile(lastIdsFileName).toString().split("\n");
    content.forEach((line) => {
        if (line.startsWith(name)) {
            return line.split(idSplitter);
        }
    });
}

export async function WriteLastId(name, id) {
    var content = await fs.readFile(lastIdsFileName).toString().split("\n");
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
