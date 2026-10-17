"""Coloriage mystère par numéros (pixel) : SVG motif -> grille numérotée -> page PDF."""
import io, cairosvg
from PIL import Image
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arc5', 'Archivo-500.ttf'))
pdfmetrics.registerFont(TTFont('Arc7', 'Archivo-700.ttf'))
pdfmetrics.registerFont(TTFont('ArcB', 'ArchivoBlack.ttf'))

# palette : numéro -> (nom, couleur utilisée dans les SVG)
PAL = {
    1: ('Rouge', '#d62828'), 2: ('Vert sapin', '#1b5e20'), 3: ('Vert clair', '#7cb342'),
    4: ('Marron', '#6d4c41'), 5: ('Jaune', '#fdd835'), 6: ('Orange', '#fb8c00'),
    7: ('Bleu ciel', '#81d4fa'), 8: ('Bleu nuit', '#1a237e'), 9: ('Rose', '#f48fb1'),
    10: ('Beige', '#d7b899'), 11: ('Gris', '#9e9e9e'), 12: ('Noir', '#212121'),
}
WHITE = (255, 255, 255)
def hx(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
PRGB = {k: hx(v[1]) for k, v in PAL.items()}

COLS, ROWS, S = 30, 32, 20

def grid(svg_path):
    png = cairosvg.svg2png(url=svg_path, output_width=COLS * S, output_height=ROWS * S, background_color='white')
    im = Image.open(io.BytesIO(png)).convert('RGB')
    G = []
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            px = im.crop((c * S + 3, r * S + 3, c * S + S - 3, r * S + S - 3)).getdata()
            col = Counter(px).most_common(1)[0][0]
            best, bd = 0, sum((a - b) ** 2 for a, b in zip(col, WHITE))
            for k, p in PRGB.items():
                d = sum((a - b) ** 2 for a, b in zip(col, p))
                if d < bd: best, bd = k, d
            row.append(best)
        G.append(row)
    return G

def preview(G, path, s=12):
    im = Image.new('RGB', (COLS * s, ROWS * s), 'white')
    for r in range(ROWS):
        for c in range(COLS):
            if G[r][c]:
                im.paste(PRGB[G[r][c]], (c * s, r * s, c * s + s, r * s + s))
    im.save(path)

W, H = 8.5 * inch, 11 * inch
def page(cv, G, num, title):
    m = 0.55 * inch
    cell = (W - 2 * m) / COLS
    gx, gy = m, H - 1.05 * inch - ROWS * cell
    cv.setFont('Arc7', 11); cv.setFillGray(0.15)
    cv.drawString(m, H - 0.72 * inch, f'N° {num}')
    cv.setFont('Arc5', 9); cv.setFillGray(0.45); cv.drawRightString(W - m, H - 0.72 * inch, 'Colorie chaque case selon son numéro et découvre l\'image')
    cv.setLineWidth(0.35); cv.setStrokeGray(0.55)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = gx + c * cell, gy + (ROWS - 1 - r) * cell
            cv.rect(x, y, cell, cell, stroke=1, fill=0)
            n = G[r][c]
            if n:
                cv.setFont('Arc5', 7 if n < 10 else 6.2); cv.setFillGray(0.35)
                cv.drawCentredString(x + cell / 2, y + cell / 2 - 2.4, str(n))
    cv.setLineWidth(1.1); cv.setStrokeGray(0.2); cv.rect(gx, gy, COLS * cell, ROWS * cell)
    used = sorted({n for row in G for n in row if n})
    ly = gy - 0.32 * inch
    cv.setFont('Arc7', 10); cv.setFillGray(0.15)
    cv.drawString(m, ly, 'Couleurs :')
    x = m + 0.85 * inch
    for n in used:
        lab = f'{n} = {PAL[n][0]}'
        cv.setFont('Arc5', 10); w = pdfmetrics.stringWidth(lab, 'Arc5', 10)
        if x + w > W - m: ly -= 0.24 * inch; x = m + 0.85 * inch
        cv.drawString(x, ly, lab); x += w + 0.22 * inch
    cv.setFont('Arc5', 9); cv.setFillGray(0.4)
    cv.drawString(m, ly - 0.27 * inch, 'Case sans numéro = laisser blanc.')
    cv.showPage()

def blank(cv):
    cv.showPage()
