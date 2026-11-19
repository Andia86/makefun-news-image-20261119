#!/usr/bin/env python3
"""Compose the entry image for make.fun news-image-20261119.

Builds a 1024x1024 broadsheet front page for Thursday 19 November 2026:
masthead with a huge serif date, 11 numbered story cards (a wide hero
card for the Shenzhen trilateral summit, the rest with small flat
illustrations drawn in code), a world map with numbered pins for the
card stories AND the briefs, a dense two-column numbered brief list
for the remaining stories, and a sourcing footer. All type is drawn
with PIL so every word is spelled exactly as written here; the map
artwork in art/map.png is a text-free vintage atlas plate, and every
pin position was checked against the artwork's own coastlines
(land/sea sampling plus zoomed crops) before being placed.

Run:  python3 build_page.py   ->  writes entry.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
CREAM = (246, 239, 221)
CARD = (255, 253, 246)
INK = (26, 23, 18)
NAVY = (22, 53, 94)
RED = (179, 32, 42)
GREY = (92, 84, 70)
SKY = (250, 246, 231)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def centered(draw, cx, y, s, f, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def tracked(draw, cx, y, s, f, fill, tracking=6):
    """Draw letterspaced text centred on cx."""
    widths = [text_w(draw, ch, f) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += w + tracking
    return total


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- content
# 11 card stories: (tag, headline, one-line summary, pin, icon).
# Pin = (fx, fy) of the pin circle in the full 2240x1120 map image, or
# ((fx, fy), (ax, ay)) when the circle is offset with a leader line to
# the true anchor point (used where two stories share one city or a
# coast is too crowded for two full circles).
CARDS = [
    ("CHINA · APEC SUMMIT", "Trump, Xi and Putin meet in Shenzhen",
     "Xi hosts the first US-China-Russia summit: nuclear arms, the wars "
     "in Ukraine and Iran, and trade on the table.",
     (0.556, 0.462), "hero"),
    ("CRIMEA · WAR", "Ukraine hits Crimea bridge a third time",
     "Third strike in a week hits the rail link and halts traffic.",
     (0.356, 0.315), "bridge"),
    ("HORMUZ · WAR", "Tankers burn after hitting mines",
     "Iran: three tankers afire east of Hormuz; one hit off Khasab.",
     (0.458, 0.460), "ship"),
    ("KUWAIT · WAR", "Iran fires drones at a US base in Kuwait",
     "AP: Kuwait and Bahrain down drones; Tehran vows crushing reply.",
     ((0.434, 0.426), (0.443, 0.440)), "jet"),
    ("NEW YORK · MARKETS", "Anthropic's $81bn IPO is the biggest ever",
     "Reuters: priced at $83; trades as ANT, valued near $1.5 trillion.",
     (0.968, 0.315), "chart_up"),
    ("THE HAGUE · JUSTICE", "World Court rules on Rohingya genocide",
     "Judgment day in The Gambia's Rohingya case against Myanmar.",
     (0.286, 0.280), "scales"),
    ("GAZA · WAR", "Israel launches Gaza ground operation",
     "Israeli troops enter central Gaza - first such move since "
     "the ceasefire.",
     ((0.320, 0.392), (0.343, 0.368)), "arrow"),
    ("NEW ZEALAND · GAMING", "GTA VI launches to a 99",
     "Out from New Zealand; its 99 ties Ocarina of Time's all-time record.",
     (0.726, 0.860), "gamepad"),
    ("WASHINGTON · POLITICS", "Peltola seals Senate majority",
     "Alaska win gives Democrats 56 seats; Jeffries first Black "
     "Speaker.",
     ((0.938, 0.352), (0.955, 0.335)), "ballot"),
    ("INDIA · STORM", "Cyclone Akvan bears down on Andhra",
     "540 km of coast braces for Friday landfall; gusts to 145 km/h.",
     (0.475, 0.505), "cyclone"),
    ("WORLD · CHILDREN", "1 in 4 children in war zones",
     "A record share of the world's children, Save the Children counts.",
     (0.246, 0.276), "shield"),
]

# Stories 12-44: (place, short text, pin). One line each in the brief
# list; pin is None for the two stories that have no place on land
# (marked with a star / diamond in the list and explained in the
# map caption).
BRIEFS = [
    ("ETHIOPIA", "Eritrea clashes threaten war",
     (0.385, 0.520)),
    ("KUMAMOTO", "M5.7 quake, no tsunami",
     (0.610, 0.407)),
    ("HONDURAS", "Four attacks in Yoro kill 12",
     (0.913, 0.446)),
    ("FLORIDA", "Floods fell synagogue roof",
     (0.958, 0.432)),
    ("KASHMIR", "Police kill a rebel leader",
     (0.455, 0.360)),
    ("ILLINOIS", "Indicted in foiled temple plot",
     ((0.912, 0.296), (0.925, 0.312))),
    ("PARIS", "France jails 3 women over ISIS",
     (0.250, 0.324)),
    ("WASHINGTON", "Pew: Islam #1 by 2035",
     ((0.978, 0.372), (0.955, 0.335))),
    ("CHRISTMAS I.", "Red crabs march to sea",
     (0.548, 0.665)),
    ("SYDNEY", "Jobless rate climbs to 4.9%",
     (0.660, 0.812)),
    ("HONG KONG", "Gold 1-year low; HS -2.8%",
     ((0.534, 0.494), (0.552, 0.466))),
    ("LONDON", "Bills to rise 26% in January",
     ((0.264, 0.234), (0.246, 0.276))),
    ("SEOUL", "Exam under anti-cheat curbs",
     (0.594, 0.346)),
    ("TOKYO", "Takaichi's muted welcome noted",
     (0.634, 0.342)),
    ("RIYADH", "Yemen campaign into 2027",
     (0.406, 0.464)),
    ("MYANMAR", "Ruler questions ASEAN ties",
     (0.505, 0.442)),
    ("CARACAS", "Hegseth inks defence pact",
     (0.130, 0.556)),
    ("WELLINGTON", "Nicholls ton: NZ 236/5",
     ((0.756, 0.836), (0.726, 0.860))),
    ("TURIN", "Alcaraz into ATP Finals last 4",
     (0.283, 0.335)),
    ("DAKAR", "Ambure wins hurdles bronze",
     (0.224, 0.464)),
    ("MUMBAI", "Dhoni retires from the IPL",
     ((0.434, 0.502), (0.452, 0.486))),
    ("FALKLANDS", "Falklands beat Costa Rica",
     (0.105, 0.885)),
    ("DENVER", "Nuggets edge Celtics 105-101",
     (0.885, 0.345)),
    ("SAO PAULO", "Bovespa -1.3%: debt fears",
     (0.152, 0.698)),
    ("KATHMANDU", "Nepal league Qualifier 2",
     (0.470, 0.398)),
    ("DHAKA", "Rabada stretches SA's Test lead",
     ((0.498, 0.440), (0.488, 0.424))),
    ("DETROIT", "Cadillac keeps Bottas for 2027",
     ((0.946, 0.276), (0.943, 0.300))),
    ("UKRAINE", "'Vivaldi' melds drones, troops",
     (0.330, 0.278)),
    ("NEW YORK", "Van Gogh record: $190.4m",
     ((0.988, 0.266), (0.968, 0.315))),
    ("SANTA CLARA", "Nvidia turmoil hits chips",
     ((0.852, 0.330), (0.872, 0.342))),
    ("CANBERRA", "Spending record: A$82.6bn",
     (0.640, 0.795)),
    ("DEEP SPACE *", "Signals take 24 hours",
     None),
    ("WORLDWIDE +", "Java flaw: systems open",
     None),
]

N_STORIES = len(CARDS) + len(BRIEFS)  # 44

# ---------------------------------------------------------------- icons
# Small flat illustrations drawn in code in the page palette. Each
# takes a draw context and a centre.


def icon_bridge(d, cx, cy):
    for px in (cx - 20, cx + 24):   # pylons
        d.rectangle([px - 2, cy - 16, px + 2, cy + 8], fill=NAVY)
    d.line([cx - 36, cy - 4, cx - 2, cy - 4], fill=NAVY, width=3)
    d.line([cx + 14, cy - 4, cx + 36, cy - 4], fill=NAVY, width=3)
    d.polygon([(cx - 2, cy - 4), (cx + 13, cy - 4), (cx + 9, cy + 5)], fill=RED)
    d.arc([cx - 20, cy - 26, cx + 24, cy - 2], 0, 180, fill=GREY, width=1)
    for wx in (cx - 28, cx - 6, cx + 16):   # waves
        d.arc([wx, cy + 9, wx + 14, cy + 17], 180, 360, fill=NAVY, width=2)


def icon_ship(d, cx, cy):
    # tanker hull, deck and superstructure; flame and smoke astern
    d.polygon([(cx - 34, cy + 4), (cx + 30, cy + 4), (cx + 22, cy + 14),
               (cx - 26, cy + 14)], fill=NAVY)
    d.rectangle([cx - 30, cy - 2, cx + 18, cy + 4], fill=NAVY)
    d.rectangle([cx + 20, cy - 12, cx + 30, cy + 4], fill=NAVY)
    d.rectangle([cx - 22, cy - 8, cx - 12, cy - 2], fill=RED)
    d.rectangle([cx - 6, cy - 8, cx + 4, cy - 2], fill=RED)
    fx, fy = cx - 38, cy - 2
    d.polygon([(fx, fy), (fx - 6, fy - 10), (fx - 1, fy - 6),
               (fx + 2, fy - 13), (fx + 5, fy - 5), (fx + 7, fy - 9),
               (fx + 8, fy)], fill=RED)
    for wx in (cx - 30, cx - 8, cx + 14):   # waves
        d.arc([wx, cy + 15, wx + 14, cy + 22], 180, 360, fill=NAVY, width=2)


def icon_jet(d, cx, cy):
    d.polygon([(cx - 30, cy - 2), (cx + 8, cy - 14), (cx + 28, cy - 16),
               (cx + 14, cy - 6), (cx + 24, cy + 2), (cx + 2, cy - 1),
               (cx - 6, cy + 6), (cx - 14, cy - 2)], fill=NAVY)
    d.line([cx - 36, cy - 10, cx - 26, cy - 8], fill=GREY, width=2)
    d.line([cx - 36, cy + 2, cx - 27, cy + 1], fill=GREY, width=2)
    d.line([cx - 30, cy + 14, cx + 34, cy + 14], fill=NAVY, width=2)
    bx, by = cx + 18, cy + 12
    for dx, dy in ((-8, -3), (-5, -7), (0, -9), (5, -7), (8, -3), (-7, 2), (7, 2)):
        d.line([bx, by, bx + dx, by + dy], fill=RED, width=3)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=RED)


def icon_chart_up(d, cx, cy):
    d.line([cx - 30, cy - 16, cx - 30, cy + 16], fill=GREY, width=2)
    d.line([cx - 30, cy + 16, cx + 32, cy + 16], fill=GREY, width=2)
    pts = [(cx - 26, cy + 11), (cx - 12, cy + 3), (cx - 3, cy + 8),
           (cx + 10, cy - 4), (cx + 24, cy - 13)]
    d.line(pts, fill=RED, width=3)
    d.polygon([(cx + 24, cy - 13), (cx + 15, cy - 13), (cx + 23, cy - 5)], fill=RED)
    d.text((cx + 16, cy + 2), "$", font=font(SANS_B, 15), fill=NAVY)


def icon_scales(d, cx, cy):
    d.line([cx, cy - 20, cx, cy + 12], fill=NAVY, width=3)
    d.line([cx - 26, cy - 15, cx + 26, cy - 15], fill=NAVY, width=3)
    d.ellipse([cx - 3, cy - 23, cx + 3, cy - 17], fill=RED)
    for sx in (cx - 26, cx + 26):
        d.line([sx, cy - 15, sx - 7, cy - 2], fill=NAVY, width=2)
        d.line([sx, cy - 15, sx + 7, cy - 2], fill=NAVY, width=2)
        d.arc([sx - 10, cy - 6, sx + 10, cy + 6], 0, 180, fill=NAVY, width=3)
    d.line([cx - 12, cy + 16, cx + 12, cy + 16], fill=NAVY, width=3)


def icon_arrow(d, cx, cy):
    # a bold advance arrow crossing a line on the ground
    d.polygon([(cx - 32, cy - 6), (cx + 8, cy - 6), (cx + 8, cy - 14),
               (cx + 30, cy), (cx + 8, cy + 14), (cx + 8, cy + 6),
               (cx - 32, cy + 6)], fill=RED)
    d.line([cx + 14, cy - 20, cx + 14, cy + 18], fill=NAVY, width=3)
    d.line([cx - 36, cy + 18, cx + 36, cy + 18], fill=NAVY, width=2)
    for dx, dy in ((-24, -16), (-8, -19), (24, 16)):
        d.line([cx + dx - 3, cy + dy, cx + dx + 3, cy + dy], fill=GREY, width=2)


def icon_gamepad(d, cx, cy):
    d.rounded_rectangle([cx - 32, cy - 14, cx + 32, cy + 14], radius=12,
                        fill=NAVY)
    d.line([cx - 20, cy - 5, cx - 20, cy + 5], fill=(252, 252, 248), width=3)
    d.line([cx - 25, cy, cx - 15, cy], fill=(252, 252, 248), width=3)
    d.ellipse([cx + 12, cy - 8, cx + 18, cy - 2], fill=RED)
    d.ellipse([cx + 20, cy + 1, cx + 26, cy + 7], fill=(240, 200, 80))


def icon_ballot(d, cx, cy):
    d.rectangle([cx - 11, cy - 18, cx + 11, cy + 3], fill=(252, 252, 248), outline=NAVY, width=2)
    d.line([cx - 6, cy - 8, cx - 1, cy - 3], fill=RED, width=3)
    d.line([cx - 1, cy - 3, cx + 7, cy - 13], fill=RED, width=3)
    d.rectangle([cx - 24, cy + 3, cx + 24, cy + 18], outline=NAVY, width=3)
    d.line([cx - 13, cy + 7, cx + 13, cy + 7], fill=NAVY, width=3)


def icon_cyclone(d, cx, cy):
    for r, a0, a1 in ((19, 195, 330), (19, 15, 150), (13, 150, 300),
                      (13, 330, 105), (7, 110, 300)):
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=NAVY, width=5)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


def icon_shield(d, cx, cy):
    d.polygon([(cx, cy - 20), (cx + 16, cy - 14), (cx + 16, cy + 2),
               (cx, cy + 20), (cx - 16, cy + 2), (cx - 16, cy - 14)],
              outline=NAVY, width=3)
    d.ellipse([cx - 4, cy - 10, cx + 4, cy - 2], fill=RED)   # head
    d.arc([cx - 8, cy - 4, cx + 8, cy + 14], 180, 360, fill=RED, width=3)  # shoulders


ICONS = {
    "bridge": icon_bridge, "ship": icon_ship, "jet": icon_jet,
    "chart_up": icon_chart_up, "scales": icon_scales, "arrow": icon_arrow,
    "gamepad": icon_gamepad, "ballot": icon_ballot,
    "cyclone": icon_cyclone, "shield": icon_shield,
}


def hero_art(d, x, y, w, h):
    """Shenzhen skyline panel for the hero card: towers, a convention
    hall with flags, a red sun, and the harbour along the bottom.
    Everything is drawn inside the panel's w x h box."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 42, y + 12, x + w - 16, y + 38], fill=RED)
    base = y + h - 26
    towers = [(4, 56), (25, 82), (47, 64), (68, 94), (90, 70)]
    for tx, th in towers:
        d.rectangle([x + tx, base - th, x + tx + 17, base], fill=NAVY)
        for wy in range(base - th + 7, base - 7, 11):
            for wx in (x + tx + 4, x + tx + 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(252, 246, 230))
    hx0, hx1 = x + 112, x + 182
    d.rectangle([hx0, base - 24, hx1, base], fill=NAVY)
    d.pieslice([hx0 - 5, base - 40, hx1 + 5, base - 8], 180, 360, fill=RED)
    d.rectangle([hx0 - 5, base - 25, hx1 + 5, base - 22], fill=RED)
    for fx in (hx0 + 12, hx0 + 35, hx0 + 58):   # three small flags
        d.line([fx, base - 40, fx, base - 27], fill=NAVY, width=2)
        d.rectangle([fx, base - 40, fx + 7, base - 35], fill=RED)
    d.rectangle([x, base, x + w, y + h], fill=NAVY)
    for wx in range(x + 10, x + w - 24, 46):
        d.arc([wx, base + 8, wx + 22, base + 16], 180, 360, fill=(252, 246, 230), width=2)


