"""Série d'épingles Pinterest 1000x1500 pour les 2 livres de coloriage."""
import os
from PIL import Image, ImageDraw
from promo_common import *
from promo_static import bg, framed, split, kids_pair, mockup
import engine

W, H = 1000, 1500
OUT = 'pins'; os.makedirs(OUT, exist_ok=True)
NAVY, RED, YEL, CREAM = (26, 35, 126), (198, 40, 40), (253, 216, 53), (246, 240, 230)
COV_A = front_cover('Noel_cosy_adultes_couverture.pdf', 90, '/tmp/front_adultes.png')
COV_K = front_cover('Noel_magique_enfants_couverture.pdf', 90, '/tmp/front_enfants.png')

def save(im, name):
    im.convert('RGB').save(f'{OUT}/{name}.jpg', quality=90); return name

def corner_book(im, cover, h=340):
    m = mockup(cover, h); im.paste(m, (W - m.width - 5, H - m.height - 5), m)

def footer(d, txt, color='white', y=H - 230):
    d.text((50, y), txt[0], font=font(FONT_I, 40), fill=YEL)
    d.text((50, y + 60), txt[1], font=font(FONT_B, 46), fill=color)
    d.text((50, y + 118), txt[2], font=font(FONT_B, 46), fill=color)

def thumbs_adult(names):
    return [Image.open(f'cache/{b}_sol.png') for b in names]

def thumbs_kids(names):
    engine.COLS, engine.ROWS = 26, 28; out = []
    for b in names:
        engine.preview(engine.grid(f'mosa/{b}.svg'), f'cache/{b}_kid.png', 20); out.append(Image.open(f'cache/{b}_kid.png'))
    return out

