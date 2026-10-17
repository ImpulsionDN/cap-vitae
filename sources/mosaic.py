"""Coloriage mystère en mosaïque : motif SVG -> zones irrégulières numérotées -> page PDF."""
import io, cairosvg, numpy as np
from PIL import Image
from scipy import ndimage
from scipy.spatial import cKDTree
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
D = os.path.dirname(os.path.abspath(__file__))
for n, f in [('Arc5', 'Archivo-500.ttf'), ('Arc7', 'Archivo-700.ttf'), ('ArcB', 'ArchivoBlack.ttf')]:
    pdfmetrics.registerFont(TTFont(n, os.path.join(D, f)))

PAL = {
    1: ('Rouge', '#d62828'), 2: ('Vert sapin', '#1b5e20'), 3: ('Vert clair', '#7cb342'),
    4: ('Marron', '#6d4c41'), 5: ('Jaune', '#fdd835'), 6: ('Orange', '#fb8c00'),
    7: ('Bleu ciel', '#81d4fa'), 8: ('Bleu nuit', '#1a237e'), 9: ('Rose', '#f48fb1'),
    10: ('Beige', '#d7b899'), 11: ('Gris', '#9e9e9e'), 12: ('Noir', '#212121'),
}
def hx(h): return np.array([int(h[i:i+2], 16) for i in (1, 3, 5)])
PARR = np.array([[255, 255, 255]] + [hx(PAL[k][1]) for k in range(1, 13)])

W, H = 8.5 * inch, 11 * inch
M = 0.55 * inch
DPI = 300
GW_IN = (W - 2 * M) / inch          # 7.4 in
GH_IN = GW_IN * 320 / 300           # garde le ratio du motif

def labels(svg, px_w, px_h):
    png = cairosvg.svg2png(url=svg, output_width=px_w, output_height=px_h, background_color='white')
    im = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(int)
    best = np.zeros(im.shape[:2], int); bd = np.full(im.shape[:2], 1 << 30)
    for k, p in enumerate(PARR):
        d = ((im - p) ** 2).sum(-1)
        m = d < bd; best[m] = k; bd[m] = d[m]
    return best  # 0 = blanc, 1..12

def segment(lab, target_px, rng):
    """Découpe chaque zone de couleur en cellules irrégulières (Voronoï contraint)."""
    cells = np.zeros(lab.shape, int)
    nid = 1
    color_of = {}
    for col in np.unique(lab):
        comp, n = ndimage.label(lab == col)
        for k in range(1, n + 1):
            mask = comp == k
            ys, xs = np.nonzero(mask)
            area = len(ys)
            if area < 40:
                continue
            ns = max(1, int(round(area / target_px)))
            pts = np.c_[ys, xs]
            seeds = pts[rng.choice(len(pts), ns, replace=False)].astype(float)
            sub = pts[rng.choice(len(pts), min(len(pts), 20000), replace=False)]
            for _ in range(6):  # relaxation de Lloyd (sur un échantillon) pour des cellules régulières
                a = cKDTree(seeds).query(sub)[1]
                cnt = np.bincount(a, minlength=ns)
                sy = np.bincount(a, sub[:, 0], minlength=ns); sx = np.bincount(a, sub[:, 1], minlength=ns)
                ok = cnt > 0
                seeds[ok] = np.c_[sy[ok] / cnt[ok], sx[ok] / cnt[ok]]
            a = cKDTree(seeds).query(pts)[1]
            cells[ys, xs] = nid + a
            for s in range(ns): color_of[nid + s] = int(col)
            nid += ns
    # pixels orphelins (minuscules zones) -> cellule voisine
    if (cells == 0).any():
        idx = ndimage.distance_transform_edt(cells == 0, return_distances=False, return_indices=True)
        cells = cells[idx[0], idx[1]]
    return cells, color_of

def render(svg, target_area_in2=0.11, seed=1):
    pw, ph = int(GW_IN * DPI), int(GH_IN * DPI)
    lab = labels(svg, pw, ph)
    rng = np.random.default_rng(seed)
    cells, color_of = segment(lab, target_area_in2 * DPI * DPI, rng)
    # contours
    edge = np.zeros(cells.shape, bool)
    edge[:, 1:] |= cells[:, 1:] != cells[:, :-1]
    edge[1:, :] |= cells[1:, :] != cells[:-1, :]
    edge = ndimage.binary_dilation(edge, iterations=2)
    # numéros : point le plus intérieur de chaque cellule
    marks = []
    objs = ndimage.find_objects(cells)
    for cid, sl in enumerate(objs, 1):
        if sl is None: continue
        sub = cells[sl] == cid
        dt = ndimage.distance_transform_edt(np.pad(sub, 1))[1:-1, 1:-1]
        y, x = np.unravel_index(dt.argmax(), dt.shape)
        marks.append((sl[1].start + x, sl[0].start + y, dt.max(), color_of[cid]))
    return edge, marks, lab, cells, color_of

def preview(cells, color_of, edge, path):
    lut = np.zeros(cells.max() + 1, int)
    for k, v in color_of.items(): lut[k] = v
    rgb = PARR[lut[cells]].astype(np.uint8)
    rgb[edge] = (60, 60, 60)
    Image.fromarray(rgb).resize((rgb.shape[1] // 3, rgb.shape[0] // 3)).save(path)

def page(cv, edge, marks, num, tmpdir='/tmp'):
    gw, gh = GW_IN * inch, GH_IN * inch
    gx, gy = M, H - 1.0 * inch - gh
    img = Image.fromarray(np.where(edge, 70, 255).astype(np.uint8))
    p = os.path.join(tmpdir, f'_edge_{num}.png'); img.save(p, dpi=(DPI, DPI))
    cv.drawImage(p, gx, gy, gw, gh)
    cv.setLineWidth(1.2); cv.setStrokeGray(0.25); cv.rect(gx, gy, gw, gh)
    cv.setFont('Arc7', 11); cv.setFillGray(0.15)
    cv.drawString(M, H - 0.68 * inch, f'N° {num}')
    cv.setFont('Arc5', 9); cv.setFillGray(0.45)
    cv.drawRightString(W - M, H - 0.68 * inch, "Colorie chaque zone selon son numéro et découvre l'image")
    sc = inch / DPI
    for x, y, r, col in marks:
        if col == 0: continue
        rpt = r * sc
        fs = max(4.2, min(8.0, rpt * 1.25))
        cv.setFont('Arc5', fs); cv.setFillGray(0.3)
        cv.drawCentredString(gx + x * sc, gy + gh - y * sc - fs * 0.36, str(col))
    used = sorted({m[3] for m in marks if m[3]})
    ly = gy - 0.34 * inch
    cv.setFont('Arc7', 10); cv.setFillGray(0.15); cv.drawString(M, ly, 'Couleurs :')
    x = M + 0.85 * inch
    for n in used:
        lab = f'{n} = {PAL[n][0]}'
        w = pdfmetrics.stringWidth(lab, 'Arc5', 10)
        if x + w > W - M: ly -= 0.24 * inch; x = M + 0.85 * inch
        cv.setFont('Arc5', 10); cv.drawString(x, ly, lab); x += w + 0.22 * inch
    cv.setFont('Arc5', 9); cv.setFillGray(0.4)
    cv.drawString(M, ly - 0.27 * inch, 'Zone sans numéro = laisser blanc.')
    cv.showPage()
