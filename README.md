# ניחושיר

Guess Hebrew songs from a split second of audio. Five songs a day from easy to impossible, plus an endless mode you can filter by decade.

**Play:** https://tisheldev.github.io/nichushir/

Clips are the 30-second previews from the Israeli Apple Music catalog, loaded live from Apple's servers. Nothing is stored in this repo except track IDs.

## Editing the song list

- `src/songs.txt` holds hand-picked songs: `trackId|title|artist|decade|tier`
- `src/catalog.txt` holds the bulk catalog, grouped by artist: `#artist|fame` followed by `trackId|title|year` lines
- `src/template.html` is the game itself

After editing, run `python3 src/build.py` to regenerate `index.html`.

Track IDs come from Apple Music links: the number after `?i=` in a song's share link.
