"""Vidéo longue 16:9 « Les 24 heures miroirs », voix ElevenLabs + visuels Oracle Arcana.
Usage : python3 render_long.py outdir [--frames]
Voix : audio/p1.mp3, p2.mp3, p3.mp3 (textes voix_partie_1..3.txt)."""
import os, sys, re, math, random, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import render as R
from heures import M

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
GOLD, GOLD2, CREAM, ROSE = R.GOLD, R.GOLD2, R.CREAM, R.ROSE
GAP = 0.5  # silence entre les parties

def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))

def pauses(p):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-i', p, '-af', 'silencedetect=n=-35dB:d=0.28', '-f', 'null', '-'], capture_output=True, text=True).stderr
    res = []
    for m in re.finditer(r'silence_end: ([\d.]+) \| silence_duration: ([\d.]+)', out):
        e, d = float(m.group(1)), float(m.group(2)); res.append((e - d / 2, d))
    return res

def snap(t, ps, win):
    c = [(d, m) for m, d in ps if abs(m - t) <= win]
    return max(c)[1] if c else t

def timeline():
    """Paragraphes avec début/fin absolus et points de révélation, alignés sur les pauses de la voix."""
    import align
    paras = []; offset = 0.0
    for k in (1, 2, 3):
        ps_txt = open(f'{HERE}/voix_partie_{k}.txt').read().split('\n\n')
        mp = f'{HERE}/audio/p{k}.mp3'; D = dur(mp)
        al = align.align(ps_txt, mp, D); prev = 0.0
        for i, (p, sents) in enumerate(zip(ps_txt, al)):
            marks = {}; t0 = prev
            for s, t in sents:
                for key, pat in (('ange', "L'ange associé"), ('amour', 'En amour'), ('num', 'En numérologie'), ('tarot', 'Et dans le tarot')):
                    if s.startswith(pat): marks[key] = offset + t0
                t0 = t
            end = D if i == len(ps_txt) - 1 else sents[-1][1]
            paras.append({'text': p, 'start': offset + prev, 'end': offset + end, 'marks': marks})
            prev = end
        offset += D + GAP
    return paras, offset - GAP

# ---------- dessin ----------
def background():
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([14, 12, 38]); mid = np.array([38, 22, 66]); bot = np.array([12, 10, 30])
    g = np.where(y < 0.55, top + (mid - top) * (y / 0.55), mid + (bot - mid) * ((y - 0.55) / 0.45))
    img = np.repeat(g[:, None, :], W, axis=1).reshape(H, W, 3)
    yy, xx = np.mgrid[0:H, 0:W]
    for cx in (0.27, 0.5):
        d = np.sqrt(((xx - W * cx) / W) ** 2 + ((yy - H * 0.48) / H) ** 2)
        img = img + (np.clip(0.3 - d, 0, None) / 0.3)[..., None] * np.array([40, 26, 48])
    return np.clip(img, 0, 255).astype(np.uint8)

rng = random.Random(11)
STARS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.8, 2.4), rng.uniform(0, 6.28), rng.uniform(0.6, 2.0)) for _ in range(230)]
def stars(img, t):
    d = ImageDraw.Draw(img)
    for x, y, r, ph, sp in STARS:
        a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * sp + ph))
        d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(int(v * a) for v in (255, 240, 210)))

def wrap(d, txt, f, width):
    rows, cur = [], ''
    for w_ in txt.split(' '):
        t = (cur + ' ' + w_).strip()
        if d.textlength(t, font=f) > width and cur: rows.append(cur); cur = w_
        else: cur = t
    rows.append(cur); return rows

