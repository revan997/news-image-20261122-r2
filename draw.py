#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' - Sunday 22 November 2026.
Fresh build for news-image-20261122 rebuild r2. PIL only, no network.
Renders entry.png (1024x1024) from the verified fact sheet R3.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # margin
CW = W - 2 * M              # content width = 992

PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 30, 36)
NAVY = (20, 50, 79)
TEAL = (14, 107, 107)
GOLD = (178, 106, 0)
GREEN = (30, 107, 58)
PURPLE = (107, 63, 160)
GREY = (90, 90, 88)
RULE = (120, 110, 95)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def center(draw, y, text, fnt, fill=INK, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- data
STATS = [
    ("2,700", "drones in a week — Zelenskyy"),
    ("258", "Democratic House seats"),
    ("$120bn", "adaptation target dropped"),
    ("1,600+", "Delta flights delayed"),
    ("130 days", "of blockade on Iran"),
    ("538", "Lahore AQI, world's worst"),
]

REGIONS = [
    ("EUROPE", NAVY), ("MIDDLE EAST", RED), ("AMERICAS", GREEN),
    ("ASIA-PACIFIC", GOLD), ("AFRICA", PURPLE), ("OCEANIA", TEAL),
    ("WORLD", (51, 51, 51)),
]

TIMELINE = [
    ("00:04", "Gaza toll 1,661"),
    ("00:09", "Teen gamer rescue"),
    ("00:26", "Fred Nile dies, 92"),
    ("04:19", "Indonesia factory fire"),
    ("07:36", "Benghazi depot blast"),
    ("09:41", "Europe protests"),
    ("12:00", "COP31 ends, no deal"),
    ("15:03", "Khartoum drones"),
    ("15:36", "Merkury hit"),
    ("17:13", "Hormuz tankers"),
]

BIG = [
    {
        "tag": "CLIMATE  ·  ANTALYA", "color": TEAL,
        "head": "COP31 COLLAPSES",
        "deck": ("Climate talks in Antalya end with no deal as the EU and ~130 parties "
                 "reject the Antalya Pact — it says nothing about fossil fuels."),
        "art": "globe",
    },
    {
        "tag": "GULF  ·  STRAIT OF HORMUZ", "color": RED,
        "head": "TWO TANKERS HIT BY MINES",
        "deck": ("Iran says two supertankers hit naval mines and caught fire east of the "
                 "Strait of Hormuz. UKMTO separately reports a tanker incident in the "
                 "Gulf of Oman."),
        "art": "tanker",
    },
    {
        "tag": "UKRAINE  ·  NEAR KYIV", "color": NAVY,
        "head": "FLATS HIT NEAR KYIV",
        "deck": ("A Russian drone hits a five-storey block in Dymer; 2 dead, 14 missing. "
                 "Zelenskyy urges the US to release Patriot missiles: ~2,700 drones "
                 "in a week."),
        "art": "flats",
    },
]

GRID = [
    ("LIBYA", RED, "RUSSIAN WARSHIP SINKS AT BENGHAZI",
     "Suspected Ukrainian sea drones hit the corvette Merkury before dawn; 10 hurt. A second vessel is hit that evening."),
    ("USA", NAVY, "DEMOCRATS HIT 258 IN THE HOUSE",
     "AP calls Chuck Hubbard the winner over Virginia Foxx in North Carolina — the largest Democratic majority since 1992."),
    ("GULF", RED, "TWO HURT AS GULF ATTACKS MOUNT",
     "Bahrain says two were hurt Sunday as Iran is blamed for a strike on a civilian site; tankers hit in Hormuz."),
    ("POLAND", NAVY, "ALL THREE WERE RUSSIAN MISSILES",
     "Debris tests confirm the three objects that fell on Friday were Russian Kh-101 cruise missiles. NATO meets Monday."),
    ("SUDAN", PURPLE, "DRONES HIT KHARTOUM HOMES, UN BUILDING",
     "Drones strike homes at dawn; a UN building is damaged with staff inside. Four killed."),
    ("SPORT", GREEN, "MARQUEZ TAKES AN EIGHTH TITLE",
     "Marc Marquez finishes eighth in Portugal to seal a record-equalling eighth MotoGP crown. Alcaraz beats Zverev 6-2, 7-6."),
    ("USA · TRAVEL", NAVY, "DELTA OUTAGE DELAYS 1,600+ FLIGHTS",
     "Weight-and-balance system fails Sunday; FAA ground stop for Atlanta-bound flights; not a hack."),
    ("INDONESIA", GOLD, "CANDY FACTORY FIRE: 3 DEAD, 36 MISSING",
     "Fire at PT Fonusa Agung Mulia, Cikande, Banten; search continues Sunday; 15 rescued alive, 4 hurt."),
    ("IRAN", RED, "IRAN UNVEILS MISSILE CITY",
     "Dual-missile launcher and a new underground missile city shown on state media; IRGC commander Vahidi toured Saturday."),
    ("SAUDI", RED, "SAUDIS INTERCEPT HOUTHI DRONE, MISSILE",
     "Coalition intercepts a Houthi drone and a ballistic missile; Houthis claim a hit on the Rabigh refinery — unconfirmed."),
    ("EUROPE", NAVY, "EUROPE PROTESTS, DAY THREE",
     "Protests across Europe enter a third straight day over living costs and housing; France now six weekends in a row."),
    ("FINLAND", NAVY, "FINLAND: WAR IS SPILLING OVER",
     "After a drone strike on a Russian cargo ship in the Baltic Sea."),
]

ALSO = [
    "UAE condemns Iranian attack on Bahrain.",
    "Ex-Italian police chief found dead amid Sicily inquiry.",
    "Settlers burn 12 vehicles in Ramallah villages.",
    "Eisenkot's Yashar, Netanyahu's Likud talk unity government.",
    "Blast at Benghazi naval-base depot triggers a fire.",
    "Aoun demands Israeli withdrawal on independence eve.",
    "Palestinians protest in Gaza; 350,000 families homeless.",
    "Iran in a \u201csilent economic war\u201d as blockade hits 130 days.",
    "Turkey: Israel blocking container homes for Gaza.",
    "Foundation urges Germany to arrest an Israeli soldier.",
    "Fred Nile, ex-NSW politician, dies aged 92.",
    "Teen gamer and his mother help rescue a missing girl.",
    "Gaza toll since the October 2025 ceasefire reaches 1,661.",
    "Nigeria funeral boat toll rises to 24 dead, 24 rescued.",
    "Trump backs a 10% credit-card rate cap, open to a deal.",
    "Bessent warns the Fed against over-tightening.",
    "Cleverbridge breach: hackers copied card numbers and CVVs.",
    "Fidan: US-Israel war fallout threatens global markets.",
    "Paolo Bulgari, luxury jeweller, dies at 89.",
    "Football: Liverpool thrash Man Utd 4-0; Boca win Copa 2-0.",
    "World Central Kitchen: Gaza dead were not its team.",
    "Turkey: Israel may use Druze support for a Syria operation.",
    "Settlers attack homes in Hebron, Ramallah; tear gas fired.",
    "US Army to detonate lead azide in Iowa despite court pause.",
]

DATE_CHECK = ("Every story above was first reported on Sunday 22 November 2026. Left out on "
              "purpose: the ICJ's Myanmar ruling (19 Nov), BepiColombo's Mercury orbit (21 Nov), "
              "the El Chapo Isidro capture (20\u201321 Nov). Friday/Saturday events appear only "
              "where Sunday brought the toll, the confirmation or the claim: Poland's missiles "
              "(confirmed Sunday), Bahrain (two hurt Sunday), the Nigeria boat toll (announced "
              "Saturday, reported Sunday), the Indonesia fire (search Sunday). Dymer: 2 dead, "
              "14 missing \u2014 Sunday's figures, not Monday's toll.")

# land rectangles (lon_min, lon_max, lat_min, lat_max) for the dotted map
LAND = [
    (-168, -55, 15, 71), (-58, -20, 60, 83), (-105, -77, 7, 20),
    (-78, -35, -5, 12), (-72, -55, -55, -5),
    (-11, 40, 36, 70), (-6, 2, 50, 59),
    (-18, 32, -35, 35), (32, 51, 5, 32),
    (40, 180, 10, 75), (68, 89, 8, 35), (95, 105, 5, 28),
    (95, 141, -11, 6), (129, 146, 31, 45),
    (113, 154, -39, -11), (166, 178, -47, -34),
]
DOTS = [
    (30.7, 36.9), (56.5, 26.6), (30.5, 50.5), (20.1, 32.1), (32.5, 15.6),
    (106.3, -6.2), (50.6, 26.2), (21.0, 58.5), (35.2, 31.9), (34.5, 31.5),
    (-79.0, 35.8), (-8.9, 38.9), (74.3, 31.5),
]


def draw_globe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 53, 87))
    cx, cy, r = x + w // 2, y + h // 2 + 2, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(47, 127, 193),
              outline=(220, 220, 210), width=2)
    d.ellipse([cx - 22, cy - 18, cx - 2, cy - 2], fill=(63, 158, 77))
    d.ellipse([cx + 2, cy + 4, cx + 22, cy + 20], fill=(63, 158, 77))
    d.ellipse([cx - 12, cy + 10, cx + 4, cy + 24], fill=(63, 158, 77))
    crack = [(cx - 26, cy - 26), (cx - 10, cy - 12), (cx - 18, cy + 2),
             (cx - 2, cy + 10), (cx - 10, cy + 22), (cx + 6, cy + 28)]
    d.line(crack, fill=(10, 10, 10), width=4, joint="curve")
    d.line([(cx + 26, cy - 26), (cx + 12, cy - 8), (cx + 22, cy + 6)],
           fill=(10, 10, 10), width=3, joint="curve")


