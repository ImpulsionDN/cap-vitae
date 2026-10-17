"""Générateur de mandalas de Noël (SVG, formes fermées coloriables).
Chaque mandala = centre + couches concentriques de motifs répétés en symétrie radiale.
render(seed, colored=False) -> texte SVG (viewBox -500 -500 1000 1000)."""
import math, random

SW = 2.6      # trait principal (unités ; 1000 u = ~7.4 in)
SW2 = 1.9     # trait de détail
PALETTE = ['#c62828', '#2e7d32', '#f9a825', '#1565c0', '#ad1457', '#6d4c41',
           '#00838f', '#ef6c00', '#7cb342', '#5e35b1', '#d84315', '#81d4fa']

def f(v):
    return f'{v:.2f}'

# ---------- motifs : dessinés pointe vers le haut, base en (0,0), hauteur h vers y négatif ----------
def petal(w, h, k=0.5):
    return (f'M0,0 C{f(w*k)},{f(-h*0.25)} {f(w*k)},{f(-h*0.75)} 0,{f(-h)} '
            f'C{f(-w*k)},{f(-h*0.75)} {f(-w*k)},{f(-h*0.25)} 0,0Z')

def flame(w, h):
    return (f'M0,0 C{f(w*0.55)},{f(-h*0.15)} {f(w*0.45)},{f(-h*0.6)} 0,{f(-h)} '
            f'C{f(-w*0.45)},{f(-h*0.6)} {f(-w*0.55)},{f(-h*0.15)} 0,0Z')

def arch(w, h):
    # arche en ogive, base large
    return (f'M{f(-w/2)},0 C{f(-w/2)},{f(-h*0.55)} {f(-w*0.15)},{f(-h*0.8)} 0,{f(-h)} '
            f'C{f(w*0.15)},{f(-h*0.8)} {f(w/2)},{f(-h*0.55)} {f(w/2)},0Z')

def star(n, ro, ri, cx=0, cy=0, rot=-90):
    pts = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        a = math.radians(rot + i * 180 / n)
        pts.append(f'{f(cx + r*math.cos(a))},{f(cy + r*math.sin(a))}')
    return 'M' + ' L'.join(pts) + 'Z'

def circle(cx, cy, r):
    return (f'M{f(cx-r)},{f(cy)} a{f(r)},{f(r)} 0 1,0 {f(2*r)},0 '
            f'a{f(r)},{f(r)} 0 1,0 {f(-2*r)},0Z')

def diamond(w, h):
    return f'M0,0 L{f(w/2)},{f(-h/2)} L0,{f(-h)} L{f(-w/2)},{f(-h/2)}Z'

def heart(s, cy):
    y = cy + s * 0.45
    return (f'M0,{f(y)} C{f(-s*1.1)},{f(y-s*0.7)} {f(-s*0.55)},{f(y-s*1.45)} 0,{f(y-s*0.95)} '
            f'C{f(s*0.55)},{f(y-s*1.45)} {f(s*1.1)},{f(y-s*0.7)} 0,{f(y)}Z')

def tree(w, h):
    out = [f'M{f(-w*0.08)},0 L{f(w*0.08)},0 L{f(w*0.08)},{f(-h*0.14)} L{f(-w*0.08)},{f(-h*0.14)}Z']
    tiers = [(0.12, 0.5, 0.5), (0.38, 0.75, 0.4), (0.62, 1.0, 0.32)]
    for y0, y1, hw in tiers:
        out.append(f'M{f(-w*hw)},{f(-h*y0)} L{f(w*hw)},{f(-h*y0)} L0,{f(-h*y1)}Z')
    return out

def holly(w, h):
    def leaf(sign):
        # feuille de houx à pointes, orientée en diagonale
        pts = []
        L = h * 0.62; W = w * 0.2
        for i in range(7):
            t = i / 6
            off = W * math.sin(math.pi * t) * (1.25 if i % 2 else 0.85)
            pts.append((off, -L * t))
        for i in range(5, 0, -1):
            t = i / 6
            off = W * math.sin(math.pi * t) * (1.25 if i % 2 else 0.85)
            pts.append((-off, -L * t))
        a = math.radians(32 * sign)
        rp = [(x*math.cos(a) - y*math.sin(a), x*math.sin(a) + y*math.cos(a) - h*0.3) for x, y in pts]
        return 'M0,' + f(-h*0.3) + ' ' + ' '.join(f'L{f(x)},{f(y)}' for x, y in rp) + 'Z'
    out = [leaf(1), leaf(-1)]
    br = min(w, h) * 0.09
    for dx, dy in [(-br*1.1, -h*0.24), (br*1.1, -h*0.24), (0, -h*0.36)]:
        out.append(circle(dx, dy, br))
    return out

