"""Vidéos verticales 1080x1920 : le coloriage se révèle tout seul, puis carte finale avec le livre."""
import sys, random
import numpy as np
from PIL import Image, ImageDraw
from promo_common import *
import engine

W, H, FPS = 1080, 1920, 30

def background(color, seed):
    bg = Image.new('RGB', (W, H), color); d = ImageDraw.Draw(bg); rng = random.Random(seed)
    for _ in range(160):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 6)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
    return bg

def card(img, w):
    h = int(img.height * w / img.width)
    c = Image.new('RGB', (w + 28, h + 28), 'white'); c.paste(img.resize((w, h), Image.LANCZOS), (14, 14))
    return c

def end_card(bg, cover, lines, accent):
    f = bg.copy(); m = mockup(cover, 880)
    f.paste(m, ((W - m.width) // 2, 220), m)
    d = ImageDraw.Draw(f)
    text_center(d, W, 100, lines[0], font(FONT_B, 62), 'white')
    text_center(d, W, 1230, lines[1], font(FONT_B, 54), accent)
    text_center(d, W, 1310, lines[2], font(FONT_I, 44), 'white')
    pill_w = 560; x0 = (W - pill_w) // 2
    d.rounded_rectangle((x0, 1410, x0 + pill_w, 1515), 52, fill=accent)
    text_center(d, W, 1432, lines[3], font(FONT_B, 50), (20, 20, 40))
    return f

def frame_with(bg, img_card, top, bottom, accent, y=360):
    f = bg.copy(); f.paste(img_card, ((W - img_card.width) // 2, y))
    d = ImageDraw.Draw(f)
    text_center(d, W, 110, top, font(FONT_B, 64), 'white', spacing=14)
    if bottom:
        text_center(d, W, y + img_card.height + 45, bottom, font(FONT_I, 52), accent)
    return f

def adult(out, b='01_chocolat'):
    NAVY, YEL = (26, 35, 126), (253, 216, 53)
    bg = background(NAVY, 3)
    sol, num, regions, e = mosaic_assets(b)
    rng = random.Random(4); rng.shuffle(regions); regions.sort(key=lambda r: r[0])
    cur = np.asarray(num).copy(); s = np.asarray(sol)
    cover = front_cover('Noel_cosy_adultes_couverture.pdf', 90, '/tmp/front_adult.png')
    def gen():
        c0 = card(num, 860)
        for i in range(60):
            yield frame_with(bg, c0, 'Un numéro =\nune couleur', 'Prêt(e) à colorier ?', YEL)
        n = len(regions); T = 300
        done = 0
        for t in range(T):
            target = int(n * ((t + 1) / T) ** 1.15)
            for c, m in regions[done:target]:
                cur[m] = s[m]
            done = target
            yield frame_with(bg, card(Image.fromarray(cur), 860), 'Zone après zone...', 'l\'image apparaît', YEL)
        full = card(sol, 860)
        for i in range(60):
            yield frame_with(bg, full, 'Et voilà !', 'Un chocolat chaud tout doux', YEL)
        ec = end_card(bg, cover, ['40 coloriages mystères', 'Coloriages mystères', 'Noël cosy · pour adultes', 'Lien en bio'], YEL)
        for i in range(120):
            yield ec
    write_video(gen(), out)

def adult_kids(out, b='04_bonhomme'):
    RED, YEL = (198, 40, 40), (253, 216, 53)
    bg = background(RED, 5)
    engine.COLS, engine.ROWS = 26, 28
    G = engine.grid(f'mosa/{b}.svg'); C, R = 26, 28; s = 36
    base = Image.new('RGB', (C * s, R * s), 'white'); d = ImageDraw.Draw(base); fnt = font(FONT_5, 17)
    cells = []
    for r in range(R):
        for c in range(C):
            x, y = c * s, r * s; n = G[r][c]
            if n:
                d.text((x + s / 2, y + s / 2), str(n), fill=(90, 90, 90), font=fnt, anchor='mm'); cells.append((r, c, n))
            d.rectangle((x, y, x + s, y + s), outline=(160, 160, 160))
    cur = base.copy(); dc = ImageDraw.Draw(cur)
    cells.sort(key=lambda t: (t[2], t[0], t[1]))
    cover = front_cover('Noel_magique_enfants_couverture.pdf', 90, '/tmp/front_kids.png')
    def gen():
        c0 = card(base, 860)
        for i in range(60):
            yield frame_with(bg, c0, 'Une case,\nun numéro...', 'Qu\'est-ce qui se cache ici ?', YEL)
        n = len(cells); T = 300; done = 0
        for t in range(T):
            target = int(n * (t + 1) / T)
            for r, c, k in cells[done:target]:
                x, y = c * s, r * s
                dc.rectangle((x, y, x + s, y + s), fill=PAL[k], outline=(160, 160, 160))
            done = target
            yield frame_with(bg, card(cur, 860), 'Case après case...', 'la surprise apparaît !', YEL)
        for i in range(60):
            yield frame_with(bg, card(cur, 860), 'Un bonhomme de neige !', 'Bravo !', YEL)
        ec = end_card(bg, cover, ['40 coloriages magiques', 'Coloriages magiques', 'de Noël · dès 6 ans', 'Lien en bio'], YEL)
        for i in range(120):
            yield ec
    write_video(gen(), out)

if __name__ == '__main__':
    import os; os.makedirs('promo', exist_ok=True)
    if 'adult' in sys.argv: adult('promo/Video_TikTok_Reels_Noel_cosy_adultes.mp4')
    if 'kids' in sys.argv: adult_kids('promo/Video_TikTok_Reels_Noel_magique_enfants.mp4')
