"""Short YouTube heure miroir, 1080x1920, 30 fps. Usage: python3 render.py data.json outdir [--frames]"""
import json, sys, os, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
GF = '/usr/share/fonts/truetype/google-fonts/ofl/'
SERIF = GF + 'crimsontext/CrimsonText-SemiBold.ttf'
SERIF_I = GF + 'crimsontext/CrimsonText-Italic.ttf'
SERIF_B = GF + 'crimsontext/CrimsonText-Bold.ttf'
SANS = GF + 'montserrat/Montserrat[wght].ttf'
GOLD = (222, 184, 110); GOLD2 = (246, 214, 150); CREAM = (246, 238, 224); ROSE = (226, 150, 182)

def font(p, s, wght=None):
    f = ImageFont.truetype(p, s)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

def background():
    y = np.linspace(0, 1, H)[:, None]
    top = np.array([14, 12, 38]); mid = np.array([38, 22, 66]); bot = np.array([12, 10, 30])
    g = np.where(y < 0.55, top + (mid - top) * (y / 0.55), mid + (bot - mid) * ((y - 0.55) / 0.45))
    img = np.repeat(g[:, None, :], W, axis=1).reshape(H, W, 3)
    # soft glow centre
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * 0.42) / H) ** 2)
    img = img + (np.clip(0.35 - d, 0, None) / 0.35)[..., None] * np.array([60, 40, 70])
    return np.clip(img, 0, 255).astype(np.uint8)

rng = random.Random(7)
STARS = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0.8, 2.6), rng.uniform(0, 6.28), rng.uniform(0.6, 2.0)) for _ in range(170)]

def draw_stars(img, t):
    d = ImageDraw.Draw(img)
    for x, y, r, ph, sp in STARS:
        a = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * sp + ph))
        c = tuple(int(v * a) for v in (255, 240, 210))
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)

def text_layer(lines, glow=True):
    """lines: list of (text, fontpath, size, color, y, wght). returns RGBA."""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for txt, fp, sz, col, y, wg in lines:
        f = font(fp, sz, wg)
        # wrap to 900px
        words = txt.split(' '); rows = []; cur = ''
        for w_ in words:
            test = (cur + ' ' + w_).strip()
            if d.textlength(test, font=f) > 900 and cur: rows.append(cur); cur = w_
            else: cur = test
        rows.append(cur)
        lh = int(sz * 1.18)
        for i, r in enumerate(rows):
            tw = d.textlength(r, font=f)
            d.text(((W - tw) / 2, y + i * lh), r, font=f, fill=col + (255,))
    if glow:
        g = lay.filter(ImageFilter.GaussianBlur(14))
        ga = np.array(g).astype(np.float32); ga[..., 3] *= 0.8
        base = Image.alpha_composite(Image.fromarray(ga.astype(np.uint8)), lay)
        return base
    return lay

def star_shape(d, x, y, r, col):
    d.polygon([(x, y - r * 2), (x + r * .5, y - r * .5), (x + r * 2, y), (x + r * .5, y + r * .5), (x, y + r * 2), (x - r * .5, y + r * .5), (x - r * 2, y), (x - r * .5, y - r * .5)], fill=col)

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)

def nrows(txt, fp, sz, wg):
    f = font(fp, sz, wg); d = ImageDraw.Draw(Image.new('RGB', (10, 10)))
    rows = 1; cur = ''
    for w_ in txt.split(' '):
        test = (cur + ' ' + w_).strip()
        if d.textlength(test, font=f) > 900 and cur: rows += 1; cur = w_
        else: cur = test
    return rows

def build(data):
    L = lambda s: (s, SANS, 44, GOLD, None, 600)
    scenes = []
    for sc in data['scenes']:
        groups = []
        bottom = 0
        for g in sc['groups']:
            lines = []
            for ln in g['lines']:
                fp = {'label': SANS, 'big': SERIF_B, 'title': SERIF, 'italic': SERIF_I, 'small': SANS}[ln['style']]
                sz = {'label': 46, 'big': ln.get('size', 250), 'title': ln.get('size', 92), 'italic': ln.get('size', 80), 'small': ln.get('size', 50)}[ln['style']]
                col = {'label': GOLD, 'big': GOLD2, 'title': CREAM, 'italic': ROSE, 'small': CREAM}[ln['style']]
                wg = 600 if ln['style'] == 'label' else (500 if ln['style'] == 'small' else None)
                lines.append((ln['text'], fp, sz, col, ln['y'], wg))
            fixed = []
            for (txt, fp, sz, col, y, wg) in lines:
                if y < bottom + 30: y = bottom + 30
                bottom = y + int(sz * 1.18) * nrows(txt, fp, sz, wg)
                fixed.append((txt, fp, sz, col, y, wg))
            groups.append((g['at'], text_layer(fixed)))
        scenes.append((sc['dur'], groups, sc.get('logo', False)))
    return scenes

