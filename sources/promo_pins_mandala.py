"""Épingles Pinterest (1000x1500) pour le livre Mandalas de Noël."""
import os, cairosvg
from PIL import Image, ImageDraw
from promo_common import font, text_center, front_cover, mockup, FONT_B, FONT_I, FONT_7
from promo_static import bg
from mandala_gen import render

W, H = 1000, 1500
GRN, GOLD, RED = (15, 61, 36), (249, 199, 79), (198, 40, 40)
OUT = 'pins_m'; os.makedirs(OUT, exist_ok=True); os.makedirs('mcache', exist_ok=True)
COV = front_cover('Mandalas_Noel_couverture.pdf', 86, '/tmp/front_mandalas.png')


def png(seed, colored, px):
    p = f'mcache/p{seed:02d}_{int(colored)}_{px}.png'
    if not os.path.exists(p):
        cairosvg.svg2png(bytestring=render(seed, colored, colored).encode(), write_to=p, output_width=px)
    return Image.open(p).convert('RGB')


def disc(img):
    px = img.width; m = Image.new('L', (px, px), 0); ImageDraw.Draw(m).ellipse((0, 0, px - 1, px - 1), fill=255)
    o = Image.new('RGBA', (px, px), (0, 0, 0, 0)); o.paste(img, (0, 0), m); return o