# ---------------------------------------------------------------- layout
W = 1024
MARGIN = 28
RIGHT = W - MARGIN


def card_frame(draw, x, y, w, h, num, tag):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=NAVY, width=1)
    r = 11
    cx, cy = x + 17, y + 17
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    nf = font(SANS_B, 14)
    n = str(num)
    draw.text((cx - text_w(draw, n, nf) / 2, cy - 8), n, font=nf, fill=(255, 255, 255))
    draw.text((x + 36, y + 9), tag, font=font(SANS_B, 11), fill=GREY)


def draw_card(draw, x, y, w, h, num, tag, headline, dek, icon):
    card_frame(draw, x, y, w, h, num, tag)
    ICONS[icon](draw, x + w // 2, y + 48)
    hf = font(SERIF_B, 14)
    if len(wrap(draw, headline.upper(), hf, w - 20)) > 2:
        print("CARD HEADLINE OVERFLOW", num, headline)
    if len(wrap(draw, dek, font(SANS, 12), w - 20)) > 2:
        print("CARD DEK OVERFLOW", num, dek)
    lines = wrap(draw, headline.upper(), hf, w - 20)[:2]
    ly = y + 74
    for ln in lines:
        draw.text((x + 10, ly), ln, font=hf, fill=INK)
        ly += 17
    df = font(SANS, 12)
    for ln in wrap(draw, dek, df, w - 20)[:2]:
        draw.text((x + 10, ly + 3), ln, font=df, fill=(60, 54, 44))
        ly += 14


def draw_hero(draw, x, y, w, h, num, tag, headline, dek):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=NAVY, width=1)
    hero_art(draw, x + 1, y + 1, 188, h - 2)
    tx = x + 202
    r = 11
    cx, cy = tx + 6, y + 17
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    nf = font(SANS_B, 14)
    n = str(num)
    draw.text((cx - text_w(draw, n, nf) / 2, cy - 8), n, font=nf, fill=(255, 255, 255))
    draw.text((tx + 25, y + 9), tag, font=font(SANS_B, 11), fill=GREY)
    hf = font(SERIF_B, 19)
    ly = y + 40
    for ln in wrap(draw, headline.upper(), hf, w - 214)[:2]:
        draw.text((tx, ly), ln, font=hf, fill=INK)
        ly += 23
    df = font(SANS, 12)
    for ln in wrap(draw, dek, df, w - 214)[:3]:
        draw.text((tx, ly + 4), ln, font=df, fill=(60, 54, 44))
        ly += 15