LOGO = None
def logo_layer():
    global LOGO
    if LOGO is None:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        cx, cy, R = W // 2, 450, 185
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=GOLD + (255,), width=6)
        r = 58; mx, my = cx - 8, cy - 62
        d.ellipse((mx - r, my - r, mx + r, my + r), fill=GOLD2 + (255,))
        d.ellipse((mx - r + 30, my - r - 12, mx + r + 30, my + r - 12), fill=(0, 0, 0, 0))
        star_shape(d, cx + 62, cy - 110, 8, GOLD2 + (255,))
        f = font(SERIF_B, 50)
        for t, y in (('ORACLE', cy + 40), ('ARCANA', cy + 98)):
            tw = d.textlength(t, font=f); d.text((cx - tw / 2, y - 28), t, font=f, fill=CREAM + (255,))
        LOGO = lay
    return LOGO

def frame(bg, scene, t, gt):
    dur, groups, logo = scene
    img = Image.fromarray(bg.copy()); draw_stars(img, gt)
    img = img.convert('RGBA')
    fade_out = 1 - ease((t - (dur - 0.45)) / 0.45) if logo is False else 1
    for at, lay in groups:
        a = ease((t - at) / 0.7) * fade_out
        if a <= 0: continue
        dy = int((1 - ease((t - at) / 0.9)) * 40)
        arr = np.array(lay); arr[..., 3] = (arr[..., 3] * a).astype(np.uint8)
        L = Image.fromarray(arr)
        if dy: L = L.transform(L.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy))
        img = Image.alpha_composite(img, L)
    if logo:
        a = ease(t / 0.8); arr = np.array(logo_layer()); arr[..., 3] = (arr[..., 3] * a).astype(np.uint8)
        img = Image.alpha_composite(img, Image.fromarray(arr))
    return img.convert('RGB')

PROGS = [
    [[0, 3, 7, 14], [-4, 0, 3, 10], [-2, 2, 5, 12], [-5, 0, 3, 10]],
    [[0, 4, 7, 11], [5, 9, 12, 16], [-3, 0, 4, 7], [2, 5, 9, 12]],
    [[0, 3, 7, 10], [-2, 2, 5, 9], [-4, 0, 3, 7], [-7, -3, 0, 3]],
    [[0, 7, 12, 16], [-3, 4, 9, 12], [-5, 2, 7, 11], [-1, 2, 7, 14]],
    [[0, 3, 7, 12], [1, 5, 8, 12], [-2, 3, 7, 10], [0, 3, 7, 14]],
]
def audio(total, scene_starts, path, seed=0):
    rnd = random.Random(seed)
    sr = 44100; n = int(total * sr); t = np.arange(n) / sr
    out = np.zeros(n)
    root = 196.0 * 2 ** (rnd.randint(-3, 4) / 12)
    prog = PROGS[seed % len(PROGS)]
    bright = rnd.uniform(0.06, 0.22); lfo = rnd.uniform(0.08, 0.2)
    seg = total / len(prog)
    for i, ch in enumerate(prog):
        s0 = i * seg; env = np.clip(np.minimum((t - s0 + 1.5) / 2.5, (s0 + seg + 1.5 - t) / 2.5), 0, 1)
        for semi in ch:
            f = root * 2 ** (semi / 12)
            out += env * (np.sin(2 * np.pi * f * t) * 0.5 + np.sin(2 * np.pi * f * 2.003 * t) * bright + np.sin(2 * np.pi * f * 0.5 * t) * 0.18) * (0.6 + 0.4 * np.sin(2 * np.pi * lfo * t + f))
    out *= 0.05
    bell = [root * 2 ** (s / 12) * 4 for s in rnd.sample([0, 3, 5, 7, 10, 12, 14], 3)]
    for s in scene_starts:
        k = (t >= s); tt = (t - s)[k]
        out[k] += sum(np.sin(2 * np.pi * f * tt) for f in bell) * np.exp(-tt * 2.2) * 0.06
    for dl, g in ((0.11, .35), (0.23, .25), (0.37, .18), (0.53, .12)):
        d = int(dl * sr); out[d:] += out[:-d] * g
    fade = np.minimum(1, np.minimum(t / 1.0, (total - t) / 1.5)); out *= fade
    out = out / max(1e-6, np.abs(out).max()) * 0.6
    st = np.stack([out, np.roll(out, 300)], 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes())

def main():
    data = json.load(open(sys.argv[1], encoding='utf-8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    bg = background(); scenes = build(data)
    if '--frames' in sys.argv:
        gt = 0
        for i, sc in enumerate(scenes):
            frame(bg, sc, sc[0] - 0.6, gt + sc[0] - 0.6).save(f'{out}/check_{i}.jpg', quality=90); gt += sc[0]
        return
    files = []; gt = 0; starts = []
    for i, sc in enumerate(scenes):
        starts.append(gt); dur = sc[0]; nf = int(round(dur * FPS))
        tmp = f'{out}/s{i}.tmp.mp4'; fin = f'{out}/s{i}.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
        for k in range(nf):
            p.stdin.write(frame(bg, sc, k / FPS, gt + k / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0; os.replace(tmp, fin); files.append(fin); gt += dur
    with open(f'{out}/list.txt', 'w') as f:
        for fn in files: f.write(f"file '{os.path.abspath(fn)}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{out}/list.txt', '-c', 'copy', f'{out}/video.mp4'], check=True)
    audio(gt, starts, f'{out}/music.wav', data.get('seed', 0))
    final = f'{out}/{data["name"]}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{out}/video.mp4', '-i', f'{out}/music.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', final + '.tmp.mp4'], check=True)
    os.replace(final + '.tmp.mp4', final); print(final, gt)

if __name__ == '__main__':
    main()