def grid(im, thumbs, cols, cell, x0, y0, gap=14, ratio=1.07):
    for i, t in enumerate(thumbs):
        f = framed(t, cell); im.paste(f, (x0 + (i % cols) * (cell + gap), y0 + (i // cols) * (int(cell * ratio) + gap)))

def pin_split(key, b, title, sub, name):
    color, cov = (NAVY, COV_A) if key == 'a' else (RED, COV_K)
    if key == 'a':
        sol, num, _, _ = mosaic_assets(b); l, r = num, sol
    else:
        l, r = kids_pair(b)
    im = bg(W, H, color, hash(name) % 100); d = ImageDraw.Draw(im)
    text_center(d, W, 55, title, font(FONT_B, 70), 'white', spacing=6)
    text_center(d, W, 55 + 85 * (title.count('\n') + 1) + 10, sub, font(FONT_I, 42), YEL)
    f = framed(split(l, r), 700); y = 330 if title.count('\n') else 250
    im.paste(f, ((W - f.width) // 2, y))
    corner_book(im, cov, 330)
    footer(d, ['Avant / Après', 'Disponible', 'sur Amazon'])
    return save(im, name)

def pin_grid(key, names, title, sub, name, cols=3, cell=250):
    color, cov = (NAVY, COV_A) if key == 'a' else (RED, COV_K)
    th = thumbs_adult(names) if key == 'a' else thumbs_kids(names)
    im = bg(W, H, color, hash(name) % 100); d = ImageDraw.Draw(im)
    text_center(d, W, 50, title, font(FONT_B, 66), 'white', spacing=6)
    ty = 50 + 80 * (title.count('\n') + 1) + 5
    text_center(d, W, ty, sub, font(FONT_I, 40), YEL)
    gw = cols * cell + (cols - 1) * 14 + 20
    grid(im, th, cols, cell, (W - gw) // 2, ty + 80)
    corner_book(im, cov, 330)
    footer(d, ['40 dessins dans le livre', 'Disponible', 'sur Amazon'])
    return save(im, name)

def pin_book(key, title, sub, bullets, name):
    color, cov = (NAVY, COV_A) if key == 'a' else (RED, COV_K)
    im = bg(W, H, color, hash(name) % 100); d = ImageDraw.Draw(im)
    text_center(d, W, 50, title, font(FONT_B, 66), 'white', spacing=6)
    text_center(d, W, 50 + 80 * (title.count('\n') + 1) + 5, sub, font(FONT_I, 40), YEL)
    m = mockup(cov, 720); im.paste(m, ((W - m.width) // 2, 270), m)
    y = 1080
    for b in bullets:
        d.text((150, y), '✓' if False else '•', font=font(FONT_B, 44), fill=YEL)
        d.text((195, y), b, font=font(FONT_7, 40), fill='white'); y += 62
    d.rounded_rectangle((W // 2 - 260, H - 125, W // 2 + 260, H - 40), 42, fill=YEL)
    text_center(d, W, H - 110, 'Disponible sur Amazon', font(FONT_B, 40), (20, 20, 40))
    return save(im, name)

def pin_zoom(key, name):
    if key == 'a':
        sol, num, _, _ = mosaic_assets('33_fenetre_chat'); z = num.crop((num.width // 4, num.height // 5, num.width * 3 // 4, num.height * 7 // 10))
        im = bg(W, H, NAVY, 77); d = ImageDraw.Draw(im)
        text_center(d, W, 50, 'Environ 500 zones\npar dessin', font(FONT_B, 70), 'white', spacing=6)
        text_center(d, W, 260, 'pour 1 à 2 heures de pure détente', font(FONT_I, 42), YEL)
        f = framed(z, 760); im.paste(f, ((W - f.width) // 2, 340)); corner_book(im, COV_A, 330)
        footer(d, ['Coloriages mystères · Noël cosy', 'Disponible', 'sur Amazon'])
    else:
        a, c = kids_pair('12_ourson'); z = a.crop((0, a.height // 5, a.width * 2 // 3, a.height * 4 // 5))
        im = bg(W, H, RED, 78); d = ImageDraw.Draw(im)
        text_center(d, W, 50, 'Des grandes cases\nfaciles à colorier', font(FONT_B, 70), 'white', spacing=6)
        text_center(d, W, 260, 'idéal pour les 6 - 10 ans', font(FONT_I, 42), YEL)
        f = framed(z, 760); im.paste(f, ((W - f.width) // 2, 340)); corner_book(im, COV_K, 330)
        footer(d, ['Coloriages magiques de Noël', 'Disponible', 'sur Amazon'])
    return save(im, name)

if __name__ == '__main__':
    A = ['01_chocolat', '02_maison', '03_sapin', '05_renne', '06_chat_bonnet', '13_village', '14_chalet', '19_biscuits', '25_marche', '32_lecture', '33_fenetre_chat', '36_boule_neige']
    K = ['16_pere_noel', '05_renne', '11_pingouin', '34_train', '12_ourson', '02_maison', '04_bonhomme', '15_traineau', '17_lutin', '18_cadeaux', '23_hibou', '24_renard']
    made = [
        pin_split('a', '14_chalet', 'Coloriage mystère\nde Noël', 'le chalet sous la neige apparaît', 'A01_chalet_avant_apres'),
        pin_split('k', '16_pere_noel', 'Coloriage magique\nde Noël', 'case après case, le Père Noël !', 'K01_pere_noel_avant_apres'),
        pin_grid('a', A[:9], 'Idée cadeau pour\nmaman ou mamie', '40 coloriages mystères de Noël', 'A02_cadeau_maman'),
        pin_grid('k', K[:9], 'Activité sans écran\npour Noël', '40 coloriages magiques dès 6 ans', 'K02_sans_ecran'),
        pin_split('a', '33_fenetre_chat', 'Le chat de Noël\nà colorier', 'coloriage par numéros pour adultes', 'A03_chat_avant_apres'),
        pin_split('k', '05_renne', 'Le petit renne\nà découvrir', 'coloriage par numéros dès 6 ans', 'K03_renne_avant_apres'),
        pin_book('a', 'Coloriages mystères\nNoël cosy', 'le livre de coloriage anti-stress', ['40 dessins de Noël cosy', 'Solutions incluses', 'Un dessin par page'], 'A04_livre'),
        pin_book('k', 'Coloriages magiques\nde Noël', 'le cahier des vacances de Noël', ['40 images à découvrir', 'Grandes cases dès 6 ans', 'Solutions incluses'], 'K04_livre'),
        pin_zoom('a', 'A05_500_zones'),
        pin_zoom('k', 'K05_grandes_cases'),
        pin_grid('a', A[3:12], 'Coloriages de Noël\nanti-stress', 'chalet, renne, marché de Noël...', 'A06_anti_stress'),
        pin_grid('k', K[3:12], 'Coloriage de Noël\nenfant 6 ans', 'renne, lutin, traîneau, cadeaux...', 'K06_enfant_6_ans'),
    ]
    print(made)