def half(seed, px):
    a = png(seed, False, px).copy(); b = png(seed, True, px)
    a.paste(b.crop((px // 2, 0, px, px)), (px // 2, 0)); return a


def on_white(img, pad=24):
    px = img.width; c = Image.new('RGBA', (px + 2 * pad, px + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(c).ellipse((0, 0, px + 2 * pad - 1, px + 2 * pad - 1), fill='white')
    c.alpha_composite(disc(img), (pad, pad)); return c


def base(name, title, sub):
    im = bg(W, H, GRN, hash(name) % 100).convert('RGBA'); d = ImageDraw.Draw(im)
    text_center(d, W, 50, title, font(FONT_B, 70), 'white', spacing=6)
    y = 50 + 85 * (title.count('\n') + 1) + 5
    text_center(d, W, y, sub, font(FONT_I, 42), GOLD)
    return im, d, y + 70


def corner(im, h=320):
    m = mockup(COV, h); im.alpha_composite(m, (W - m.width - 5, H - m.height - 5))


def foot(d, a, b='Disponible', c='sur Amazon', y=H - 230):
    d.text((50, y), a, font=font(FONT_I, 40), fill=GOLD)
    d.text((50, y + 60), b, font=font(FONT_B, 46), fill='white')
    d.text((50, y + 118), c, font=font(FONT_B, 46), fill='white')


def save(im, name):
    im.convert('RGB').save(f'{OUT}/{name}.jpg', quality=90); return name


def pin_split(seed, title, sub, name):
    im, d, y = base(name, title, sub)
    m = on_white(half(seed, 820)); im.alpha_composite(m, ((W - m.width) // 2, y))
    corner(im); foot(d, 'Avant / Après'); return save(im, name)


def pin_line(seed, title, sub, name):
    im, d, y = base(name, title, sub)
    m = on_white(png(seed, False, 820)); im.alpha_composite(m, ((W - m.width) // 2, y))
    corner(im); foot(d, '40 mandalas dans le livre'); return save(im, name)


def pin_grid(seeds, title, sub, name, cell=270):
    im, d, y = base(name, title, sub)
    gap = 30; x0 = (W - (3 * cell + 2 * gap)) // 2
    for i, s in enumerate(seeds[:6]):
        m = on_white(png(s, True, cell - 16), 8)
        im.alpha_composite(m, (x0 + (i % 3) * (cell + gap), y + 10 + (i // 3) * (cell + gap)))
    corner(im); foot(d, '40 mandalas de Noël'); return save(im, name)


def pin_zoom(seed, title, sub, name):
    im, d, y = base(name, title, sub)
    big = half(seed, 1800); z = big.crop((450, 450, 1350, 1350)).resize((820, 820), Image.LANCZOS)
    f = Image.new('RGB', (840, 840), 'white'); f.paste(z, (10, 10)); im.paste(f, ((W - 840) // 2, y))
    corner(im); foot(d, 'Des détails à savourer'); return save(im, name)


def pin_book(title, sub, bullets, name):
    im, d, y = base(name, title, sub)
    m = mockup(COV, 720); im.alpha_composite(m, ((W - m.width) // 2, y - 10))
    yy = 1080
    for b in bullets:
        d.text((150, yy), '•', font=font(FONT_B, 44), fill=GOLD)
        d.text((195, yy), b, font=font(FONT_7, 40), fill='white'); yy += 62
    d.rounded_rectangle((W // 2 - 260, H - 125, W // 2 + 260, H - 40), 42, fill=GOLD)
    text_center(d, W, H - 110, 'Disponible sur Amazon', font(FONT_B, 40), (20, 20, 40))
    return save(im, name)


def pin_steps(seed, name):
    im, d, y = base(name, 'Comment colorier\nun mandala ?', 'la méthode zen en 3 étapes')
    steps = ['Commencez\npar le centre', 'Avancez anneau\naprès anneau', 'Admirez\nle résultat']
    px = 330; l = png(seed, False, px); c = png(seed, True, px)
    mid = l.copy(); mm = Image.new('L', (px, px), 0); ImageDraw.Draw(mm).ellipse((px // 4, px // 4, px * 3 // 4, px * 3 // 4), fill=255)
    mid.paste(c, (0, 0), mm)
    for i, (s, img) in enumerate(zip(steps, [l, mid, c]), 1):
        im.alpha_composite(on_white(img, 10), (60, y));
        d.ellipse((440, y + 120, 520, y + 200), fill=GOLD)
        text_center(d, 960, y + 132, str(i), font(FONT_B, 50), (20, 20, 40))
        d.multiline_text((550, y + 120), s, font=font(FONT_7, 44), fill='white', spacing=8)
        y += px + 40
    corner(im, 280); return save(im, name)


if __name__ == '__main__':
    made = [
        pin_split(3, 'Mandala de Noël\nà colorier', 'pour ados et adultes', 'M01_mandala_noel'),
        pin_steps(7, 'M02_comment'),
        pin_grid([1, 4, 9, 12, 15, 22], 'Mandalas de Noël\nanti-stress', '40 modèles tous différents', 'M03_grille'),
        pin_book('Mandalas de Noël', 'le livre de coloriage zen', ['40 mandalas originaux', 'Motifs de Noël cachés', 'Grand format 21,6 x 27,9 cm'], 'M04_livre'),
        pin_split(11, 'Coloriage zen\npour les fêtes', 'un mandala, un moment de calme', 'M05_zen'),
        pin_zoom(5, 'Sapins, houx,\nétoiles cachés', 'des motifs de Noël dans chaque anneau', 'M06_details'),
        pin_line(18, 'Mandala de Noël\nadulte', 'prêt à colorier', 'M07_trait'),
        pin_split(20, 'Art-thérapie\nde Noël', 'se détendre en coloriant', 'M08_art_therapie'),
        pin_grid([2, 6, 14, 19, 25, 30], 'Idée cadeau\npour ado', '40 mandalas de Noël à colorier', 'M09_cadeau_ado'),
        pin_book('Le cadeau zen\nde Noël', 'pour celles et ceux qui aiment colorier', ['Un mandala par page', 'Verso blanc, pas de transfert', 'Page test pour vos couleurs'], 'M10_cadeau'),
        pin_split(24, 'Mandala facile\nou détaillé', 'des niveaux pour tous', 'M11_niveaux'),
        pin_zoom(28, 'Coloriage\nanti-stress', 'feutres fins, crayons ou stylos gel', 'M12_anti_stress'),
        pin_split(31, 'Mandala de Noël\nfeutres et crayons', 'à colorier anneau après anneau', 'M13_feutres'),
        pin_grid([8, 13, 17, 27, 33, 36], "Calendrier de l'Avent\nzen", 'un mandala par jour', 'M14_avent'),
        pin_line(35, 'Mandala à colorier\npour Noël', 'grand format', 'M15_trait2'),
        pin_split(38, 'Une pause\ncocooning', 'loin de l\'agitation des fêtes', 'M16_cocooning'),
        pin_book('Idée cadeau\nfemme ou ado', 'mandalas de Noël à colorier', ['40 mandalas de Noël', 'Pour ados et adultes', 'Coloriage anti-stress'], 'M17_cadeau_femme'),
        pin_split(16, 'Mandala de Noël\ncosy', 'un plaid, un thé, des crayons', 'M18_cosy'),
        pin_grid([0, 10, 21, 26, 34, 39], 'Mandalas de Noël\npour adultes', 'zen, détaillés, festifs', 'M19_adultes'),
        pin_split(37, 'Dernier cadeau\nde Noël ?', 'les mandalas de Noël à colorier', 'M20_derniere_minute'),
    ]
    print(made)
