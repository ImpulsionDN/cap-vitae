"""Livret enfants : Coloriages magiques de Noël (pixel, dès 6 ans)."""
import glob, os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import engine
from engine import PAL, W, H
from book_adult import NAMES
pdfmetrics.registerFont(TTFont('FrIt', 'FrauncesIt.ttf'))
engine.COLS, engine.ROWS = 26, 28
TITLE, SUB, TAG, BRAND = 'Coloriages magiques', 'de Noël', '40 images à découvrir · dès 6 ans', 'Studio Impulsion'
motifs = sorted(os.path.basename(f)[:-4] for f in glob.glob('mosa/*.svg'))
M = 0.55 * inch

def centered(cv, t, f, s, y, g=0.1):
    cv.setFont(f, s); cv.setFillGray(g); cv.drawCentredString(W / 2, y, t)

def page(cv, G, num):
    C, R = engine.COLS, engine.ROWS
    cell = (W - 2 * M) / C
    gx, gy = M, H - 1.0 * inch - R * cell
    cv.setFont('Arc7', 13); cv.setFillGray(0.15); cv.drawString(M, H - 0.7 * inch, f'N° {num}')
    cv.setFont('Arc5', 10); cv.setFillGray(0.4)
    cv.drawRightString(W - M, H - 0.7 * inch, 'Colorie chaque case avec la couleur de son numéro !')
    cv.setLineWidth(0.4); cv.setStrokeGray(0.55)
    for r in range(R):
        for c in range(C):
            x, y = gx + c * cell, gy + (R - 1 - r) * cell
            cv.rect(x, y, cell, cell, stroke=1, fill=0)
            n = G[r][c]
            if n:
                fs = 8.5 if n < 10 else 7.2
                cv.setFont('Arc5', fs); cv.setFillGray(0.3)
                cv.drawCentredString(x + cell / 2, y + cell / 2 - fs * 0.35, str(n))
    cv.setLineWidth(1.2); cv.setStrokeGray(0.2); cv.rect(gx, gy, C * cell, R * cell)
    used = sorted({n for row in G for n in row if n})
    ly = gy - 0.36 * inch
    cv.setFont('Arc7', 11); cv.setFillGray(0.15); cv.drawString(M, ly, 'Couleurs :')
    x = M + 0.95 * inch
    for n in used:
        lab = f'{n} = {PAL[n][0]}'; w = pdfmetrics.stringWidth(lab, 'Arc5', 11)
        if x + w > W - M: ly -= 0.26 * inch; x = M + 0.95 * inch
        cv.setFont('Arc5', 11); cv.drawString(x, ly, lab); x += w + 0.25 * inch
    cv.setFont('Arc5', 10); cv.setFillGray(0.45); cv.drawString(M, ly - 0.3 * inch, 'Case sans numéro = laisse-la blanche.')
    cv.showPage()

def build(out):
    cv = canvas.Canvas(out, pagesize=(W, H)); cv.setTitle(f'{TITLE} {SUB}'); cv.setAuthor(BRAND)
    centered(cv, BRAND.upper(), 'Arc7', 10, H - 1.4 * inch, 0.35)
    centered(cv, TITLE, 'ArcB', 38, H - 3.6 * inch); centered(cv, SUB, 'ArcB', 48, H - 4.4 * inch, 0.25)
    centered(cv, TAG, 'FrIt', 18, H - 5.2 * inch, 0.2); cv.showPage()
    cv.setFont('Arc5', 9); cv.setFillGray(0.25); y = 2.4 * inch
    for l in [f'{TITLE} {SUB}', f'© 2026 {BRAND}. Tous droits réservés.',
              'Les pages peuvent être photocopiées pour un usage strictement personnel et familial.',
              'Les illustrations ont été conçues avec l\'aide d\'outils numériques.', 'Première édition : novembre 2026.']:
        cv.drawString(M, y, l); y -= 0.24 * inch
    cv.showPage()
    centered(cv, 'Comment ça marche ?', 'ArcB', 26, H - 1.4 * inch)
    cv.setFont('Arc5', 14); cv.setFillGray(0.15); y = H - 2.3 * inch
    for l in ['1. Regarde le numéro écrit dans chaque case.', '2. Trouve sa couleur sous le dessin.',
              '3. Colorie la case avec cette couleur.', '4. Case après case, une image de Noël apparaît !', '',
              'Astuce : colorie d\'abord tous les 1, puis tous les 2, etc.', 'Les solutions sont à la fin du livre.']:
        cv.drawString(1.0 * inch, y, l); y -= 0.38 * inch
    cv.setStrokeGray(0.3); cv.setLineWidth(1.2); cv.roundRect(1.0 * inch, 1.3 * inch, W - 2.0 * inch, 1.5 * inch, 14)
    centered(cv, 'Ce livre appartient à', 'FrIt', 17, 2.35 * inch, 0.2); cv.line(2.0 * inch, 1.7 * inch, W - 2.0 * inch, 1.7 * inch)
    cv.showPage()
    centered(cv, 'Teste tes couleurs', 'ArcB', 26, H - 1.4 * inch)
    bw, bh = 2.0 * inch, 1.3 * inch; x0 = (W - 3 * bw - 0.6 * inch) / 2
    for i in range(12):
        n = i + 1; c, r = i % 3, i // 3
        x = x0 + c * (bw + 0.3 * inch); yy = H - 2.2 * inch - (r + 1) * (bh + 0.45 * inch)
        cv.setStrokeGray(0.3); cv.roundRect(x, yy, bw, bh, 10)
        cv.setFont('Arc7', 13); cv.setFillGray(0.15); cv.drawCentredString(x + bw / 2, yy - 0.26 * inch, f'{n}  {PAL[n][0]}')
    cv.showPage()
    grids = {}
    for i, b in enumerate(motifs, 1):
        G = engine.grid(f'mosa/{b}.svg'); grids[b] = G
        page(cv, G, i); cv.showPage()
    for p in range(0, len(motifs), 9):
        if p == 0: centered(cv, 'Les solutions', 'ArcB', 24, H - 0.95 * inch)
        tw = 2.1 * inch; th = tw * engine.ROWS / engine.COLS
        for i, b in enumerate(motifs[p:p + 9]):
            c, r = i % 3, i // 3
            x = (W - 3 * tw - 0.6 * inch) / 2 + c * (tw + 0.3 * inch); yy = H - 1.25 * inch - (r + 1) * (th + 0.4 * inch)
            engine.preview(grids[b], f'cache/{b}_kid.png', 20)
            Image.open(f'cache/{b}_kid.png').convert('L').save(f'cache/{b}_kidg.png')
            cv.drawImage(f'cache/{b}_kidg.png', x, yy, tw, th)
            cv.setFont('Arc7', 9.5); cv.setFillGray(0.2); cv.drawString(x, yy - 0.17 * inch, f'N° {motifs.index(b) + 1}  {NAMES[b]}')
        cv.showPage()
    centered(cv, 'Bravo, tu as tout colorié !', 'ArcB', 24, H / 2 + 0.6 * inch)
    centered(cv, 'Si ce livre vous a plu, un avis sur Amazon nous aide beaucoup.', 'Arc5', 12, H / 2, 0.3)
    cv.showPage()
    cv.save()

if __name__ == '__main__':
    build('Noel_magique_enfants_interieur.pdf')
