"""Couverture KDP broché : Coloriages mystères - Noël cosy."""
import sys, numpy as np
from PIL import Image, ImageDraw
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import mosaic  # enregistre les polices Archivo
pdfmetrics.registerFont(TTFont('FrIt', 'FrauncesIt.ttf'))

import os
NOBC = os.environ.get('NOBC') == '1'
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 92
BLEED = 0.125
spine = PAGES * 0.002252
TW = (2 * BLEED + 2 * 8.5 + spine) * inch
TH = (11 + 2 * BLEED) * inch
NAVY = (0x1a / 255, 0x23 / 255, 0x7e / 255)
RED = (0xd6 / 255, 0x28 / 255, 0x28 / 255)
YEL = (0xfd / 255, 0xd8 / 255, 0x35 / 255)

def teaser(b, out):
    """Moitié gauche : zones numérotées ; moitié droite : coloriée."""
    sol = Image.open(f'cache/{b}_sol.png').convert('RGB')
    edge = Image.open(f'cache/{b}_edge.png').convert('L').resize(sol.size)
    num = Image.new('RGB', sol.size, 'white'); num.paste((70, 70, 70), mask=edge.point(lambda v: 255 if v < 128 else 0))
    import json
    from PIL import ImageFont
    d0 = ImageDraw.Draw(num); k = sol.size[0] / (edge_w := Image.open(f'cache/{b}_edge.png').size[0])
    for x, y, r, col in json.load(open(f'cache/{b}.json')):
        if col == 0 or x * k > sol.size[0] / 2: continue
        fs = max(9, min(17, int(r * k * 1.1)))
        d0.text((x * k, y * k), str(col), fill=(90, 90, 90), font=ImageFont.truetype('Archivo-500.ttf', fs), anchor='mm')
    w = sol.size[0]
    out_im = num.copy(); out_im.paste(sol.crop((w // 2, 0, w, sol.size[1])), (w // 2, 0))
    d = ImageDraw.Draw(out_im); d.line([(w // 2, 0), (w // 2, sol.size[1])], fill=(255, 255, 255), width=8)
    out_im.save(out)

def build(out):
    cv = canvas.Canvas(out, pagesize=(TW, TH))
    cv.setFillColorRGB(*NAVY); cv.rect(0, 0, TW, TH, fill=1, stroke=0)
    rng = np.random.default_rng(3)
    cv.setFillColorRGB(1, 1, 1)
    for _ in range(140):
        cv.circle(rng.uniform(0, TW), rng.uniform(0, TH), rng.uniform(1.5, 4.5), fill=1, stroke=0)
    fx = (BLEED + 8.5 + spine) * inch  # début de la 1re de couverture
    cx = fx + 4.25 * inch
    # --- 1re de couverture ---
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc7', 11)
    cv.drawCentredString(cx, TH - 0.75 * inch, 'S T U D I O   I M P U L S I O N')
    cv.setFont('ArcB', 46); cv.drawCentredString(cx, TH - 1.75 * inch, 'Coloriages')
    cv.drawCentredString(cx, TH - 2.45 * inch, 'mystères')
    cv.setFillColorRGB(*YEL); cv.setFont('ArcB', 60); cv.drawCentredString(cx, TH - 3.35 * inch, 'Noël cosy')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('FrIt', 19)
    cv.drawCentredString(cx, TH - 3.85 * inch, '40 coloriages par numéros pour adultes')
    teaser('03_sapin', 'cache/teaser.png')
    tw = 5.15 * inch; th = tw * 320 / 300
    tx, ty = cx - tw / 2, 1.4 * inch
    cv.setFillColorRGB(1, 1, 1); cv.roundRect(tx - 10, ty - 10, tw + 20, th + 20, 14, fill=1, stroke=0)
    cv.drawImage('cache/teaser.png', tx, ty, tw, th)
    # badge
    bx, by = fx + 7.35 * inch, ty + th - 0.35 * inch
    cv.setFillColorRGB(*RED); cv.circle(bx, by, 0.72 * inch, fill=1, stroke=0)
    cv.setFillColorRGB(1, 1, 1); cv.setFont('ArcB', 30); cv.drawCentredString(bx, by + 0.02 * inch, '40')
    cv.setFont('Arc7', 11); cv.drawCentredString(bx, by - 0.25 * inch, 'dessins')
    cv.setFont('Arc7', 13); cv.setFillColorRGB(1, 1, 1)
    cv.drawCentredString(cx, 0.95 * inch, 'Anti-stress  ·  Solutions incluses  ·  Grand format')
    # --- 4e de couverture ---
    bxl = (BLEED + 0.6) * inch; bcx = (BLEED + 4.25) * inch
    cv.setFillColorRGB(*YEL); cv.setFont('ArcB', 26)
    cv.drawCentredString(bcx, TH - 1.25 * inch, 'Coloriez, découvrez,')
    cv.drawCentredString(bcx, TH - 1.7 * inch, 'savourez Noël.')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc5', 12.5)
    txt = ['Un chocolat chaud, un chalet sous la neige, un petit renne,',
           'un chat au coin du feu... 40 scènes de Noël tout en douceur',
           'se cachent dans ces pages. Suivez les numéros, zone après zone,',
           'et regardez l\'image apparaître sous vos crayons.']
    y = TH - 2.3 * inch
    for l in txt: cv.drawCentredString(bcx, y, l); y -= 0.25 * inch
    y -= 0.15 * inch
    cv.setFont('Arc7', 12.5)
    for l in ['• 40 coloriages mystères originaux, un par page', '• 12 couleurs simples, crayons ou feutres',
              '• Impression recto seul : pas de transfert', '• Page test des couleurs et solutions à la fin']:
        cv.drawString(bxl + 0.5 * inch, y, l); y -= 0.27 * inch
    sel = ['01_chocolat', '14_chalet', '05_renne', '33_fenetre_chat', '25_marche', '04_bonhomme']
    s = 1.85 * inch; sh = s * 320 / 300
    for i, b in enumerate(sel):
        c, r = i % 3, i // 3
        x = bxl + c * (s + 0.2 * inch); yy = 1.8 * inch + (1 - r) * (sh + 0.2 * inch)
        cv.setFillColorRGB(1, 1, 1); cv.roundRect(x - 4, yy - 4, s + 8, sh + 8, 6, fill=1, stroke=0)
        cv.drawImage(f'cache/{b}_sol.png', x, yy, s, sh)
    # zone code-barres laissée libre (KDP l'imprime en bas à droite de la 4e)
    cv.setFillColorRGB(1, 1, 1)
    if not NOBC: cv.rect((BLEED + 8.5 - 0.25 - 2.0) * inch, (BLEED + 0.25) * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=0)
    cv.save()

if __name__ == '__main__':
    build('Noel_cosy_adultes_couverture.pdf')
    print('largeur', round(TW / inch, 4), 'hauteur', TH / inch, 'dos', round(spine, 4))
