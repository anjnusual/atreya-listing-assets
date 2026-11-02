"""Builds the Amazon/Flipkart gallery and A+ images for the Atreya Ganesha lotus bell latkan.
House style matches rosepins/: 1600x1600, warm beige, italic serif headline, maroon eyebrow."""
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC, OUT, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
LENGTH_TXT = "approx. 55 cm  |  22 inch"   # ESTIMATE from photos - confirm with a tape
WIDTH_TXT = "approx. 9 cm"

S = 1600
MAROON = (139, 46, 46); INK = (59, 36, 24); BODY = (88, 66, 52); GOLD = (176, 132, 60)
f = lambda name, size: ImageFont.truetype(os.path.join(FONTS, name), size)
def serif_i(sz):
    ft = f("PlayfairDisplay-Italic.ttf", sz)
    try: ft.set_variation_by_axes([500])
    except Exception: pass
    return ft
def serif(sz):
    ft = f("PlayfairDisplay.ttf", sz)
    try: ft.set_variation_by_axes([600])
    except Exception: pass
    return ft
sans = lambda sz: f("Poppins-Regular.ttf", sz)
sans_m = lambda sz: f("Poppins-Medium.ttf", sz)
sans_sb = lambda sz: f("Poppins-SemiBold.ttf", sz)

NAMES = {1: "pack4_white", 2: "pack4_closeup", 3: "pack4_real", 4: "pair_white", 5: "pair_door"}
def src(n): return Image.open(os.path.join(SRC, NAMES[n] + ".jpg")).convert("RGB")

def bg(w=S, h=S):
    top, bot = (248, 240, 231), (233, 214, 196)
    g = Image.new("RGB", (w, h))
    px = g.load()
    for y in range(h):
        for x in range(0, w):
            t = (x / w * 0.35 + y / h * 0.65)
            px[x, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    return g

_BG = None
def beige():
    global _BG
    if _BG is None: _BG = bg()
    return _BG.copy()

def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = word
    if cur: lines.append(cur)
    return lines

def para(d, xy, text, font, fill, maxw, lh=1.35):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill); y += int(font.size * lh)
    return y

def tracked(d, xy, text, font, fill, track=4):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + track

def white_knockout(im, thr=246):
    """Strip near-white to pure white (Amazon main image rule) and return a mask of the product."""
    g = im.convert("L")
    mask = g.point(lambda v: 0 if v >= thr else 255).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    white = Image.new("RGB", im.size, (255, 255, 255))
    return Image.composite(im, white, mask), mask

