#!/usr/bin/env python3
"""Draw 'THE WORLD IN ONE DAY' - Sunday 22 November 2026.
Rebuild r3 (from r2): dense-formula execution upgrade.
- Flat illustration panel on top of every grid card (12 mini scenes).
- Enriched big-3 art (conference scene / two tankers / damaged flats).
- Region tabs carry story counts (sum 39). Verification tags + legend.
- Numbered map pins 1-15 (big-3 + grid), caption "pins match story numbers".
- Timeline cut to 6 events. Source tags under each grid deck.
Facts/numbers unchanged from fact sheet R3. PIL only, no network.
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
    if max_lines and len(lines) > max_lines:
        print(f"WARN overflow ({len(lines)}>{max_lines}): {text[:60]!r}")
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

# (name, color, count) — counts sum to 39
REGIONS = [
    ("EUROPE 12", NAVY), ("MIDDLE EAST 14", RED), ("AMERICAS 5", GREEN),
    ("ASIA-PACIFIC 1", GOLD), ("AFRICA 4", PURPLE), ("OCEANIA 1", TEAL),
    ("WORLD 2", (51, 51, 51)),
]

TIMELINE = [
    ("00:04", "Gaza toll 1,661"),
    ("04:19", "Indonesia factory fire"),
    ("07:36", "Benghazi depot blast"),
    ("12:00", "COP31 ends, no deal"),
    ("15:03", "Khartoum drones"),
    ("17:13", "Hormuz tankers"),
]

TAG_FILL = {"REPORTED": (90, 90, 88), "CLAIM": RED, "CONFIRMED": GREEN}

BIG = [
    {
        "num": 1, "tag": "CLIMATE  ·  ANTALYA", "color": TEAL,
        "head": "COP31 COLLAPSES", "verify": "REPORTED",
        "deck": ("Climate talks end with no deal as the EU and ~130 parties "
                 "reject a pact silent on fossil fuels."),
        "art": "globe",
    },
    {
        "num": 2, "tag": "GULF  ·  STRAIT OF HORMUZ", "color": RED,
        "head": "TWO TANKERS HIT BY MINES", "verify": "CLAIM",
        "deck": ("Iran says two supertankers hit mines and caught fire "
                 "east of the Strait of Hormuz."),
        "art": "tanker",
    },
    {
        "num": 3, "tag": "UKRAINE  ·  NEAR KYIV", "color": NAVY,
        "head": "FLATS HIT NEAR KYIV", "verify": "REPORTED",
        "deck": ("A Russian drone hits a five-storey block in Dymer; "
                 "2 dead, 14 missing."),
        "art": "flats",
    },
]

# (num, kicker, color, headline, deck, verify, source)
GRID = [
    (4, "LIBYA", RED, "RUSSIAN WARSHIP SINKS AT BENGHAZI",
     "Suspected Ukrainian sea drones hit the corvette Merkury; 10 hurt.",
     "REPORTED", "AP · Reuters · CNN", "libya"),
    (5, "USA", NAVY, "DEMOCRATS HIT 258 IN THE HOUSE",
     "AP calls Hubbard the winner over Foxx — largest majority since 1992.",
     "REPORTED", "AP · BBC", "house"),
    (6, "GULF", RED, "TWO HURT AS GULF ATTACKS MOUNT",
     "Bahrain says two were hurt Sunday as Iran is blamed for a strike on a civilian site.",
     "CLAIM", "AFP · Al-Monitor", "bahrain"),
    (7, "POLAND", NAVY, "ALL THREE WERE RUSSIAN MISSILES",
     "Debris tests confirm the three objects that fell Friday were Russian Kh-101 cruise missiles.",
     "CONFIRMED", "", "poland"),
    (8, "SUDAN", PURPLE, "KHARTOUM DRONES HIT UN SITE",
     "Drones strike homes at dawn; a UN building is damaged with staff inside. Four killed.",
     "REPORTED", "AFP · Al Jazeera · OCHA", "sudan"),
    (9, "SPORT", GREEN, "MARQUEZ TAKES AN EIGHTH TITLE",
     "Marquez finishes eighth in Portugal for an eighth MotoGP crown. Alcaraz beats Zverev.",
     "REPORTED", "AP · RTHK", "sport"),
    (10, "USA · TRAVEL", NAVY, "DELTA OUTAGE DELAYS 1,600+ FLIGHTS",
     "System fails Sunday; FAA ground stop for Atlanta-bound flights; not a hack.",
     "REPORTED", "ABC", "delta"),
    (11, "INDONESIA", GOLD, "CANDY FACTORY FIRE: 3 DEAD, 36 MISSING",
     "Fire at a candy factory in Cikande; search continues Sunday; 15 rescued alive, 4 hurt.",
     "REPORTED", "Reuters · AP · BBC", "indonesia"),
    (12, "IRAN", RED, "IRAN UNVEILS MISSILE CITY",
     "Iran unveils an underground missile city and dual launcher; Vahidi toured Saturday.",
     "REPORTED", "Daily Summary", "iran"),
    (13, "SAUDI", RED, "SAUDIS INTERCEPT HOUTHI DRONE",
     "Coalition intercepts a Houthi drone and missile; Rabigh refinery hit claim unconfirmed.",
     "REPORTED", "Daily Summary", "saudi"),
    (14, "EUROPE", NAVY, "EUROPE PROTESTS, DAY THREE",
     "Protests enter day three over living costs and housing; France, six weekends running.",
     "REPORTED", "Daily Summary", "europe"),
    (15, "FINLAND", NAVY, "FINLAND: WAR IS SPILLING OVER",
     "Finland warns the war is spilling over after a drone hit a Russian cargo ship.",
     "REPORTED", "Daily Summary", "finland"),
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

LEGEND = ("REPORTED = carried by the day's wires  ·  CLAIM = one side's account, labelled as such  "
          "·  CONFIRMED = verified by tests or multiple outlets")

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
# (lon, lat, story number) — display offsets spread the dense clusters
# (Med/Gulf, US Southeast) so numbered pins stay readable
PINS = [
    (30.7, 36.9, 1), (64.0, 27.0, 2), (32.0, 51.5, 3), (14.0, 28.0, 4),
    (-76.0, 38.0, 5), (50.6, 30.0, 6), (17.0, 53.5, 7), (27.0, 10.0, 8),
    (-8.9, 38.9, 9), (-88.0, 30.0, 10), (106.3, -6.2, 11), (55.0, 40.0, 12),
    (39.0, 18.0, 13), (2.3, 48.9, 14), (26.0, 61.0, 15),
]


# ---------------------------------------------------------------- big art
def draw_globe(d, x, y, w, h):
    """COP31: conference hall — globe on stand, delegates at a long table, clock."""
    d.rectangle([x, y, x + w, y + h], fill=(13, 48, 74))
    d.rectangle([x, y, x + w, y + 12], fill=(10, 38, 58))
    # wall panels
    for px in (x + 8, x + w - 58):
        d.rectangle([px, y + 16, px + 50, y + 34], fill=(18, 62, 92))
    # clock (top right)
    cx, cy, r = x + w - 26, y + 30, 11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 236, 224),
              outline=(200, 170, 60), width=2)
    d.line([cx, cy, cx, cy - 7], fill=INK, width=2)
    d.line([cx, cy, cx + 5, cy + 2], fill=INK, width=2)
    # globe centre-left on a stand
    gx, gy, gr = x + 62, y + 30, 20
    d.rectangle([gx - 3, gy + gr - 2, gx + 3, gy + gr + 8], fill=(200, 170, 60))
    d.rectangle([gx - 14, gy + gr + 8, gx + 14, gy + gr + 11], fill=(200, 170, 60))
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(47, 127, 193),
              outline=(220, 220, 210), width=2)
    d.ellipse([gx - 15, gy - 12, gx - 2, gy - 1], fill=(63, 158, 77))
    d.ellipse([gx + 1, gy + 3, gx + 15, gy + 15], fill=(63, 158, 77))
    d.ellipse([gx - 8, gy + 7, gx + 3, gy + 16], fill=(63, 158, 77))
    crack = [(gx - 17, gy - 17), (gx - 7, gy - 8), (gx - 12, gy + 1),
             (gx - 1, gy + 7), (gx - 7, gy + 15), (gx + 4, gy + 19)]
    d.line(crack, fill=(10, 10, 10), width=3, joint="curve")
    # delegates behind the table (right side)
    cols = [(176, 30, 36), (220, 220, 210), (30, 107, 58), (178, 106, 0),
            (107, 63, 160), (220, 220, 210)]
    for i, c in enumerate(cols):
        hx = x + 118 + i * 33
        d.ellipse([hx - 7, y + 18, hx + 7, y + 32], fill=(232, 196, 160))
        d.polygon([(hx - 11, y + 46), (hx + 11, y + 46), (hx + 8, y + 32),
                   (hx - 8, y + 32)], fill=c)
    # long conference table + papers + mics
    d.rectangle([x, y + 46, x + w, y + h], fill=(96, 62, 32))
    d.rectangle([x, y + 46, x + w, y + 50], fill=(128, 84, 44))
    for px in range(x + 14, x + w - 20, 44):
        d.rectangle([px, y + 53, px + 26, y + 60], fill=(240, 236, 224))
    for mx in (x + 150, x + 230, x + 290):
        d.line([mx, y + 52, mx, y + 42], fill=(20, 20, 20), width=2)
        d.ellipse([mx - 3, y + 39, mx + 3, y + 45], fill=(20, 20, 20))


def draw_tanker(d, x, y, w, h):
    """Hormuz: sunset sea, two tankers smoking/burning, mines in the water."""
    d.rectangle([x, y, x + w, y + h * 0.45], fill=(232, 112, 58))
    d.ellipse([x + w - 52, y + 4, x + w - 22, y + 34], fill=(255, 214, 130))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(23, 50, 79))
    d.rectangle([x, y + h * 0.45, x + w, y + h * 0.45 + 3], fill=(255, 200, 90))
    # far tanker (right, smaller)
    fx, fy = x + w - 128, y + h - 30
    d.polygon([(fx, fy), (fx + 108, fy), (fx + 98, fy + 14), (fx + 8, fy + 14)],
              fill=(70, 90, 115))
    d.rectangle([fx + 10, fy + 9, fx + 96, fy + 12], fill=(176, 30, 36))
    d.rectangle([fx + 62, fy - 12, fx + 84, fy], fill=(225, 225, 225))
    d.rectangle([fx + 66, fy - 9, fx + 80, fy - 5], fill=(20, 50, 79))
    d.polygon([(fx + 20, fy - 2), (fx + 30, fy - 20), (fx + 40, fy - 2)],
              fill=(255, 140, 0))
    d.ellipse([fx + 16, y + 8, fx + 34, y + 22], fill=(120, 120, 120))
    d.ellipse([fx + 28, y + 2, fx + 48, y + 16], fill=(150, 150, 150))
    # near tanker (left, larger, burning)
    hx, hy = x + 12, y + h - 26
    d.polygon([(hx, hy), (hx + 168, hy), (hx + 154, hy + 18), (hx + 8, hy + 18)],
              fill=(52, 74, 102))
    d.rectangle([hx + 10, hy + 12, hx + 152, hy + 15], fill=(176, 30, 36))
    d.rectangle([hx + 14, hy - 16, hx + 56, hy], fill=(225, 225, 225))
    d.rectangle([hx + 18, hy - 12, hx + 52, hy - 8], fill=(20, 50, 79))
    d.rectangle([hx + 96, hy - 10, hx + 138, hy], fill=(225, 225, 225))
    fx2 = hx + 150
    d.polygon([(fx2, hy - 2), (fx2 + 12, hy - 26), (fx2 + 24, hy - 2)],
              fill=(255, 140, 0))
    d.polygon([(fx2 + 18, hy - 2), (fx2 + 28, hy - 20), (fx2 + 38, hy - 2)],
              fill=(255, 200, 40))
    d.ellipse([fx2 - 4, y + 10, fx2 + 14, y + 26], fill=(120, 120, 120))
    d.ellipse([fx2 + 10, y + 4, fx2 + 30, y + 20], fill=(150, 150, 150))
    # mines (spiky black circles) + wave lines
    for mx, my in ((x + 210, y + h - 10), (x + 250, y + h - 6), (x + 60, y + h - 6)):
        d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(8, 8, 8))
        for dx, dy in ((-6, 0), (6, 0), (0, -6), (-4, -4), (4, -4)):
            d.line([mx, my, mx + dx, my + dy], fill=(8, 8, 8), width=1)
    for wy in (y + h - 14, y + h - 8):
        d.line([x + 4, wy, x + w - 4, wy], fill=(70, 110, 150), width=1)


def draw_flats(d, x, y, w, h):
    """Dymer: dusk sky, three tall blocks, middle one broken open, smoke + glow."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 74, 96))
    d.ellipse([x + w - 40, y + 6, x + w - 16, y + 30], fill=(226, 214, 180))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(40, 40, 38))
    # left block (intact, tall)
    d.rectangle([x + 10, y + 16, x + 96, y + h - 16], fill=(72, 72, 76))
    # middle block, broken top + exposed floors
    d.polygon([(x + 108, y + 34), (x + 128, y + 18), (x + 148, y + 30),
               (x + 168, y + 22), (x + 188, y + 34), (x + 188, y + h - 16),
               (x + 108, y + h - 16)], fill=(48, 48, 52))
    d.rectangle([x + 112, y + 34, x + 184, y + 38], fill=(255, 140, 0))
    d.rectangle([x + 112, y + 38, x + 184, y + 42], fill=(120, 60, 30))
    # right block (intact, taller)
    d.rectangle([x + 200, y + 10, x + 292, y + h - 16], fill=(72, 72, 76))
    # lit windows on all three blocks (rows every 11 px)
    for bx, bw, top in ((10, 86, 22), (108, 80, 44), (200, 92, 16)):
        for wy in range(y + top, y + h - 22, 11):
            for wx in range(bx + 8, bx + bw - 10, 22):
                if (wx + wy) % 3 == 0:
                    d.rectangle([x + wx, wy, x + wx + 9, wy + 7], fill=(255, 205, 90))
                elif (wx + wy) % 5 == 0:
                    d.rectangle([x + wx, wy, x + wx + 9, wy + 7], fill=(140, 160, 190))
    # impact glow + smoke rising from the broken block
    d.ellipse([x + 126, y + 38, x + 170, y + 50], fill=(255, 140, 0))
    d.ellipse([x + 136, y + 41, x + 160, y + 49], fill=(255, 210, 80))
    d.ellipse([x + 128, y + 2, x + 152, y + 18], fill=(170, 170, 168))
    d.ellipse([x + 144, y + 0, x + 168, y + 14], fill=(150, 150, 148))
    d.ellipse([x + 116, y + 0, x + 138, y + 14], fill=(185, 185, 182))
    # rubble at the base of the broken block
    for rx, rw in ((112, 14), (132, 20), (158, 12), (172, 16)):
        d.polygon([(x + rx, y + h - 16), (x + rx + rw // 2, y + h - 24),
                   (x + rx + rw, y + h - 16)], fill=(90, 86, 78))



ART = {"globe": draw_globe, "tanker": draw_tanker, "flats": draw_flats}


# ---------------------------------------------------------------- grid mini art
def _sea(d, x, y, w, h, sky, sea):
    d.rectangle([x, y, x + w, y + h * 0.55], fill=sky)
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=sea)


