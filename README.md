# The World in One Day — Sunday 22 November 2026

[![competition](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/revan997/news-image-20261122-r2/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/revan997/news-image-20261122-r2/reward.svg)](https://make.fun/bounty/news-image-20261122)

A one-page newspaper front page summing up the world's news of
Sunday, 22 November 2026, drawn with Pillow (flat illustration, no
generated imagery, no text inside the illustrations).

Lead story: **COP31 COLLAPSES** — climate talks in Antalya end with no
deal as the EU and ~130 parties reject the Antalya Pact, which says
nothing about fossil fuels. Also inside: two tankers hit by mines in
the Strait of Hormuz, a drone strike on flats in Dymer (2 dead,
14 missing), the Russian corvette Merkury sunk at Benghazi, three
Russian Kh-101 cruise missiles confirmed over Poland, drones over
Khartoum, a Delta systems outage delaying 1,600+ flights, a candy
factory fire in Cikande (3 dead, 36 missing), and sport — Márquez's
record-equalling eighth MotoGP title.

**39 stories, 7 regions** — lead + 2 big stories + 12 grid cards +
24 numbered "Also on Sunday" items, plus a stat strip ("The Day in
Numbers"), a UTC timeline ("The Day in UTC"), a dotted world map
("Where It Happened"), and a "Date Check" box explaining what was
dated to Sunday and what was deliberately left out.

## Run

```sh
python3 draw.py            # renders entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # validates + copies
```

`main.py` (Python standard library only) validates `entry.png` as a
whole PNG — magic, 1024×1024 IHDR, per-chunk CRCs, IEND trailer, no
trailing bytes, ≤ 1 MiB, IDAT inflates cleanly — copies it byte-for-byte
to `$MAKEFUN_OUTPUT_DIR/entry.png`, then re-reads the copy and
re-validates it. Deterministic: both runs write identical bytes.

## Sources

Every story was first reported on Sunday 22 November 2026. Lead and
grid stories are sourced from wire reporting (AFP, Reuters, AP, BBC);
the numbered "Also on Sunday" items are mostly sourced from a single
daily aggregator ("Daily Summary of World 22 Nov") — see the
"Date Check" box in the image itself for the dating rules and the
deliberate exclusions (ICJ Myanmar ruling 19 Nov, BepiColombo 21 Nov,
El Chapo Isidro capture 20–21 Nov).
