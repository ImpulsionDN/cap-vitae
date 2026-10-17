"""Couverture KDP broché : Coloriages magiques de Noël (enfants)."""
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import engine
pdfmetrics.registerFont(TTFont('FrIt', 'FrauncesIt.ttf'))
engine.COLS, engine.ROWS = 26, 28
import os
NOBC = os.environ.get('NOBC') == '1'
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 90
BLEED = 0.125; spine = PAGES * 0.002252
TW = (2 * BLEED + 2 * 8.5 + spine) * inch; TH = (11 + 2 * BLEED) * inch
RED = (0xd6 / 255, 0x28 / 255, 0x28 / 255); YEL = (0xfd / 255, 0xd8 / 255, 0x35 / 255); GRN = (0x1b / 255, 0x5e / 255, 0x20 / 255)

def teaser(b, out, s=40):
    G = engine.grid(f'mosa/{b}.svg'); C, R = engine.COLS, engine.ROWS
    im = Image.new('RGB', (C * s, R * s), 'white'); d = ImageDraw.Draw(im)
    f = ImageFont.truetype('Archivo-500.ttf', int(s * 0.5))
    for r in range(R):
        for c in range(C):
            x, y = c * s, r * s; n = G[r][c]
            if c >= C // 2 and n: d.rectangle([x, y, x + s, y + s], fill=engine.PRGB[n])
            elif n: d.text((x + s / 2, y + s / 2), str(n), fill=(90, 90, 90), font=f, anchor='mm')
            d.rectangle([x, y, x + s, y + s], outline=(150, 150, 150), width=1)
    im.save(out)

def build(out):
    cv = canvas.Canvas(out, pagesize=(TW, TH))
    cv.setFillColorRGB(*RED); cv.rect(0, 0, TW, TH, fill=1, stroke=0)
    rng = np.random.default_rng(5); cv.setFillColorRGB(1, 1, 1)
    for _ in range(120): cv.circle(rng.uniform(0, TW), rng.uniform(0, TH), rng.uniform(1.5, 4.5), fill=1, stroke=0)
    fx = (BLEED + 8.5 + spine) * inch; cx = fx + 4.25 * inch
    cv.setFont('Arc7', 11); cv.drawCentredString(cx, TH - 0.75 * inch, 'S T U D I O   I M P U L S I O N')
    cv.setFont('ArcB', 48); cv.drawCentredString(cx, TH - 1.75 * inch, 'Coloriages')
    cv.drawCentredString(cx, TH - 2.5 * inch, 'magiques')
    cv.setFillColorRGB(*YEL); cv.setFont('ArcB', 58); cv.drawCentredString(cx, TH - 3.4 * inch, 'de Noël')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('FrIt', 20); cv.drawCentredString(cx, TH - 3.9 * inch, '40 images à découvrir case par case')
    teaser('04_bonhomme', 'cache/teaser_kids.png')
    tw = 5.0 * inch; th = tw * 28 / 26; tx, ty = cx - tw / 2, 1.3 * inch
    cv.setFillColorRGB(1, 1, 1); cv.roundRect(tx - 10, ty - 10, tw + 20, th + 20, 14, fill=1, stroke=0)
    cv.drawImage('cache/teaser_kids.png', tx, ty, tw, th)
    bx, by = fx + 7.4 * inch, ty + th - 0.3 * inch
    cv.setFillColorRGB(*GRN); cv.circle(bx, by, 0.72 * inch, fill=1, stroke=0)
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc7', 12); cv.drawCentredString(bx, by + 0.12 * inch, 'dès')
    cv.setFont('ArcB', 28); cv.drawCentredString(bx, by - 0.25 * inch, '6 ans')
    cv.setFont('Arc7', 13); cv.drawCentredString(cx, 0.72 * inch, 'Grandes cases  ·  Solutions incluses  ·  Grand format')
    bcx = (BLEED + 4.25) * inch; bxl = (BLEED + 0.6) * inch
    cv.setFillColorRGB(*YEL); cv.setFont('ArcB', 26)
    cv.drawCentredString(bcx, TH - 1.25 * inch, 'Une case, un numéro,')
    cv.drawCentredString(bcx, TH - 1.7 * inch, 'une surprise !')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc5', 13); y = TH - 2.3 * inch
    for l in ['Un bonhomme de neige, un renne, le Père Noël, un petit train...',
              'Ton enfant colorie chaque case avec la couleur de son numéro',
              'et découvre l\'image de Noël cachée. Calme, concentration',
              'et fierté garanties pendant les vacances !']:
        cv.drawCentredString(bcx, y, l); y -= 0.26 * inch
    y -= 0.12 * inch; cv.setFont('Arc7', 13)
    for l in ['• 40 coloriages magiques, un par page', '• Grandes cases faciles à colorier',
              '• 12 couleurs simples, crayons ou feutres', '• Solutions à la fin du livre']:
        cv.drawString(bxl + 0.6 * inch, y, l); y -= 0.28 * inch
    sel = ['16_pere_noel', '05_renne', '11_pingouin', '34_train', '12_ourson', '02_maison']
    s = 1.85 * inch; sh = s * 28 / 26
    for i, b in enumerate(sel):
        G = engine.grid(f'mosa/{b}.svg'); engine.preview(G, f'cache/{b}_kid.png', 20)
        c, r = i % 3, i // 3; x = bxl + c * (s + 0.2 * inch); yy = 1.8 * inch + (1 - r) * (sh + 0.2 * inch)
        cv.setFillColorRGB(1, 1, 1); cv.roundRect(x - 4, yy - 4, s + 8, sh + 8, 6, fill=1, stroke=0)
        cv.drawImage(f'cache/{b}_kid.png', x, yy, s, sh)
    cv.setFillColorRGB(1, 1, 1)
    if not NOBC: cv.rect((BLEED + 8.5 - 0.25 - 2.0) * inch, (BLEED + 0.25) * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=0)
    cv.save()

if __name__ == '__main__':
    build('Noel_magique_enfants_couverture.pdf')
    print('largeur', round(TW / inch, 4), 'dos', round(spine, 4))