def _smoke(d, x, y, r=5):
    d.ellipse([x, y, x + r * 2, y + r * 2], fill=(120, 120, 120))
    d.ellipse([x + 6, y - 5, x + 6 + r * 2, y - 5 + r * 2], fill=(150, 150, 150))


def _flame(d, x, y, s=10):
    d.polygon([(x, y), (x + s // 2, y - s), (x + s, y)], fill=(255, 140, 0))
    d.polygon([(x + s // 2, y), (x + s, y - s // 2), (x + s + s // 2, y)],
              fill=(255, 200, 40))


def art_libya(d, x, y, w, h):
    _sea(d, x, y, w, h, (200, 214, 226), (23, 50, 79))
    d.polygon([(x + 18, y + h - 18), (x + w - 24, y + h - 18),
               (x + w - 34, y + h - 8), (x + 28, y + h - 8)], fill=(60, 60, 62))
    d.polygon([(x + 18, y + h - 18), (x + 60, y + h - 18),
               (x + 52, y + h - 26), (x + 26, y + h - 26)], fill=(90, 90, 92))
    d.rectangle([x + 66, y + h - 30, x + 84, y + h - 18], fill=(30, 30, 30))
    _smoke(d, x + 70, y + 4)
    _flame(d, x + 96, y + h - 18, 12)
    d.ellipse([x + 120, y + 6, x + 128, y + 14], fill=(30, 30, 30))
    d.line([x + 120, y + 10, x + 128, y + 10], fill=(30, 30, 30), width=1)


def art_house(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 50, 79))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(200, 170, 60))
    cx = x + w // 2
    d.ellipse([cx - 26, y + 6, cx + 26, y + 30], fill=(240, 236, 224))
    d.rectangle([cx - 30, y + 24, cx + 30, y + 30], fill=(240, 236, 224))
    for i in range(5):
        px = cx - 28 + i * 13
        d.rectangle([px, y + 30, px + 7, y + h - 8], fill=(240, 236, 224))
    d.rectangle([cx - 34, y + h - 12, cx + 34, y + h - 8], fill=(240, 236, 224))
    d.line([cx, y + 6, cx, y - 0 + 2], fill=(240, 236, 224), width=1)
    d.polygon([(cx, y + 1), (cx + 10, y + 4), (cx, y + 7)], fill=(176, 30, 36))


def art_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 150, 90))
    d.rectangle([x, y + h * 0.5, x + w, y + h], fill=(60, 52, 48))
    for bx, bw, bh in ((8, 34, 22), (48, 26, 30), (80, 40, 18), (124, 26, 26)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(30, 30, 32))
        for wy in range(y + h - bh + 4, y + h - 4, 8):
            d.rectangle([x + bx + 5, wy, x + bx + 11, wy + 4], fill=(255, 205, 90))
    _flame(d, x + 100, y + 16, 16)
    _smoke(d, x + 106, y + 2)
    d.ellipse([x + 128, y + 4, x + 136, y + 12], fill=(255, 200, 40))


def art_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.6], fill=(180, 200, 220))
    d.rectangle([x, y + h * 0.6, x + w, y + h], fill=(63, 158, 77))
    d.polygon([(x + 40, y + 22), (x + 118, y + 10), (x + 122, y + 16),
               (x + 44, y + 28)], fill=(90, 90, 92))
    d.polygon([(x + 118, y + 10), (x + 132, y + 13), (x + 122, y + 16)],
              fill=(176, 30, 36))
    d.polygon([(x + 40, y + 22), (x + 30, y + 16), (x + 34, y + 26)],
              fill=(60, 60, 62))
    for dx, dy in ((60, 32), (88, 36), (110, 30)):
        d.ellipse([x + dx, y + dy, x + dx + 4, y + dy + 4], fill=(60, 60, 62))
    d.ellipse([x + 14, y + 6, x + 30, y + 20], fill=(255, 255, 255))
    d.ellipse([x + 120, y + 4, x + 138, y + 18], fill=(255, 255, 255))


