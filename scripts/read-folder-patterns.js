//const arg = process.argv[2];
const fs = require('fs');

module.exports = function (folder) {
  return fs.readdirSync(`./${folder}/`)
    .filter(f => f.endsWith("h2pattern"))
    .sort()
    .map(f =>
      fs.readFileSync(`./${folder}/${f}`).toString()
        .replace(/<pattern_name>([^<]+)</g, (_, name) => `<name>${simplify(name)}<`)
        .replace(/pattern_name/g, "name")
        .split("\n"))
    .map(lines =>
      lines
        .slice(2, lines.length - 2)
        .join("\n"))
    .join("")

}

function simplify (name) {
  return name.replace(/[-_ ]+/g, " ")
    .replace("Fill ", "F")
    .replace("Groove ", "G")
    .replace(/(F[0-9]+) (G[0-9]+)/, (_, g, gg) => `${gg} ${g}`)
}