def layer(items, glow=True):
    """items: (text, font, color, x, y, width, align) -> RGBA, renvoie aussi le bas."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for txt, f, col, x, y, width, align in items:
        lh = int(f.size * 1.22)
        for i, r in enumerate(wrap(d, txt, f, width)):
            tw = d.textlength(r, font=f)
            xx = x + (width - tw) / 2 if align == 'c' else x
            d.text((xx, y + i * lh), r, font=f, fill=col + (255,))
    if glow:
        g = np.array(lay.filter(ImageFilter.GaussianBlur(12))).astype(np.float32); g[..., 3] *= 0.7
        lay = Image.alpha_composite(Image.fromarray(g.astype(np.uint8)), lay)
    return lay

def height(txt, f, width):
    d = ImageDraw.Draw(Image.new('RGB', (4, 4))); return int(f.size * 1.22) * len(wrap(d, txt, f, width))

F = lambda p, s, w=None: R.font(p, s, w)
LABEL = F(R.SANS, 30, 600); BIG = F(R.SERIF_B, 230); ANGEL = F(R.SERIF, 64); BODY = F(R.SERIF, 44); ITAL = F(R.SERIF_I, 46)
TITLE = F(R.SERIF_B, 92); SMALL = F(R.SANS, 34, 500)

def logo(cx, cy, R0=150):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.ellipse((cx - R0, cy - R0, cx + R0, cy + R0), outline=GOLD + (255,), width=5)
    r = 46; mx, my = cx - 6, cy - 50
    d.ellipse((mx - r, my - r, mx + r, my + r), fill=GOLD2 + (255,))
    d.ellipse((mx - r + 24, my - r - 10, mx + r + 24, my + r - 10), fill=(0, 0, 0, 0))
    R.star_shape(d, cx + 50, cy - 90, 7, GOLD2 + (255,))
    f = F(R.SERIF_B, 40)
    for t, y in (('ORACLE', cy + 30), ('ARCANA', cy + 78)):
        tw = d.textlength(t, font=f); d.text((cx - tw / 2, y - 22), t, font=f, fill=CREAM + (255,))
    return lay

def hour_scene(h):
    ange, t2, i2, pa, _, t4, i4, num, tarot = M[h]
    LX, LW = 120, 760; RX, RW = 960, 860
    g0 = layer([('HEURE MIROIR', LABEL, GOLD, LX, 300, LW, 'c'), (h.replace('h', ':'), BIG, GOLD2, LX, 340, LW, 'c'),
                (f'{t2} {i2}', ITAL, ROSE, LX, 640, LW, 'c')])
    blocks = [('ange', 'ANGE ASSOCIÉ', f'{ange}', pa), ('amour', 'EN AMOUR', t4, i4), ('num', 'NUMÉROLOGIE', num[0].upper() + num[1:], None)]
    if tarot: blocks.append(('tarot', 'ÉCHO DU TAROT', tarot, None))
    # hauteur totale pour centrer verticalement la colonne de droite
    def bh(b):
        k, lab, a, b2 = b
        f = ANGEL if k == 'ange' else BODY
        return 44 + height(a, f, RW) + (height(b2, BODY if k == 'ange' else ITAL, RW) if b2 else 0) + 44
    tot = sum(bh(b) for b in blocks); y = (H - tot) / 2 + 10
    out = [('start', g0)]
    for b in blocks:
        k, lab, a, b2 = b; items = [(lab, LABEL, GOLD, RX, y, RW, 'l')]; y += 44
        fa = ANGEL if k == 'ange' else BODY
        items.append((a, fa, CREAM, RX, y, RW, 'l')); y += height(a, fa, RW)
        if b2:
            fb = BODY if k == 'ange' else ITAL
            items.append((b2, fb, ROSE if k != 'ange' else CREAM, RX, y, RW, 'l')); y += height(b2, fb, RW)
        y += 44; out.append((k, layer(items)))
    sep = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sep).line((905, 250, 905, 830), fill=GOLD + (120,), width=2)
    out.insert(1, ('start', sep))
    return out

def intro_scene():
    return [('start', logo(W // 2, 300)),
            ('start', layer([('Les 24 heures miroirs', TITLE, GOLD2, 0, 500, W, 'c'),
                             ('et leur signification', ITAL, ROSE, 0, 625, W, 'c')])),
            (3.0, layer([('Ange gardien  ·  Amour  ·  Numérologie  ·  Tarot', SMALL, CREAM, 0, 760, W, 'c')]))]

def outro_scene():
    return [('start', logo(W // 2, 280)),
            ('start', layer([('La signification complète de chaque heure', SMALL, CREAM, 0, 500, W, 'c'),
                             ('oracle-arcana.fr', TITLE, GOLD2, 0, 560, W, 'c')])),
            (6.0, layer([('Horoscope du jour gratuit', ITAL, ROSE, 0, 720, W, 'c')])),
            (12.0, layer([('ABONNEZ-VOUS POUR VOTRE PROCHAIN SIGNE', LABEL, GOLD, 0, 860, W, 'c')]))]

def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    paras, total = timeline()
    hours = sorted(M); assert len(paras) == 26, len(paras)
    scenes = []
    for i, p in enumerate(paras):
        if i == 0: lays = intro_scene()
        elif i == 25: lays = outro_scene()
        else: lays = hour_scene(hours[i - 1])
        groups = []
        for key, lay in lays:
            if key == 'start': at = 0.15
            elif isinstance(key, float): at = key
            else: at = p['marks'].get(key, 0) - p['start'] - 0.2
            groups.append((max(0.15, at), lay))
        scenes.append((p['start'], p['end'], groups))
    json.dump([{'start': s, 'end': e, 'reveals': [g[0] for g in gr]} for s, e, gr in scenes], open(f'{out}/timeline.json', 'w'), indent=1)
    bg = background()
    if '--frames' in sys.argv:
        for i in (0, 1, 12, 25):
            s, e, gr = scenes[i]; img = Image.fromarray(bg.copy()); stars(img, 0); img = img.convert('RGBA')
            for at, lay in gr: img = Image.alpha_composite(img, lay)
            img.convert('RGB').save(f'{out}/check_{i}.jpg', quality=90)
        return
    # vidéo : une seule passe, images recalculées seulement pendant les fondus
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '20', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-tune', 'stillimage', f'{out}/video.tmp.mp4'], stdin=subprocess.PIPE)
    nf = int(math.ceil(total * FPS)) + FPS; cache = None; si = 0
    for k in range(nf):
        t = k / FPS
        while si < len(scenes) - 1 and t >= scenes[si + 1][0]: si += 1
        s, e, gr = scenes[si]; lt = t - s
        end_t = (scenes[si + 1][0] - s) if si < len(scenes) - 1 else 1e9
        fade_out = 1 - R.ease((lt - (end_t - 0.4)) / 0.4)
        anim = any(0 <= lt - at < 0.8 for at, _ in gr) or fade_out < 1 or lt < 0.2
        if anim or cache is None:
            img = Image.fromarray(bg.copy()); stars(img, s); img = img.convert('RGBA')
            for at, lay in gr:
                a = R.ease((lt - at) / 0.7) * fade_out
                if a <= 0: continue
                arr = np.array(lay); arr[..., 3] = (arr[..., 3] * a).astype(np.uint8)
                img = Image.alpha_composite(img, Image.fromarray(arr))
            fr = img.convert('RGB').tobytes()
            if not anim: cache = fr
            else: cache = None
        else: fr = cache
        p.stdin.write(fr)
    p.stdin.close(); assert p.wait() == 0
    os.replace(f'{out}/video.tmp.mp4', f'{out}/video.mp4')
    # audio : voix + musique douce en fond
    sil = f'{out}/sil.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo', '-t', str(GAP), sil], check=True)
    with open(f'{out}/alist.txt', 'w') as f:
        for i, k in enumerate((1, 2, 3)):
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{HERE}/audio/p{k}.mp3', '-ar', '44100', '-ac', '2', f'{out}/v{k}.wav'], check=True)
            f.write(f"file '{os.path.abspath(out)}/v{k}.wav'\n")
            if i < 2: f.write(f"file '{os.path.abspath(sil)}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{out}/alist.txt', '-c', 'copy', f'{out}/voice.wav'], check=True)
    R.audio(nf / FPS, [s for s, _, _ in scenes], f'{out}/music.wav', seed=3)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{out}/voice.wav', '-i', f'{out}/music.wav', '-filter_complex',
                    '[1:a]volume=0.16[m];[0:a]apad[v];[v][m]amix=inputs=2:duration=shortest:normalize=0,alimiter=limit=0.95[a]', '-map', '[a]', f'{out}/mix.wav'], check=True)
    final = f'{out}/Les_24_heures_miroirs.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{out}/video.mp4', '-i', f'{out}/mix.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
    os.replace(final + '.tmp.mp4', final); print(final, total)

if __name__ == '__main__':
    main()