def art_sudan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 24, 40))
    d.ellipse([x + w - 30, y + 4, x + w - 12, y + 22], fill=(226, 214, 180))
    for bx, bw, bh in ((6, 40, 26), (52, 30, 34), (88, 44, 20), (128, 24, 30)):
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(40, 40, 46))
        for wy in range(y + h - bh + 4, y + h - 4, 9):
            d.rectangle([x + bx + 5, wy, x + bx + 11, wy + 4], fill=(255, 205, 90))
    _flame(d, x + 60, y + h - 34, 12)
    _smoke(d, x + 64, y + h - 44)
    d.rectangle([x + 108, y + 8, x + 124, y + 14], fill=(120, 120, 120))
    d.line([x + 104, y + 8, x + 128, y + 8], fill=(120, 120, 120), width=1)
    d.line([x + 104, y + 14, x + 128, y + 14], fill=(120, 120, 120), width=1)


def art_sport(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 107, 58))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(240, 236, 224))
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(176, 30, 36))
    # checkered flag
    for i in range(4):
        for j in range(3):
            d.rectangle([x + 118 + i * 7, y + 4 + j * 7,
                         x + 118 + i * 7 + 7, y + 4 + j * 7 + 7],
                        fill=(17, 17, 17) if (i + j) % 2 == 0 else (255, 255, 255))
    d.line([x + 118, y + 4, x + 118, y + 32], fill=(120, 90, 40), width=2)
    # motorcycle silhouette
    wx1, wx2, wy = x + 30, x + 86, y + h - 16
    d.ellipse([wx1 - 8, wy - 8, wx1 + 8, wy + 8], fill=(17, 17, 17))
    d.ellipse([wx2 - 8, wy - 8, wx2 + 8, wy + 8], fill=(17, 17, 17))
    d.ellipse([wx1 - 4, wy - 4, wx1 + 4, wy + 4], fill=(200, 200, 200))
    d.ellipse([wx2 - 4, wy - 4, wx2 + 4, wy + 4], fill=(200, 200, 200))
    d.polygon([(wx1, wy), (wx2, wy), (wx2 - 6, wy - 14), (wx1 + 14, wy - 12)],
              fill=(176, 30, 36))
    d.ellipse([wx1 + 22, wy - 24, wx1 + 32, wy - 14], fill=(232, 196, 160))
    d.polygon([(wx1 + 20, wy - 12), (wx1 + 34, wy - 12), (wx1 + 30, wy - 20),
               (wx1 + 22, wy - 20)], fill=(20, 50, 79))


