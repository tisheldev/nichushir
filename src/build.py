"""Merge the hand-checked songs with the crawled catalog and write nichushir.html."""
import json, re, collections, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

ALIAS = {  # fold duet credits into the lead artist so "right artist" hints stay consistent
    "גלי עטרי וחלב ודבש": "גלי עטרי",
    "סאבלימינל והצל": "סאבלימינל",
    "הפרויקט של עידן רייכל": "עידן רייכל",
    "אושר כהן ונועה קירל": "אושר כהן",
    "סטטיק ובן אל ונטע": "סטטיק ובן אל",
    "סטטיק ובן אל ואנה זק": "סטטיק ובן אל",
}

# Decade range each older artist was active in. Catalog dates for these artists often come from
# later compilations, so dates outside the range are pulled back into it.
ERA = {
 "יפה ירקוני": (60, 60), "הדודאים": (60, 70), "אריק לביא": (60, 70), "החלונות הגבוהים": (60, 60),
 "אסתר עופרים": (60, 70), "שולי נתן": (60, 60), 'להקת הנח"ל': (60, 70), "גאולה גיל": (60, 70),
 "הפרברים": (60, 80), "אילן ואילנית": (70, 70), "יהורם גאון": (60, 80), "נעמי שמר": (60, 80),
 "אריק איינשטיין": (60, 2000), "נחמה הנדל": (60, 60), "שמוליק קראוס": (60, 80), "ג'וזי כץ": (60, 80),
 "הגשש החיוור": (60, 80), "אריס סאן": (60, 60), "כוורת": (70, 70), "חוה אלברשטיין": (60, 90),
 "אילנית": (70, 80), "גלי עטרי": (70, 80), "יזהר כהן": (70, 80), "מתי כספי": (70, 90),
 "תמוז": (70, 70), "יהודית רביץ": (70, 2000), "צביקה פיק": (70, 90), "אריאל זילבר": (70, 90),
 "דני סנדרסון": (70, 2000), "גידי גוב": (70, 2000), "שלמה גרוניך": (70, 90), "מיקי גבריאלוב": (70, 80),
 "יוסי בנאי": (60, 90), "ירדנה ארזי": (70, 80), "הכל עובר חביבי": (70, 80), "עופרה חזה": (70, 90),
 "חדוה עמרני": (60, 70), "חדוה ודוד": (70, 70), "שולה חן": (60, 80), "עוזי חיטמן": (70, 90),
 "בני אמדורסקי": (60, 70), "זוהר ארגוב": (80, 80), "תיסלם": (80, 80), "חיים משה": (80, 2000),
 "בועז שרעבי": (70, 90), "נורית גלרון": (70, 90), "אבנר גדסי": (70, 90), "ריקי גל": (70, 90),
 "גזוז": (70, 80), "פורטיסחרוף": (80, 90), "דקלון": (70, 2000), "ג'ו עמר": (60, 80),
 "אביהו מדינה": (80, 2000), "יגאל בשן": (70, 90), "דורון מזר": (80, 2000), "אלי לוזון": (80, 2000),
 "מזי כהן": (80, 2000), "דויד ברוזה": (70, 2000), "יוני רכטר": (70, 90), "דני רובס": (80, 2000),
}
DROP_IDS = {1597899516, 777630753, 1257515637}  # spelling variants of songs already listed

def norm(t):
    t = re.sub(r"[֑-ׇ]", "", t)
    t = re.sub(r"[\"'״׳`\-–־.,!?()]", "", t)
    return re.sub(r"\s+", " ", t).strip()

def decade(y):
    if y < 1970: return 60
    if y < 1980: return 70
    if y < 1990: return 80
    if y < 2000: return 90
    if y < 2010: return 2000
    if y < 2020: return 2010
    return 2020

def tkey(t):  # title identity, ignoring spaces and punctuation
    return norm(t).replace(" ", "")

songs, seen_ids, seen_keys, seen_titles = [], set(), set(), set()

for line in open("songs.txt", encoding="utf8").read().strip().split("\n"):
    i, t, a, d, tier = line.split("|")
    a = ALIAS.get(a, a)
    songs.append({"id": int(i), "t": t, "a": a, "d": int(d), "tier": int(tier)})
    seen_ids.add(int(i)); seen_keys.add((a, norm(t))); seen_titles.add(tkey(t))

artist, fame, rank = None, 2, 0
for line in open("catalog.txt", encoding="utf8").read().strip().split("\n"):
    line = line.strip()
    if not line: continue
    if line.startswith("#"):
        artist, f = line[1:].split("|"); fame, rank = int(f), 0
        continue
    i, t, y = line.split("|")
    i, y = int(i), int(y)
    r = rank; rank += 1
    if y >= 2026 or y < 1950 or i in DROP_IDS: continue
    if re.search(r"[A-Za-z&()]|נאמבר", t): continue
    if i in seen_ids or (artist, norm(t)) in seen_keys or tkey(t) in seen_titles: continue
    d = decade(y)
    if artist in ERA:
        lo, hi = ERA[artist]; d = min(max(d, lo), hi)
    # 1 = an artist's biggest hit, 2 = their other big songs, 3 = known, 4 = deep cuts
    tier = (1 if r < 1 else 2 if r < 5 else 3) if fame == 1 else (3 if r < 2 else 4)
    songs.append({"id": i, "t": t, "a": artist, "d": d, "tier": tier})
    seen_ids.add(i); seen_keys.add((artist, norm(t))); seen_titles.add(tkey(t))

songs.sort(key=lambda s: (s["d"], s["a"], s["t"]))
print(len(songs), "songs")
print("by decade:", dict(sorted(collections.Counter(s["d"] for s in songs).items())))
print("by tier:", dict(sorted(collections.Counter(s["tier"] for s in songs).items())))
print("artists:", len({s["a"] for s in songs}))

js = ",\n".join(json.dumps([s["id"], s["t"], s["a"], s["d"], s["tier"]], ensure_ascii=False) for s in songs)
tpl = open("template.html", encoding="utf8").read()
# compact rows [id, title, artist, decade, tier] -> objects
html = tpl.replace("/*SONGS*/[]", "[\n" + js + "\n].map(([id, t, a, d, tier]) => ({id, t, a, d, tier}))")
open("../index.html", "w", encoding="utf8").write(html)