def bell(w, h):
    s = min(w, h * 0.9)
    return [f'M{f(-s*0.42)},{f(-h*0.18)} C{f(-s*0.38)},{f(-h*0.55)} {f(-s*0.3)},{f(-h*0.85)} 0,{f(-h*0.88)} '
            f'C{f(s*0.3)},{f(-h*0.85)} {f(s*0.38)},{f(-h*0.55)} {f(s*0.42)},{f(-h*0.18)} Z',
            circle(0, -h*0.12, s*0.09),
            circle(0, -h*0.93, s*0.06)]

def ornament(w, h):
    r = min(w * 0.44, h * 0.36)
    cy = -h * 0.08 - r
    return [circle(0, cy, r),
            f'M{f(-r*0.28)},{f(cy-r*0.95)} L{f(r*0.28)},{f(cy-r*0.95)} L{f(r*0.28)},{f(cy-r*1.25)} L{f(-r*0.28)},{f(cy-r*1.25)}Z',
            f'M{f(-r*0.95)},{f(cy-r*0.22)} C{f(-r*0.4)},{f(cy+r*0.08)} {f(r*0.4)},{f(cy+r*0.08)} {f(r*0.95)},{f(cy-r*0.22)} '
            f'L{f(r*0.95)},{f(cy+r*0.22)} C{f(r*0.4)},{f(cy+r*0.52)} {f(-r*0.4)},{f(cy+r*0.52)} {f(-r*0.95)},{f(cy+r*0.22)}Z']

def gift(w, h):
    s = min(w * 0.8, h * 0.75)
    x0, y0 = -s/2, -h*0.08
    return [f'M{f(x0)},{f(y0)} L{f(-x0)},{f(y0)} L{f(-x0)},{f(y0-s*0.8)} L{f(x0)},{f(y0-s*0.8)}Z',
            f'M{f(-s*0.09)},{f(y0)} L{f(s*0.09)},{f(y0)} L{f(s*0.09)},{f(y0-s*0.8)} L{f(-s*0.09)},{f(y0-s*0.8)}Z',
            petal(s*0.35, s*0.32).replace('M0,0', f'M0,{f(y0-s*0.8)}', 1) if False else
            f'M0,{f(y0-s*0.8)} C{f(-s*0.35)},{f(y0-s*1.05)} {f(-s*0.35)},{f(y0-s*0.75)} 0,{f(y0-s*0.8)} '
            f'C{f(s*0.35)},{f(y0-s*1.05)} {f(s*0.35)},{f(y0-s*0.75)} 0,{f(y0-s*0.8)}Z']

def snowstar(w, h):
    r = min(w, h) * 0.48
    return [star(6, r, r * 0.45, 0, -h/2), circle(0, -h/2, r * 0.18)]

def candle(w, h):
    cw = min(w * 0.38, h * 0.26)
    return [f'M{f(-cw/2)},{f(-h*0.05)} L{f(cw/2)},{f(-h*0.05)} L{f(cw/2)},{f(-h*0.6)} L{f(-cw/2)},{f(-h*0.6)}Z',
            flame(cw * 1.2, h * 0.33).replace('M0,0', f'M0,{f(-h*0.62)}')
            .replace(' 0,0Z', f' 0,{f(-h*0.62)}Z')]

def shift(path, dy):
    """décale un chemin construit à la base 0 (petal/flame/arch/diamond) de dy en y."""
    import re
    def rep(m):
        return f'{m.group(1)},{f(float(m.group(2)) + dy)}'
    return re.sub(r'(-?\d+\.?\d*),(-?\d+\.?\d*)', rep, path)