def draw_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(232, 112, 58))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(23, 50, 79))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(18, 40, 64))
    hx, hy = x + 30, y + h - 34
    d.polygon([(hx, hy), (hx + w - 70, hy), (hx + w - 84, hy + 22),
               (hx + 8, hy + 22)], fill=(12, 12, 12))
    d.rectangle([hx + 40, hy - 16, hx + 90, hy], fill=(30, 30, 30))
    d.rectangle([hx + 120, hy - 10, hx + 170, hy], fill=(30, 30, 30))
    fx = hx + 190
    d.polygon([(fx, hy - 6), (fx + 14, hy - 30), (fx + 26, hy - 6)], fill=(255, 140, 0))
    d.polygon([(fx + 22, hy - 6), (fx + 34, hy - 24), (fx + 46, hy - 6)], fill=(255, 200, 40))
    d.ellipse([fx - 2, y + 6, fx + 16, y + 22], fill=(120, 120, 120))
    d.ellipse([fx + 12, y + 2, fx + 32, y + 18], fill=(150, 150, 150))


def draw_flats(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 107, 125))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(60, 60, 58))
    # left block (intact)
    d.rectangle([x + 14, y + 34, x + 92, y + h - 18], fill=(52, 52, 54))
    # middle block, broken top
    d.polygon([(x + 108, y + 52), (x + 128, y + 30), (x + 148, y + 48),
               (x + 168, y + 34), (x + 188, y + 52), (x + 188, y + h - 18),
               (x + 108, y + h - 18)], fill=(38, 38, 40))
    # right block (intact)
    d.rectangle([x + 204, y + 26, x + 282, y + h - 18], fill=(52, 52, 54))
    # lit windows
    for bx in (14, 108, 204):
        for wy in range(y + 44, y + h - 26, 14):
            for wx in (bx + 8, bx + 34, bx + 60):
                if (wx + wy) % 3 == 0:
                    d.rectangle([x + wx, wy, x + wx + 9, wy + 8], fill=(255, 205, 90))
    # impact glow + smoke on the broken block (kept inside the art box)
    d.ellipse([x + 128, y + 52, x + 168, y + 66], fill=(255, 140, 0))
    d.ellipse([x + 138, y + 55, x + 158, y + 65], fill=(255, 210, 80))
    d.ellipse([x + 130, y + 8, x + 152, y + 26], fill=(170, 170, 168))
    d.ellipse([x + 144, y + 2, x + 168, y + 20], fill=(150, 150, 148))
    d.ellipse([x + 118, y + 6, x + 138, y + 22], fill=(185, 185, 182))