def art_delta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 230))
    d.ellipse([x + 10, y + 6, x + 40, y + 18], fill=(255, 255, 255))
    d.ellipse([x + 96, y + 12, x + 132, y + 24], fill=(255, 255, 255))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 90, 88))
    d.line([x, y + h - 5, x + w, y + h - 5], fill=(255, 255, 255), width=1)
    # airplane
    cx, cy = x + w // 2, y + 24
    d.polygon([(cx - 52, cy), (cx + 44, cy - 4), (cx + 56, cy),
               (cx + 44, cy + 4), (cx - 52, cy + 3)], fill=(255, 255, 255))
    d.polygon([(cx - 8, cy), (cx + 6, cy - 12), (cx + 12, cy - 12),
               (cx + 2, cy)], fill=(255, 255, 255))
    d.polygon([(cx - 8, cy + 2), (cx + 2, cy + 12), (cx + 8, cy + 12),
               (cx + 0, cy + 2)], fill=(230, 230, 230))
    d.polygon([(cx - 52, cy), (cx - 62, cy - 8), (cx - 62, cy + 6)],
              fill=(176, 30, 36))
    for wx in range(cx - 44, cx + 36, 10):
        d.rectangle([wx, cy - 1, wx + 4, cy + 2], fill=(20, 50, 79))