# ---------- couches ----------
MOTIFS = ['petal', 'double_petal', 'flame', 'arch', 'diamond', 'heart', 'tree', 'holly',
          'bell', 'ornament', 'gift', 'snowstar', 'candle', 'dots', 'teeth', 'scallop']
XMAS = {'tree', 'holly', 'bell', 'ornament', 'gift', 'snowstar', 'heart'}

def layer_shapes(kind, n, r0, r1, rng):
    """Renvoie [(angle, [chemins], role)] pour une couche."""
    h = r1 - r0
    slot = 2 * math.pi * (r0 + h * 0.5) / n
    w = slot * 0.88
    out = []
    for i in range(n):
        ang = 360 * i / n
        if kind == 'petal':
            p = [petal(w, h), shift(petal(w*0.45, h*0.55), -h*0.2)]
        elif kind == 'double_petal':
            out.append((ang + 180 / n, [petal(w*1.05, h), shift(petal(w*0.4, h*0.45), -h*0.35)], 'b'))
            p = [petal(w*0.8, h*0.78), shift(petal(w*0.35, h*0.4), -h*0.18)]
        elif kind == 'flame':
            p = [flame(w, h), shift(flame(w*0.45, h*0.5), -h*0.15)]
        elif kind == 'arch':
            wa = slot * 0.99
            p = [arch(wa, h), shift(arch(wa*0.5, h*0.55), 0), circle(0, -h*0.75, min(wa, h)*0.08)]
        elif kind == 'diamond':
            p = [diamond(w*0.9, h), shift(diamond(w*0.45, h*0.5), -h*0.25)]
        elif kind == 'heart':
            s = min(w*0.5, h*0.62)
            p = [heart(s, -h*0.5)]
        elif kind == 'tree':
            p = tree(min(w*1.05, h*0.95), h*0.96)
        elif kind == 'holly':
            p = holly(w, h)
        elif kind == 'bell':
            p = bell(w, h)
        elif kind == 'ornament':
            p = ornament(w, h)
        elif kind == 'gift':
            p = gift(w, h)
        elif kind == 'snowstar':
            p = snowstar(w, h)
        elif kind == 'candle':
            p = candle(w, h)
        elif kind == 'dots':
            rr = min(slot*0.3, h*0.38)
            p = [circle(0, -h/2, rr), circle(0, -h/2, rr*0.45)]
        elif kind == 'teeth':
            wt = slot * 1.0
            p = [f'M{f(-wt/2)},0 L{f(wt/2)},0 L0,{f(-h)}Z']
        elif kind == 'scallop':
            wt = slot * 1.0
            p = [arch(wt, h*0.9), circle(0, -h*0.35, min(wt, h)*0.13)]
        out.append((ang, p, 'a'))
    return out

def plan(seed):
    rng = random.Random(seed)
    n = rng.choice([6, 8, 8, 10, 12])
    radii = [rng.uniform(58, 82)]
    kinds = []
    xm = sorted(XMAS); rng.shuffle(xm)
    base = ['petal', 'double_petal', 'flame', 'arch', 'diamond', 'dots', 'teeth', 'scallop']
    i = 0
    while True:
        if i % 2 == 1 and xm:
            k = xm.pop(); t = rng.uniform(62, 80)
        else:
            k = rng.choice(base)
            while kinds and k == kinds[-1]:
                k = rng.choice(base)
            t = rng.uniform(42, 62)
        if radii[-1] + t > 405:
            break
        kinds.append(k); radii.append(radii[-1] + t); i += 1
    # répartir le reste pour finir à 405, puis couche de silhouette
    scale = (405 - radii[0]) / (radii[-1] - radii[0])
    radii = [radii[0] + (r - radii[0]) * scale for r in radii]
    kinds.append(rng.choice(['double_petal', 'arch', 'petal', 'flame']))
    radii.append(405 + rng.uniform(62, 82))
    return n, radii, kinds, None, rng.choice(['star', 'snow', 'flower', 'star8'])

RATIO = {'petal': 0.7, 'double_petal': 0.8, 'flame': 0.6, 'arch': 1.0, 'diamond': 0.6,
         'dots': 0.85, 'teeth': 0.75, 'scallop': 0.95}