ART = {"globe": draw_globe, "tanker": draw_tanker, "flats": draw_flats}


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top bar
    f_top = font(SANS_B, 13)
    d.text((M, 4), "THE WORLD IN ONE DAY", font=f_top, fill=INK)
    right = "39 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    f_top2 = font(SANS_B, 11)
    d.text((W - M - d.textlength(right, font=f_top2), 6), right, font=f_top2, fill=INK)
    d.line([M, 22, W - M, 22], fill=INK, width=2)

    # ---- masthead
    center(d, 26, "Sunday 22 November 2026", font(SERIF_B, 58))
    center(d, 92, "COP31 collapses in Antalya  \u00b7  Two tankers hit by mines off Hormuz  \u00b7  A drone kills two near Kyiv",
           font(SERIF_I, 19), fill=(40, 40, 40))
    d.line([M, 116, W - M, 116], fill=INK, width=1)

    # ---- stat strip
    y0, y1 = 120, 160
    cell = CW // 6
    for i, (num, lab) in enumerate(STATS):
        x = M + i * cell
        if i:
            d.line([x - 4, y0 + 4, x - 4, y1 - 4], fill=RULE, width=1)
        center(d, y0, num, font(SANS_B, 24), fill=RED, cx=x + cell // 2)
        center(d, y0 + 27, lab, font(SANS, 10), fill=GREY, cx=x + cell // 2)
    d.line([M, y1 + 2, W - M, y1 + 2], fill=INK, width=1)

    # ---- region tabs
    ry = 166
    tab_w = CW // 7
    for i, (name, col) in enumerate(REGIONS):
        x = M + i * tab_w
        wdt = tab_w - 2 if i < 6 else tab_w
        d.rectangle([x, ry, x + wdt, ry + 20], fill=col)
        center(d, ry + 4, name, font(SANS_B, 12), fill=(255, 255, 255),
               cx=x + wdt // 2)

    # ---- timeline
    ty = 192
    d.text((M, ty), "THE DAY IN UTC", font=font(SANS_B, 12), fill=INK)
    tl_y = 214
    d.line([M, tl_y, W - M, tl_y], fill=INK, width=2)
    tx0, tx1 = M + 130, W - M
    slot = (tx1 - tx0) / len(TIMELINE)
    for i, (t, ev) in enumerate(TIMELINE):
        cx = tx0 + slot * i + slot / 2
        center(d, tl_y - 15, t, font(SANS_B, 11), fill=RED, cx=int(cx))
        d.ellipse([cx - 3, tl_y - 3, cx + 3, tl_y + 3], fill=RED)
        draw_wrapped(d, int(cx - slot / 2 + 3), tl_y + 6, ev,
                     font(SANS, 9), int(slot - 6), fill=INK, leading=10,
                     max_lines=2)

    # ---- big stories
    by = 244
    col_w = (CW - 20) // 3
    art_h = 68
    for i, s in enumerate(BIG):
        x = M + i * (col_w + 10)
        ART[s["art"]](d, x, by, col_w, art_h)
        yy = by + art_h + 5
        d.text((x, yy), s["tag"], font=font(SANS_B, 10), fill=s["color"])
        yy += 13
        yy = draw_wrapped(d, x, yy, s["head"], font(SERIF_B, 22), col_w,
                          leading=24, max_lines=2)
        yy += 2
        draw_wrapped(d, x, yy, s["deck"], font(SANS, 12), col_w, leading=14,
                     max_lines=3)
    d.line([M, 426, W - M, 426], fill=INK, width=1)

    # ---- grid of 12 cards
    gy = 434
    gw = (CW - 5 * 8) // 6
    gh = 100
    for idx, (tag, col, head, deck) in enumerate(GRID):
        r, c = divmod(idx, 6)
        x = M + c * (gw + 8)
        y = gy + r * (gh + 8)
        d.text((x, y), tag, font=font(SANS_B, 10), fill=col)
        yy = draw_wrapped(d, x, y + 13, head, font(SANS_B, 13), gw,
                          leading=15, max_lines=3)
        draw_wrapped(d, x, yy + 1, deck, font(SANS, 10), gw, leading=12,
                     max_lines=3)
    grid_bottom = gy + 2 * gh + 8

    # ---- map + also on sunday
    ay = grid_bottom + 8
    d.text((M, ay), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    d.text((M + 316, ay), "ALSO ON SUNDAY \u2014 24 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    d.line([M, ay + 18, M + 300, ay + 18], fill=INK, width=1)
    d.line([M + 316, ay + 18, W - M, ay + 18], fill=INK, width=1)

    map_x, map_y, map_w, map_h = M, ay + 24, 300, 200
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(232, 238, 242))
    step = 6
    for gy2 in range(map_y + 3, map_y + map_h - 2, step):
        lat = 75 - (gy2 - map_y) / map_h * 135
        for gx in range(map_x + 3, map_x + map_w - 2, step):
            lon = -180 + (gx - map_x) / map_w * 360
            if any(lo0 <= lon <= lo1 and la0 <= lat <= la1
                   for lo0, lo1, la0, la1 in LAND):
                d.ellipse([gx - 1, gy2 - 1, gx + 1, gy2 + 1], fill=(42, 74, 107))
    for lon, lat in DOTS:
        px = map_x + (lon + 180) / 360 * map_w
        py = map_y + (75 - lat) / 135 * map_h
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
    d.text((map_x, map_y + map_h + 4),
           "Red dots mark the places in today's stories.",
           font=font(SANS, 10), fill=GREY)

    # also-on list, 2 columns x 12
    ax = M + 316
    colw = (W - M - ax - 12) // 2
    f_num = font(SANS_B, 11)
    f_it = font(SANS, 11)
    for i, item in enumerate(ALSO):
        c = 0 if i < 12 else 1
        row = i % 12
        x = ax + c * (colw + 12)
        y = ay + 24 + row * 19
        d.text((x, y), f"{13 + i}.", font=f_num, fill=RED)
        num_w = d.textlength(f"{13 + i}. ", font=f_num)
        d.text((x + num_w, y), item, font=f_it, fill=INK)

    # ---- date check
    dy = ay + 24 + 12 * 19 + 8
    d.rectangle([M, dy, W - M, dy + 88], outline=RED, width=2)
    d.text((M + 10, dy + 6), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    draw_wrapped(d, M + 10, dy + 24, DATE_CHECK, font(SANS, 12), CW - 20,
                 leading=14, max_lines=4)

    # ---- footer
    fy = dy + 88 + 7
    center(d, fy, "ALSO:  Brazil storm toll 5  \u00b7  Lahore AQI 538, world's worst  \u00b7  "
           "Shuri Castle restored, opens Monday  \u00b7  Markets: Taiwan \u221217.5% in a week, "
           "S&P in correction  \u00b7  THE WORLD IN ONE DAY  \u00b7  SUNDAY 22 NOVEMBER 2026",
           font(SANS, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
