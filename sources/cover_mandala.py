"""Couverture KDP broché : Mandalas de Noël."""
import os, sys, numpy as np
from PIL import Image, ImageDraw
import cairosvg
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from mandala_gen import render
for n, f in [('Arc5', 'Archivo-500.ttf'), ('Arc7', 'Archivo-700.ttf'), ('ArcB', 'ArchivoBlack.ttf'), ('FrIt', 'FrauncesIt.ttf')]:
    pdfmetrics.registerFont(TTFont(n, f))
NOBC = os.environ.get('NOBC') == '1'
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 86
BLEED = 0.125; spine = PAGES * 0.002252
TW = (2 * BLEED + 2 * 8.5 + spine) * inch; TH = (11 + 2 * BLEED) * inch
GRN = (0x0f / 255, 0x3d / 255, 0x24 / 255)
GOLD = (0xf9 / 255, 0xc7 / 255, 0x4f / 255)
RED = (0xc6 / 255, 0x28 / 255, 0x28 / 255)

def teaser(seed, out, px=1800):
    """Moitié gauche au trait, moitié droite coloriée, sur disque blanc."""
    cairosvg.svg2png(bytestring=render(seed).encode(), write_to='/tmp/t_l.png', output_width=px)
    cairosvg.svg2png(bytestring=render(seed, True, True).encode(), write_to='/tmp/t_c.png', output_width=px)
    a = Image.open('/tmp/t_l.png').convert('RGB'); b = Image.open('/tmp/t_c.png').convert('RGB')
    a.paste(b.crop((px // 2, 0, px, px)), (px // 2, 0))
    mask = Image.new('L', (px, px), 0); ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    out_im = Image.new('RGBA', (px, px), (0, 0, 0, 0)); out_im.paste(a, (0, 0), mask)
    out_im.save(out)

def thumb(seed, out, px=700):
    cairosvg.svg2png(bytestring=render(seed, True, True).encode(), write_to='/tmp/th.png', output_width=px)
    im = Image.open('/tmp/th.png').convert('RGB')
    mask = Image.new('L', (px, px), 0); ImageDraw.Draw(mask).ellipse((0, 0, px - 1, px - 1), fill=255)
    o = Image.new('RGBA', (px, px), (0, 0, 0, 0)); o.paste(im, (0, 0), mask); o.save(out)

def build(out):
    cv = canvas.Canvas(out, pagesize=(TW, TH))
    cv.setFillColorRGB(*GRN); cv.rect(0, 0, TW, TH, fill=1, stroke=0)
    rng = np.random.default_rng(11)
    for _ in range(150):
        cv.setFillColorRGB(1, 1, 1) if rng.random() < 0.75 else cv.setFillColorRGB(*GOLD)
        cv.circle(rng.uniform(0, TW), rng.uniform(0, TH), rng.uniform(1.2, 4), fill=1, stroke=0)
    fx = (BLEED + 8.5 + spine) * inch; cx = fx + 4.25 * inch
    # 1re de couverture
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc7', 11)
    cv.drawCentredString(cx, TH - 0.75 * inch, 'S T U D I O   I M P U L S I O N')
    cv.setFont('ArcB', 64); cv.drawCentredString(cx, TH - 1.85 * inch, 'Mandalas')
    cv.setFillColorRGB(*GOLD); cv.setFont('ArcB', 60); cv.drawCentredString(cx, TH - 2.75 * inch, 'de Noël')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('FrIt', 20)
    cv.drawCentredString(cx, TH - 3.3 * inch, '40 mandalas à colorier pour ados et adultes')
    teaser(0, '/tmp/teaser_m.png')
    d = 6.0 * inch; ty = 1.25 * inch
    cv.setFillColorRGB(1, 1, 1); cv.circle(cx, ty + d / 2, d / 2 + 8, fill=1, stroke=0)
    cv.drawImage('/tmp/teaser_m.png', cx - d / 2, ty, d, d, mask='auto')
    bx, by = fx + 7.45 * inch, ty + d - 0.15 * inch
    cv.setFillColorRGB(*RED); cv.circle(bx, by, 0.7 * inch, fill=1, stroke=0)
    cv.setFillColorRGB(1, 1, 1); cv.setFont('ArcB', 30); cv.drawCentredString(bx, by + 0.02 * inch, '40')
    cv.setFont('Arc7', 11); cv.drawCentredString(bx, by - 0.25 * inch, 'mandalas')
    cv.setFont('Arc7', 13)
    cv.drawCentredString(cx, 0.75 * inch, 'Anti-stress  ·  Motifs de Noël  ·  Grand format')
    # 4e de couverture
    bcx = (BLEED + 4.25) * inch; bxl = (BLEED + 0.6) * inch
    cv.setFillColorRGB(*GOLD); cv.setFont('ArcB', 26)
    cv.drawCentredString(bcx, TH - 1.25 * inch, 'Un moment de calme')
    cv.drawCentredString(bcx, TH - 1.7 * inch, 'sous le sapin.')
    cv.setFillColorRGB(1, 1, 1); cv.setFont('Arc5', 12.5); y = TH - 2.3 * inch
    for l in ['Sapins, houx, cadeaux, cloches, étoiles...',
              '40 mandalas originaux où se cachent des motifs de Noël.',
              'Du centre vers l\'extérieur, anneau après anneau,',
              'laissez vos couleurs faire le reste.']:
        cv.drawCentredString(bcx, y, l); y -= 0.25 * inch
    y -= 0.15 * inch; cv.setFont('Arc7', 12.5)
    for l in ['• 40 mandalas de Noël originaux, un par page', '• Impression recto seul : pas de transfert de feutre',
              '• Page pour tester vos couleurs', '• Grand format 21,6 x 27,9 cm']:
        cv.drawString(bxl + 0.6 * inch, y, l); y -= 0.27 * inch
    s = 2.3 * inch
    for i, seed in enumerate([3, 9, 14, 21, 30, 38][:4]):
        c, r = i % 2, i // 2
        thumb(seed, f'/tmp/th{i}.png')
        x = bcx - s - 0.15 * inch + c * (s + 0.3 * inch); yy = 1.75 * inch + (1 - r) * (s + 0.25 * inch)
        cv.drawImage(f'/tmp/th{i}.png', x, yy, s, s, mask='auto')
    if not NOBC:
        cv.setFillColorRGB(1, 1, 1)
        cv.rect((BLEED + 8.5 - 0.25 - 2.0) * inch, (BLEED + 0.25) * inch, 2.0 * inch, 1.2 * inch, fill=1, stroke=0)
    cv.save()

if __name__ == '__main__':
    build(os.environ.get('OUT', 'Mandalas_Noel_couverture.pdf'))
    print('largeur', round(TW / inch, 4), 'dos', round(spine, 4))