def count(kind, n, r0, r1, last=False):
    h = r1 - r0
    circ = 2 * math.pi * (r0 + h * 0.5)
    ratio = RATIO.get(kind, 1.05)
    if last:
        ratio *= 1.4
    return n * max(1, round(circ / (h * ratio) / n))

XPAL = ['#c62828', '#1b5e20', '#f9a825', '#1a237e', '#7cb342', '#ad1457', '#81d4fa', '#ef6c00', '#ffffff']

def render(seed, colored=False, xmas_pal=False):
    rng = random.Random(seed * 7 + 1)
    n, radii, kinds, mult, center = plan(seed)
    cols = (XPAL if xmas_pal else PALETTE)[:]
    random.Random(seed).shuffle(cols)
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-500 -500 1000 1000">',
             '<rect x="-500" y="-500" width="1000" height="1000" fill="white"/>']

    def fill(ci):
        return cols[ci % len(cols)] if colored else 'white'

    # couches de l'extérieur vers l'intérieur pour que les anneaux se superposent proprement
    for li in range(len(kinds) - 1, -1, -1):
        r0, r1 = radii[li], radii[li + 1]
        gap = (r1 - r0) * 0.04
        # anneau de fond de la couche (zone coloriable)
        if kinds[li] in XMAS or kinds[li] in ('dots',):
            parts.append(f'<path d="{circle(0, 0, r1)}" fill="{fill(li*3+2) if colored else "white"}" '
                         f'stroke="black" stroke-width="{SW}"/>')
        shapes = layer_shapes(kinds[li], count(kinds[li], n, r0, r1, li == len(kinds) - 1), r0 + gap, r1 - gap, rng)
        g = []
        for ang, paths, role in sorted(shapes, key=lambda s: s[2] != 'b'):
            for pi, d in enumerate(paths):
                ci = li * 3 + (pi if role == 'a' else pi + 1)
                g.append(f'<path transform="rotate({f(ang)}) translate(0,{f(-(r0+gap))})" d="{d}" '
                         f'fill="{fill(ci)}" stroke="black" stroke-width="{SW if pi == 0 else SW2}" '
                         f'stroke-linejoin="round"/>')
        parts += g
        if kinds[li] not in XMAS and kinds[li] != 'dots':
            pass
    # anneaux séparateurs
    for r in radii[1:-1]:
        parts.append(f'<circle r="{f(r)}" fill="none" stroke="black" stroke-width="{SW}"/>')
    # centre
    rc = radii[0]
    parts.append(f'<path d="{circle(0, 0, rc)}" fill="{fill(1)}" stroke="black" stroke-width="{SW}"/>')
    if center == 'star':
        parts.append(f'<path d="{star(5, rc*0.85, rc*0.38)}" fill="{fill(2)}" stroke="black" stroke-width="{SW}"/>')
    elif center == 'star8':
        parts.append(f'<path d="{star(8, rc*0.88, rc*0.5)}" fill="{fill(2)}" stroke="black" stroke-width="{SW}"/>')
        parts.append(f'<path d="{circle(0, 0, rc*0.25)}" fill="{fill(4)}" stroke="black" stroke-width="{SW2}"/>')
    elif center == 'snow':
        parts.append(f'<path d="{star(6, rc*0.88, rc*0.35)}" fill="{fill(2)}" stroke="black" stroke-width="{SW}"/>')
        parts.append(f'<path d="{star(6, rc*0.4, rc*0.2, rot=-60)}" fill="{fill(4)}" stroke="black" stroke-width="{SW2}"/>')
    else:
        for k in range(8):
            parts.append(f'<path transform="rotate({k*45})" d="{petal(rc*0.42, rc*0.85)}" fill="{fill(2)}" '
                         f'stroke="black" stroke-width="{SW2}"/>')
        parts.append(f'<path d="{circle(0, 0, rc*0.25)}" fill="{fill(4)}" stroke="black" stroke-width="{SW2}"/>')
    parts.append('</svg>')
    return '\n'.join(parts)

if __name__ == '__main__':
    import cairosvg, sys
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        cairosvg.svg2png(bytestring=render(s).encode(), write_to=f'/tmp/m{s}.png', output_width=500)
        cairosvg.svg2png(bytestring=render(s, True).encode(), write_to=f'/tmp/m{s}c.png', output_width=500)