def split_pin(pin):
    """Return (circle_frac, anchor_frac); anchor == circle if direct."""
    if pin is None:
        return None, None
    if isinstance(pin[0], tuple):
        return pin[0], pin[1]
    return pin, pin


def main():
    page = Image.new("RGB", (W, W), CREAM)
    draw = ImageDraw.Draw(page)
    cx = W // 2

    # ---- masthead
    tracked(draw, cx, 12, "THE DAY IN WORLD NEWS", font(SANS_B, 16), NAVY, 8)
    centered(draw, cx, 36, "THURSDAY 19 NOVEMBER 2026", font(SERIF_B, 44), INK)
    draw.rectangle([MARGIN, 96, RIGHT, 99], fill=RED)
    centered(draw, cx, 106, f"{N_STORIES} STORIES · 6 CONTINENTS · ONE PAGE",
             font(SANS_B, 19), RED)
    draw.rectangle([MARGIN, 134, RIGHT, 135], fill=NAVY)

    # ---- story cards: hero + 2, then rows of 4 / 4
    grid_y = 146
    row_h, gap = 146, 8
    tag, head, dek, _pin, _icon = CARDS[0]
    draw_hero(draw, MARGIN, grid_y, 480, row_h, 1, tag, head, dek)
    for j, i in enumerate((1, 2)):
        tag, head, dek, _pin, icon = CARDS[i]
        draw_card(draw, MARGIN + 480 + gap + j * (236 + gap), grid_y,
                  236, row_h, i + 1, tag, head, dek, icon)
    for r_i, (a, b) in enumerate(((3, 7), (7, 11))):
        y = grid_y + (r_i + 1) * (row_h + gap)
        for i in range(a, b):
            tag, head, dek, _pin, icon = CARDS[i]
            draw_card(draw, MARGIN + (i - a) * (236 + gap), y, 236, row_h,
                      i + 1, tag, head, dek, icon)

    # ---- bottom band: map (left) + brief list (right, two columns)
    band_y = grid_y + 3 * row_h + 2 * gap + 12  # 612
    draw.text((MARGIN, band_y), "WHERE IT HAPPENED - EVERY STORY PINNED",
              font=font(SANS_B, 13), fill=NAVY)
    draw.text((468, band_y), f"IN BRIEF - STORIES 12-{N_STORIES}",
              font=font(SANS_B, 13), fill=NAVY)

    art = Image.open("art/map.png").convert("RGB")
    crop = art.crop((0, 30, 2240, 1010))            # 2240 x 980
    map_w = 420
    map_h = round(map_w * crop.height / crop.width)  # 184
    map_x, map_y = MARGIN, band_y + 22
    page.paste(crop.resize((map_w, map_h)), (map_x, map_y))
    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=NAVY, width=1)

    def pin_xy(frac):
        fx, fy = frac
        return (map_x + fx * map_w,
                map_y + (fy * 1120 - 30) / 980 * map_h)

    all_pins = [c[3] for c in CARDS] + [b[2] for b in BRIEFS]

    # leader lines first, under the pins
    for pin in all_pins:
        circ, anch = split_pin(pin)
        if circ is not None and anch != circ:
            (cxp, cyp), (axp, ayp) = pin_xy(circ), pin_xy(anch)
            draw.line([axp, ayp, cxp, cyp], fill=NAVY, width=1)

    # card pins: bigger circles; brief pins: smaller
    for i, pin in enumerate(all_pins):
        circ, _anch = split_pin(pin)
        if circ is None:
            continue
        px, py = pin_xy(circ)
        if i < len(CARDS):
            r, pf = 7, font(SANS_B, 9)
        else:
            r, pf = 6, font(SANS_B, 8)
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        s = str(i + 1)
        draw.text((px - text_w(draw, s, pf) / 2, py - (5 if i < len(CARDS) else 4)),
                  s, font=pf, fill=(255, 255, 255))

    cap = ("Pins 1-44 mark where each story happened. Two have no place "
           "on land: * Voyager 1, a full light-day (25.9bn km) from Earth, "
           "and + a flaw in the Java platform, which governments warn "
           "leaves systems everywhere open to hackers.")
    cf = font(SANS, 12)
    ly = map_y + map_h + 8
    for ln in wrap(draw, cap, cf, map_w):
        draw.text((map_x, ly), ln, font=cf, fill=(60, 54, 44))
        ly += 15

    # brief list: two columns, one line per story
    bf = font(SANS, 11)
    bfb = font(SANS_B, 11)
    col_x = (468, 738)
    col_w = RIGHT - col_x[1]
    half = (len(BRIEFS) + 1) // 2
    warn = []
    for i, (place, txt, _pin) in enumerate(BRIEFS):
        col = 0 if i < half else 1
        row = i if col == 0 else i - half
        x = col_x[col]
        y = band_y + 26 + row * 15
        num = str(len(CARDS) + i + 1)
        draw.text((x, y), num, font=bfb, fill=RED)
        draw.text((x + 20, y), place + " - ", font=bfb, fill=INK)
        off = x + 20 + text_w(draw, place + " - ", bfb)
        line = txt
        while text_w(draw, line, bf) > x + col_w - off and line:
            line = line[:-1]
        if line != txt:
            warn.append((num, txt, line))
        draw.text((off, y), line, font=bf, fill=(60, 54, 44))
    for w_ in warn:
        print("TRUNCATED brief", w_)

    # ---- one-line summary strip
    sy = 918
    draw.rectangle([MARGIN, sy, RIGHT, sy + 30], outline=NAVY, width=1)
    sf = font(SERIF, 12)
    s = ("THE DAY IN ONE LINE:  three presidents at one table, two wars "
         "widening, a record IPO, a record Van Gogh, and GTA VI's 99.")
    centered(draw, cx, sy + 8, s, sf, INK)

    # ---- footer
    fy = 962
    draw.rectangle([MARGIN, fy, RIGHT, fy + 1], fill=NAVY)
    ff = font(SANS, 11)
    draw.text((MARGIN, fy + 8),
              "Every story was reported on Thursday 19 November 2026; disputed claims are attributed.",
              font=ff, fill=GREY)
    draw.text((MARGIN, fy + 26),
              "Sources: Reuters, AP, AFP, BBC, Al Jazeera, The Hindu, Japan Times, NDTV, "
              "The National, Save the Children. Tomorrow: Cyclone Akvan makes landfall in India.",
              font=ff, fill=GREY)
    draw.text((MARGIN, fy + 44),
              f"Date check: all {N_STORIES} stories are dated Thursday 19 November 2026, "
              "checked against the Reuters, AP and AFP wires.",
              font=ff, fill=NAVY)

    page.save("entry.png", optimize=True)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