def on_white_square(im, fill=0.9):
    im, _ = white_knockout(im)
    sc = S * fill / max(im.size)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    c = Image.new("RGB", (S, S), (255, 255, 255))
    c.paste(im, ((S - im.width) // 2, (S - im.height) // 2))
    return c

def cutout(im, box=None):
    if box: im = im.crop(box)
    clean, mask = white_knockout(im)
    rgba = clean.convert("RGBA"); rgba.putalpha(mask)
    return rgba

def paste_scaled(canvas, rgba, xy, h=None, w=None):
    if h: sc = h / rgba.height
    else: sc = w / rgba.width
    r = rgba.resize((round(rgba.width * sc), round(rgba.height * sc)), Image.LANCZOS)
    # soft shadow
    sh = Image.new("RGBA", r.size, (60, 35, 20, 0))
    sh.putalpha(r.getchannel("A").point(lambda v: v * 0.22).filter(ImageFilter.GaussianBlur(14)))
    canvas.paste(sh, (xy[0] + 14, xy[1] + 18), sh)
    canvas.paste(r, xy, r)
    return sc, r.size

def save(im, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
    print("wrote", path, im.size)

STRAND_BOX = (320, 0, 560, 1254)   # left strand of the pair photo
# y positions of each part inside STRAND_BOX (source pixels)
PARTS = [
    (35, "Braided cord loop", "Hangs on a nail, hook or adhesive hook"),
    (185, "Yellow and pink flowers", "Soft fabric petals, top and bottom"),
    (335, "Gold-finish bells", "5 on every strand"),
    (455, "Lotus buds", "One above and one below Ganesha"),
    (612, "Painted Ganesha on MDF", "The centrepiece, facing outward"),
    (1150, "Pearl tassel", "With flower drops that sway when the door opens"),
]

def img_anatomy(out):
    c = beige(); d = ImageDraw.Draw(c)
    tracked(d, (110, 110), "WHAT IS ON EVERY STRAND", sans_sb(30), MAROON, 4)
    para(d, (110, 165), "Ganesha at the centre, a lotus on either side.", serif_i(70), INK, 1380, 1.2)
    st = cutout(src(4), STRAND_BOX)
    top, H = 330, 1210
    sc, (w, h) = paste_scaled(c, st, ((S - round(st.width * H / st.height)) // 2, top), h=H)
    cx = S // 2
    for i, (y, title, sub) in enumerate(PARTS):
        yy = top + int(y * sc)
        left = i % 2 == 0
        x_edge = cx - int(w * 0.42) if left else cx + int(w * 0.42)
        x_end = 600 if left else S - 600
        d.line((x_edge, yy, x_end, yy), fill=GOLD, width=3)
        d.ellipse((x_edge - 8, yy - 8, x_edge + 8, yy + 8), fill=GOLD)
        tf, sf = sans_sb(44), sans(32)
        if left:
            tx = x_end - 20 - max(d.textlength(title, font=tf), d.textlength(sub, font=sf))
            tx = max(70, tx)
        else:
            tx = x_end + 20
        d.text((tx, yy - 56), title, font=tf, fill=INK)
        para(d, (tx, yy + 4), sub, sf, BODY, 500 if not left else 520)
    save(c, out)

def img_closeup(out):
    im = src(2).resize((S, S), Image.LANCZOS).convert("RGBA")
    band = Image.new("RGBA", (S, 430), (248, 240, 231, 238))
    im.paste(band, (0, S - 430), band)
    d = ImageDraw.Draw(im)
    tracked(d, (110, S - 370), "THE CENTREPIECE", sans_sb(30), MAROON, 4)
    para(d, (110, S - 318), "Shri Ganesh at your doorstep.", serif_i(76), INK, 1380)
    para(d, (110, S - 205), "Painted on MDF wood and framed by lotus buds. Vighnaharta at the entrance, the way Indian homes have welcomed every festival for generations.", sans(32), BODY, 1380)
    save(im, out)

def img_size(out):
    c = beige(); d = ImageDraw.Draw(c)
    tracked(d, (110, 110), "SIZE OF ONE STRAND", sans_sb(30), MAROON, 4)
    para(d, (110, 165), "Long enough for a door frame, light enough for one nail.", serif_i(66), INK, 1380, 1.2)
    st = cutout(src(4), STRAND_BOX)
    top, H = 360, 1150
    sc, (w, h) = paste_scaled(c, st, (S // 2 - 120 - round(st.width * H / st.height) // 2, top), h=H)
    ax = S // 2 + 60
    d.line((ax, top, ax, top + h), fill=INK, width=4)
    for yy in (top, top + h): d.line((ax - 24, yy, ax + 24, yy), fill=INK, width=4)
    d.text((ax + 50, top + h // 2 - 70), "Length", font=sans_m(34), fill=BODY)
    d.text((ax + 50, top + h // 2 - 22), LENGTH_TXT, font=sans_sb(46), fill=INK)
    d.text((ax + 50, top + h // 2 + 70), "loop to tassel", font=sans(30), fill=BODY)
    gy = top + int(612 * sc)
    gx0 = S // 2 - 120 - int(w * 0.40); gx1 = S // 2 - 120 + int(w * 0.40)
    d.text((ax + 50, top + h // 2 + 170), "Width", font=sans_m(34), fill=BODY)
    d.text((ax + 50, top + h // 2 + 218), WIDTH_TXT, font=sans_sb(46), fill=INK)
    d.text((ax + 50, top + h // 2 + 310), "at the widest flowers", font=sans(30), fill=BODY)
    save(c, out)

def img_compare(out):
    c = beige(); d = ImageDraw.Draw(c)
    para(d, (110, 120), "A fresh flower toran lasts till morning.", serif_i(70), INK, 1380, 1.2)
    para(d, (110, 210), "This one comes back every festival.", serif_i(70), (120, 80, 60), 1380, 1.2)
    d.line((110, 330, 230, 330), fill=MAROON, width=3)
    cols = [("Fresh flower toran", ["Wilts by the next day", "Drops petals on the floor", "Bought again every festival", "Flowers only"]),
            ("This latkan", ["Same colour, year after year", "Nothing to sweep up", "Wipe, store flat, hang again", "Ganesha, lotus and bells in one"])]
    for i, (h, items) in enumerate(cols):
        x = 110 + i * 720
        d.text((x, 390), h, font=sans_sb(42), fill=MAROON if i else BODY)
        y = 470
        for it in items:
            d.ellipse((x, y + 20, x + 12, y + 32), fill=GOLD if i else BODY)
            y = para(d, (x + 32, y), it, sans(36), INK if i else BODY, 600) + 18
    pair = cutout(src(4))
    paste_scaled(c, pair, (S - 110 - 560, 880), w=560)
    para(d, (110, 1380), "Lasts for Diwali, Ganpati, Navratri and every Griha Pravesh in between.", serif_i(46), INK, 820)
    save(c, out)

def img_inbox(out, n):
    c = beige(); d = ImageDraw.Draw(c)
    tracked(d, (110, 110), "IN THE BOX", sans_sb(30), MAROON, 4)
    head = "2 latkans. One for each side of the door." if n == 2 else "4 latkans. The main door and the mandir, both sides."
    para(d, (110, 165), head, serif_i(66), INK, 1380, 1.2)
    im = cutout(src(4)) if n == 2 else cutout(src(1))
    H = 1150
    paste_scaled(c, im, ((S - round(im.width * H / im.height)) // 2, 370), h=H)
    d.text((110, 1530 - 10), f"Pack of {n}  |  Ready to hang  |  No assembly", font=sans_m(34), fill=BODY)
    save(c, out)

def img_uses(out):
    c = beige(); d = ImageDraw.Draw(c)
    tracked(d, (110, 110), "WHERE IT GOES", sans_sb(30), MAROON, 4)
    para(d, (110, 165), "Where you pray, and where your guests walk in.", serif_i(66), INK, 900, 1.2)
    uses = [("Main door", "Both sides of the frame, the way a toran is meant to frame it"),
            ("Pooja room and mandir", "Either side of the mandir or the idol"),
            ("Ganpati and Diwali", "Backdrop for Ganesh Chaturthi, Diwali and Lakshmi Puja"),
            ("Griha Pravesh and weddings", "Housewarming, mehndi and haldi corners")]
    y = 470
    for t, s in uses:
        d.text((110, y), t, font=sans_sb(42), fill=INK)
        y = para(d, (110, y + 62), s, sans(32), BODY, 760) + 60
    st = cutout(src(4), STRAND_BOX)
    H = 1260
    paste_scaled(c, st, (S - 160 - round(st.width * H / st.height), 220), h=H)
    save(c, out)

def img_real(out):
    c = beige(); d = ImageDraw.Draw(c)
    ph = src(3).resize((900, 1600), Image.LANCZOS)
    c.paste(ph, (S - 900, 0))
    tracked(d, (90, 520), "REAL PHOTO", sans_sb(30), MAROON, 4)
    para(d, (90, 575), "Photographed at home. Not a render.", serif_i(64), INK, 560, 1.2)
    para(d, (90, 850), "The Pack of 4, held up before packing. Colours and bells are exactly what you receive.", sans(32), BODY, 540)
    save(c, out)

def img_lifestyle(out):
    save(src(5).resize((S, S), Image.LANCZOS), out)

# ---------- A+ ----------
def aplus(outdir):
    # Standard Image Header with Text: 970 x 600
    W, H = 970 * 2, 600 * 2
    c = bg(W, H); d = ImageDraw.Draw(c)
    life = src(5)
    crop = life.crop((40, 0, 40 + 760, 1254)).resize((round(760 * H / 1254), H), Image.LANCZOS)
    c.paste(crop, (W - crop.width, 0))
    tracked(d, (110, 330), "ATREYA", sans_sb(40), MAROON, 10)
    para(d, (110, 400), "Shubh aarambh, at every doorway.", serif_i(96), INK, 900, 1.15)
    para(d, (110, 660), "Ganesha lotus latkan with gold bells and a pearl tassel. Ready to hang for Diwali, Ganpati and every Griha Pravesh.", sans(38), BODY, 860)
    save(c, f"{outdir}/aplus_1_header_970x600.jpg")
    # Three images and text: 300 x 300 each (made at 600)
    tiles = [(src(2), (440, 470, 1040, 1070), "aplus_2a_ganesha"),
             (src(2), (230, 60, 700, 530), "aplus_2b_lotus"),
             (src(4), (290, 860, 610, 1180), "aplus_2c_bells_pearls")]
    for im, box, name in tiles:
        t = im.crop(box).resize((600, 600), Image.LANCZOS)
        if name.endswith("pearls"):
            t = Image.composite(t, Image.new("RGB", t.size, (248, 240, 231)), white_knockout(t)[1])
        save(t, f"{outdir}/{name}_300x300.jpg")
    # Single image and highlights: 300 x 300
    p = Image.new("RGB", (600, 600), (248, 240, 231))
    pair = cutout(src(4)); sc = 560 / pair.height
    pr = pair.resize((round(pair.width * sc), 560), Image.LANCZOS)
    p.paste(pr, ((600 - pr.width) // 2, 20), pr)
    save(p, f"{outdir}/aplus_3_pair_300x300.jpg")

if __name__ == "__main__":
    for n in (2, 4):
        d = f"{OUT}/ATR-GANESH-LOTUSBELL-LATKAN-{n}"
        save(on_white_square(src(4) if n == 2 else src(1)), f"{d}/main.jpg")
        img_lifestyle(f"{d}/other1.jpg")
        img_anatomy(f"{d}/other2.jpg")
        img_closeup(f"{d}/other3.jpg")
        img_size(f"{d}/other4.jpg")
        img_inbox(f"{d}/other5.jpg", n)
        img_compare(f"{d}/other6.jpg")
        img_uses(f"{d}/other7.jpg")
        if n == 4: img_real(f"{d}/other8.jpg")
    aplus(f"{OUT}/aplus")
