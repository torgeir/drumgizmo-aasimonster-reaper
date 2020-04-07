const fs = require('fs');
const readPatterns = require('./read-folder-patterns.js');

const { readdirSync, statSync } = require('fs');
const { join } = require('path');

const dirs = p => readdirSync(p).filter(f => statSync(join(p, f)).isDirectory());

// dirs(".")
//   .filter(d => d.indexOf("bpm") != -1)
//   .forEach(d =>
//     dirs(d)
//       .forEach(dd =>
//         dirs(`${d}/${dd}`)
//           .map(ddd => {
//             const folder = `./${d}/${dd}/${ddd}`;
//             return {folder, patterns: readPatterns(folder) };
//           })
//           .forEach(({folder, patterns}) => {
//             const parts = folder.split("/");
//             const song = `${parts[parts.length - 1]}.h2song`
//             console.log(`Creating song "${song}"`);
//             return createSong(song, folder, patterns);
//           })))

dirs(".")
  .filter(d => d.indexOf("bpm") != -1)
  .map(d =>
    dirs(d)
      .map(dd =>
        dirs(`${d}/${dd}`)
          .map(ddd => ({ folder: `./${d}/${dd}/`, patterns: readPatterns(`./${d}/${dd}/${ddd}`) }))
          .flat(2)
          .reduce(function (acc, el) {
            if (!acc) return el;
            acc.patterns = acc.patterns.concat(el.patterns)
            return acc;
          }, null))
      .forEach(({folder, patterns}) => {
        const parts = folder.split("/");
        const song = `${parts[parts.length - 2]}.h2song`
        console.log(`Creating song "${song}"`);
        return createSong(song, folder, patterns);
      }))

function createSong (songName, folder, patterns) {
  fs.writeFileSync(
    `${folder}/${songName}`,
    fs.readFileSync(`./song-front.xml`).toString()
      + patterns
      + fs.readFileSync(`./song-end.xml`).toString())
}