def art_indonesia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 150, 90))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 52, 48))
    # factory with sawtooth roof + chimney
    d.rectangle([x + 14, y + h - 30, x + 108, y + h - 14], fill=(90, 84, 78))
    for i in range(4):
        px = x + 14 + i * 24
        d.polygon([(px, y + h - 30), (px + 12, y + h - 40), (px + 24, y + h - 30)],
                  fill=(70, 64, 58))
    d.rectangle([x + 116, y + 8, x + 128, y + h - 14], fill=(70, 64, 58))
    _flame(d, x + 30, y + h - 30, 16)
    _flame(d, x + 62, y + h - 30, 12)
    _smoke(d, x + 116, y + 2)
    _smoke(d, x + 96, y + 6)
    d.rectangle([x + 24, y + h - 24, x + 34, y + h - 18], fill=(255, 205, 90))
    d.rectangle([x + 78, y + h - 24, x + 88, y + h - 18], fill=(255, 205, 90))


def art_iran(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 170, 120))
    d.polygon([(x, y + h), (x + w // 2, y + 2), (x + w, y + h)], fill=(120, 90, 60))
    d.polygon([(x + w // 2 - 12, y + 16), (x + w // 2 + 12, y + 16),
               (x + w // 2, y + 2)], fill=(240, 236, 224))
    # tunnel entrance
    d.pieslice([x + w // 2 - 16, y + h - 22, x + w // 2 + 16, y + h + 6],
               180, 360, fill=(20, 20, 20))
    # missile on launcher, right side
    mx = x + w - 34
    d.rectangle([mx - 3, y + 12, mx + 3, y + 34], fill=(220, 220, 220))
    d.polygon([(mx - 3, y + 12), (mx, y + 4), (mx + 3, y + 12)], fill=(176, 30, 36))
    d.polygon([(mx - 3, y + 34), (mx - 8, y + 40), (mx - 3, y + 38)], fill=(90, 90, 92))
    d.polygon([(mx + 3, y + 34), (mx + 8, y + 40), (mx + 3, y + 38)], fill=(90, 90, 92))
    d.rectangle([mx - 8, y + 40, mx + 8, y + 44], fill=(60, 60, 62))
    d.ellipse([x + 12, y + 6, x + 30, y + 16], fill=(255, 255, 255))


def art_saudi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 50, 79))
    for sx, sy in ((30, 10), (90, 6), (130, 14)):
        d.ellipse([x + sx, y + sy, x + sx + 16, y + sy + 8], fill=(255, 255, 255))
    # interceptor burst
    bx, by = x + w // 2, y + 20
    for ang in range(0, 360, 30):
        import math
        dx, dy = math.cos(math.radians(ang)) * 12, math.sin(math.radians(ang)) * 12
        d.line([bx, by, bx + dx, by + dy], fill=(255, 200, 40), width=2)
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(255, 140, 0))
    # drone above, shield dome below
    d.rectangle([x + 18, y + 8, x + 34, y + 14], fill=(120, 120, 120))
    d.line([x + 12, y + 8, x + 40, y + 8], fill=(120, 120, 120), width=1)
    d.pieslice([x + 30, y + h - 24, x + w - 30, y + h + 10], 180, 360,
               fill=(47, 127, 193))
    d.rectangle([x + 30, y + h - 8, x + w - 30, y + h], fill=(47, 127, 193))


def art_europe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 180))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(120, 100, 80))
    cols = [(176, 30, 36), (20, 50, 79), (30, 107, 58), (178, 106, 0),
            (107, 63, 160), (220, 220, 210), (176, 30, 36)]
    for i, c in enumerate(cols):
        hx = x + 14 + i * 21
        d.line([hx, y + 12, hx, y + 24], fill=(90, 70, 40), width=2)
        d.rectangle([hx - 8, y + 2, hx + 8, y + 14], fill=(255, 255, 255),
                    outline=(90, 70, 40))
        d.ellipse([hx - 6, y + 22, hx + 6, y + 34], fill=(232, 196, 160))
        d.polygon([(hx - 9, y + h - 10), (hx + 9, y + h - 10), (hx + 7, y + 34),
                   (hx - 7, y + 34)], fill=c)


def art_finland(d, x, y, w, h):
    _sea(d, x, y, w, h, (180, 200, 220), (23, 50, 79))
    d.rectangle([x + 16, y + h - 20, x + w - 16, y + h - 8], fill=(30, 30, 30))
    for i, c in enumerate([(176, 30, 36), (178, 106, 0), (30, 107, 58), (20, 50, 79)]):
        d.rectangle([x + 22 + i * 28, y + h - 34, x + 22 + i * 28 + 24, y + h - 20],
                    fill=c)
    d.rectangle([x + w - 40, y + h - 32, x + w - 22, y + h - 20], fill=(220, 220, 220))
    _smoke(d, x + w - 36, y + h - 44)
    d.rectangle([x + 30, y + 8, x + 46, y + 14], fill=(120, 120, 120))
    d.line([x + 24, y + 8, x + 52, y + 8], fill=(120, 120, 120), width=1)
    d.line([x + 24, y + 14, x + 52, y + 14], fill=(120, 120, 120), width=1)
    for wx in (x + 60, x + 110):
        d.line([wx, y + h - 8, wx + 10, y + h - 4], fill=(255, 255, 255), width=1)


MINI_ART = {
    "libya": art_libya, "house": art_house, "bahrain": art_bahrain,
    "poland": art_poland, "sudan": art_sudan, "sport": art_sport,
    "delta": art_delta, "indonesia": art_indonesia, "iran": art_iran,
    "saudi": art_saudi, "europe": art_europe, "finland": art_finland,
}


def verify_chip(d, x_right, y, tag):
    """Small verification chip, right-aligned at x_right."""
    f = font(SANS_B, 8)
    tw = d.textlength(tag, font=f)
    bw, bh = int(tw) + 10, 12
    x0 = x_right - bw
    d.rectangle([x0, y, x0 + bw, y + bh], fill=TAG_FILL[tag])
    d.text((x0 + 5, y + 2), tag, font=f, fill=(255, 255, 255))
    return x0


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
    center(d, 90, "COP31 collapses in Antalya  \u00b7  Two tankers hit by mines off Hormuz  \u00b7  A drone kills two near Kyiv",
           font(SERIF_I, 19), fill=(40, 40, 40))
    d.line([M, 114, W - M, 114], fill=INK, width=1)

    # ---- stat strip
    y0, y1 = 118, 158
    cell = CW // 6
    for i, (num, lab) in enumerate(STATS):
        x = M + i * cell
        if i:
            d.line([x - 4, y0 + 4, x - 4, y1 - 4], fill=RULE, width=1)
        center(d, y0, num, font(SANS_B, 24), fill=RED, cx=x + cell // 2)
        center(d, y0 + 27, lab, font(SANS, 10), fill=GREY, cx=x + cell // 2)
    d.line([M, y1 + 2, W - M, y1 + 2], fill=INK, width=1)

    # ---- region tabs (with counts, sum 39)
    ry = 164
    tab_w = CW // 7
    for i, (name, col) in enumerate(REGIONS):
        x = M + i * tab_w
        wdt = tab_w - 2 if i < 6 else tab_w
        d.rectangle([x, ry, x + wdt, ry + 20], fill=col)
        center(d, ry + 4, name, font(SANS_B, 12), fill=(255, 255, 255),
               cx=x + wdt // 2)

    # ---- timeline (6 events)
    ty = 190
    d.text((M, ty), "THE DAY IN UTC", font=font(SANS_B, 12), fill=INK)
    tl_y = 210
    d.line([M, tl_y, W - M, tl_y], fill=INK, width=2)
    tx0, tx1 = M + 130, W - M
    slot = (tx1 - tx0) / len(TIMELINE)
    for i, (t, ev) in enumerate(TIMELINE):
        cx = tx0 + slot * i + slot / 2
        center(d, tl_y - 15, t, font(SANS_B, 11), fill=RED, cx=int(cx))
        d.ellipse([cx - 3, tl_y - 3, cx + 3, tl_y + 3], fill=RED)
        center(d, tl_y + 6, ev, font(SANS, 10), fill=INK, cx=int(cx))

    # ---- big stories
    by = 232
    col_w = (CW - 20) // 3
    art_h = 68
    for i, s in enumerate(BIG):
        x = M + i * (col_w + 10)
        ART[s["art"]](d, x, by, col_w, art_h)
        # story-number badge on the art
        bx, byy, br = x + 12, by + 12, 10
        d.ellipse([bx - br, byy - br, bx + br, byy + br], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(s["num"])
        nf = font(SANS_B, 11)
        d.text((bx - d.textlength(num, font=nf) / 2, byy - 8), num,
               font=nf, fill=(255, 255, 255))
        yy = by + art_h + 5
        verify_chip(d, x + col_w, yy, s["verify"])
        d.text((x, yy), s["tag"], font=font(SANS_B, 10), fill=s["color"])
        yy += 13
        yy = draw_wrapped(d, x, yy, s["head"], font(SERIF_B, 22), col_w,
                          leading=24, max_lines=2)
        yy += 2
        draw_wrapped(d, x, yy, s["deck"], font(SANS, 12), col_w, leading=14,
                     max_lines=2)
    d.line([M, 400, W - M, 400], fill=INK, width=1)

    # ---- grid of 12 cards (with illustration panel)
    gy = 408
    gw = (CW - 5 * 8) // 6
    gh = 137
    art_h2 = 46
    for idx, (num, tag, col, head, deck, ver, src, art) in enumerate(GRID):
        r, c = divmod(idx, 6)
        x = M + c * (gw + 8)
        y = gy + r * (gh + 8)
        MINI_ART[art](d, x, y, gw, art_h2)
        yy = y + art_h2 + 4
        verify_chip(d, x + gw, yy, ver)
        d.text((x, yy), f"{num} · {tag}", font=font(SANS_B, 10), fill=col)
        yy += 13
        yy = draw_wrapped(d, x, yy, head, font(SANS_B, 13), gw,
                          leading=14, max_lines=2)
        yy = draw_wrapped(d, x, yy + 1, deck, font(SANS, 10), gw, leading=12,
                          max_lines=3)
        if src:
            d.text((x, yy + 1), src, font=font(SERIF_I, 8), fill=GREY)
    grid_bottom = gy + 2 * gh + 8

    # ---- map + also on sunday
    ay = grid_bottom + 8
    d.text((M, ay), "WHERE IT HAPPENED", font=font(SANS_B, 13), fill=INK)
    d.text((M + 316, ay), "ALSO ON SUNDAY \u2014 24 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    d.line([M, ay + 18, M + 300, ay + 18], fill=INK, width=1)
    d.line([M + 316, ay + 18, W - M, ay + 18], fill=INK, width=1)

    map_x, map_y, map_w, map_h = M, ay + 24, 300, 168
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(232, 238, 242))
    step = 6
    for gy2 in range(map_y + 3, map_y + map_h - 2, step):
        lat = 75 - (gy2 - map_y) / map_h * 135
        for gx in range(map_x + 3, map_x + map_w - 2, step):
            lon = -180 + (gx - map_x) / map_w * 360
            if any(lo0 <= lon <= lo1 and la0 <= lat <= la1
                   for lo0, lo1, la0, la1 in LAND):
                d.ellipse([gx - 1, gy2 - 1, gx + 1, gy2 + 1], fill=(42, 74, 107))
    f_pin = font(SANS_B, 8)
    for lon, lat, n in PINS:
        px = map_x + (lon + 180) / 360 * map_w
        py = map_y + (75 - lat) / 135 * map_h
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        ns = str(n)
        d.text((px - d.textlength(ns, font=f_pin) / 2, py - 6), ns,
               font=f_pin, fill=(255, 255, 255))
    d.text((map_x, map_y + map_h + 4),
           "Red pins are numbered to match the stories above.",
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
        y = ay + 24 + row * 16
        d.text((x, y), f"{13 + i}.", font=f_num, fill=RED)
        num_w = d.textlength(f"{13 + i}. ", font=f_num)
        d.text((x + num_w, y), item, font=f_it, fill=INK)

    # ---- date check
    dy = ay + 24 + 12 * 16 + 6
    d.rectangle([M, dy, W - M, dy + 72], outline=RED, width=2)
    d.text((M + 10, dy + 5), "DATE CHECK", font=font(SANS_B, 13), fill=RED)
    draw_wrapped(d, M + 10, dy + 22, DATE_CHECK, font(SANS, 12), CW - 20,
                 leading=13, max_lines=4)

    # ---- footer: legend + items
    fy = dy + 72 + 6
    center(d, fy, LEGEND, font(SANS, 9), fill=GREY)
    center(d, fy + 12, "ALSO:  Brazil storm toll 5  \u00b7  Lahore AQI 538, world's worst  \u00b7  "
           "Shuri Castle restored, opens Monday  \u00b7  Markets: Taiwan \u221217.5% in a week, "
           "S&P in correction  \u00b7  THE WORLD IN ONE DAY  \u00b7  SUNDAY 22 NOVEMBER 2026",
           font(SANS, 10), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
