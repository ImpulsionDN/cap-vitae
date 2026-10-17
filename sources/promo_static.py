"""Carrousels Instagram (1080x1350) et épingles Pinterest (1000x1500) pour les 2 livrets."""
import random
import numpy as np
from PIL import Image, ImageDraw
from promo_common import *
import engine

def bg(W, H, color, seed):
    im = Image.new('RGB', (W, H), color); d = ImageDraw.Draw(im); rng = random.Random(seed)
    for _ in range(int(W * H / 9000)):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2, 5)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 255, 255))
    return im

def framed(img, w):
    h = int(img.height * w / img.width)
    c = Image.new('RGB', (w + 20, h + 20), 'white'); c.paste(img.convert('RGB').resize((w, h), Image.LANCZOS), (10, 10))
    return c

def split(left, right):
    w, h = left.size; o = left.copy().convert('RGB')
    o.paste(right.convert('RGB').resize((w, h)).crop((w // 2, 0, w, h)), (w // 2, 0))
    ImageDraw.Draw(o).line([(w // 2, 0), (w // 2, h)], fill='white', width=6)
    return o

def kids_pair(b):
    engine.COLS, engine.ROWS = 26, 28
    G = engine.grid(f'mosa/{b}.svg'); s = 34
    a = Image.new('RGB', (26 * s, 28 * s), 'white'); c = a.copy(); da, dc = ImageDraw.Draw(a), ImageDraw.Draw(c)
    f = font(FONT_5, 16)
    for r in range(28):
        for k in range(26):
            x, y = k * s, r * s; n = G[r][k]
            if n:
                da.text((x + s / 2, y + s / 2), str(n), fill=(90, 90, 90), font=f, anchor='mm')
                dc.rectangle((x, y, x + s, y + s), fill=PAL[n])
            da.rectangle((x, y, x + s, y + s), outline=(160, 160, 160)); dc.rectangle((x, y, x + s, y + s), outline=(160, 160, 160))
    return a, c

BOOKS = {
    'adultes': dict(color=(26, 35, 126), acc=(253, 216, 53), cover=('Noel_cosy_adultes_couverture.pdf', 90),
                    name='Coloriages mystères', sub='Noël cosy', who='pour adultes', hero='01_chocolat',
                    thumbs=['14_chalet', '05_renne', '33_fenetre_chat', '25_marche', '04_bonhomme', '06_chat_bonnet'],
                    hook='Le coloriage qui cache\nune surprise', how=['Chaque zone a un numéro', 'Chaque numéro = une couleur',
                    'L\'image de Noël apparaît'], tag='Anti-stress · Solutions incluses'),
    'enfants': dict(color=(198, 40, 40), acc=(253, 216, 53), cover=('Noel_magique_enfants_couverture.pdf', 90),
                    name='Coloriages magiques', sub='de Noël', who='dès 6 ans', hero='04_bonhomme',
                    thumbs=['16_pere_noel', '05_renne', '11_pingouin', '34_train', '12_ourson', '02_maison'],
                    hook='Une case, un numéro...\nune surprise !', how=['Je lis le numéro de la case', 'Je trouve sa couleur',
                    'Je découvre l\'image cachée'], tag='Grandes cases · Solutions incluses'),
}

def assets(key, B):
    if key == 'adultes':
        sol, num, _, _ = mosaic_assets(B['hero'])
        thumbs = [Image.open(f'cache/{b}_sol.png') for b in B['thumbs']]
        return num, sol, thumbs
    a, c = kids_pair(B['hero'])
    engine.COLS, engine.ROWS = 26, 28
    thumbs = []
    for b in B['thumbs']:
        engine.preview(engine.grid(f'mosa/{b}.svg'), f'cache/{b}_kid.png', 20); thumbs.append(Image.open(f'cache/{b}_kid.png'))
    return a, c, thumbs

def grid6(thumbs, cell, gap):
    o = Image.new('RGBA', (3 * cell + 2 * gap + 20, 2 * int(cell * 1.07) + gap + 20), (0, 0, 0, 0))
    for i, t in enumerate(thumbs):
        f = framed(t, cell); o.paste(f, ((i % 3) * (cell + gap), (i // 3) * (int(cell * 1.07) + gap)))
    return o

def make(key):
    B = BOOKS[key]; num, sol, thumbs = assets(key, B)
    cover = front_cover(*B['cover'], f'/tmp/front_{key}.png'); acc = B['acc']; out = []
    # ---------- Instagram 1080x1350 ----------
    W, H = 1080, 1350
    s1 = bg(W, H, B['color'], 1); d = ImageDraw.Draw(s1)
    text_center(d, W, 70, B['hook'], font(FONT_B, 62), 'white', spacing=12)
    f = framed(split(num, sol), 790); s1.paste(f, ((W - f.width) // 2, 290))
    text_center(d, W, 290 + f.height + 25, 'Avant  /  Après', font(FONT_I, 46), acc)
    text_center(d, W, H - 70, 'Glissez pour voir la suite  »', font(FONT_7, 34), 'white')
    s2 = bg(W, H, B['color'], 2); d = ImageDraw.Draw(s2)
    text_center(d, W, 80, 'Comment ça marche ?', font(FONT_B, 64), 'white')
    for i, t in enumerate(B['how']):
        y = 250 + i * 150
        d.ellipse((120, y, 220, y + 100), fill=acc); d.text((170, y + 50), str(i + 1), font=font(FONT_B, 54), fill=(20, 20, 40), anchor='mm')
        d.text((260, y + 50), t, font=font(FONT_7, 46), fill='white', anchor='lm')
    crop = num.crop((0, 0, num.width // 2, num.height // 2)) if key == 'adultes' else num.crop((0, num.height // 4, num.width // 2, num.height * 3 // 4))
    f = framed(crop, 500); s2.paste(f, ((W - f.width) // 2, 700))
    s3 = bg(W, H, B['color'], 3); d = ImageDraw.Draw(s3)
    text_center(d, W, 80, '40 dessins de Noël', font(FONT_B, 66), 'white')
    text_center(d, W, 180, 'un par page, verso blanc', font(FONT_I, 44), acc)
    g = grid6(thumbs, 300, 26); s3.paste(g, ((W - g.width) // 2 + 10, 320), g)
    text_center(d, W, H - 110, B['tag'], font(FONT_7, 38), 'white')
    s4 = bg(W, H, B['color'], 4); d = ImageDraw.Draw(s4)
    m = mockup(cover, 760); s4.paste(m, ((W - m.width) // 2, 40), m)
    text_center(d, W, 940, f"{B['name']} · {B['sub']}", font(FONT_B, 50), acc)
    text_center(d, W, 1015, f"40 coloriages {B['who']} · Grand format", font(FONT_I, 40), 'white')
    d.rounded_rectangle((W // 2 - 330, 1110, W // 2 + 330, 1215), 52, fill=acc)
    text_center(d, W, 1132, 'Sur Amazon · lien en bio', font(FONT_B, 46), (20, 20, 40))
    for i, s in enumerate([s1, s2, s3, s4], 1):
        p = f'promo/Instagram_{key}_{i}.png'; s.save(p); out.append(p)
    # ---------- Pinterest 1000x1500 ----------
    W, H = 1000, 1500
    p1 = bg(W, H, B['color'], 5); d = ImageDraw.Draw(p1)
    text_center(d, W, 60, f"{B['name']}\n{B['sub']}", font(FONT_B, 76), 'white', spacing=6)
    text_center(d, W, 265, f"40 coloriages par numéros {B['who']}", font(FONT_I, 42), acc)
    f = framed(split(num, sol), 700); p1.paste(f, ((W - f.width) // 2, 340))
    m = mockup(cover, 360); p1.paste(m, (W - m.width - 10, H - m.height - 10), m)
    d.text((60, H - 250), 'Avant / Après', font=font(FONT_I, 44), fill=acc)
    d.text((60, H - 180), 'Disponible', font=font(FONT_B, 50), fill='white')
    d.text((60, H - 120), 'sur Amazon', font=font(FONT_B, 50), fill='white')
    p2 = bg(W, H, B['color'], 6); d = ImageDraw.Draw(p2)
    text_center(d, W, 50, 'Idée cadeau de Noël', font(FONT_B, 66), 'white')
    text_center(d, W, 140, f"40 coloriages mystères {B['who']}" if key == 'adultes' else '40 coloriages magiques dès 6 ans', font(FONT_I, 42), acc)
    m = mockup(cover, 560); p2.paste(m, ((W - m.width) // 2, 205), m)
    g = grid6(thumbs, 240, 22); p2.paste(g, ((W - g.width) // 2 + 10, 855), g)
    text_center(d, W, H - 70, B['tag'] + ' · Sur Amazon', font(FONT_7, 30), 'white')
    for i, s in enumerate([p1, p2], 1):
        p = f'promo/Pinterest_{key}_{i}.png'; s.save(p); out.append(p)
    return out

if __name__ == '__main__':
    for k in BOOKS: print(make(k))
