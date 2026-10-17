"""Outils communs pour les visuels promo (TikTok, Instagram, Pinterest)."""
import json, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

FONT_B = 'ArchivoBlack.ttf'; FONT_7 = 'Archivo-700.ttf'; FONT_5 = 'Archivo-500.ttf'; FONT_I = 'FrauncesIt.ttf'
PAL = {1: (214, 40, 40), 2: (27, 94, 32), 3: (124, 179, 66), 4: (109, 76, 65), 5: (253, 216, 53), 6: (251, 140, 0),
       7: (129, 212, 250), 8: (26, 35, 126), 9: (244, 143, 177), 10: (215, 184, 153), 11: (158, 158, 158), 12: (33, 33, 33)}

def font(f, s):
    return ImageFont.truetype(f, s)

def front_cover(pdf, pages, out, dpi=160):
    spine = pages * 0.002252
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', '-singlefile', pdf, '/tmp/cov'], check=True)
    im = Image.open('/tmp/cov.png').convert('RGB')
    x0 = int((0.125 + 8.5 + spine) * dpi); y0 = int(0.125 * dpi)
    im.crop((x0, y0, x0 + int(8.5 * dpi), y0 + int(11 * dpi))).save(out)
    return out

def mockup(cover_path, height):
    """Couverture avec ombre portée et léger reflet, fond transparent."""
    c = Image.open(cover_path).convert('RGB')
    w = int(c.width * height / c.height); c = c.resize((w, height), Image.LANCZOS)
    pad = int(height * 0.06)
    canvas = Image.new('RGBA', (w + 2 * pad, height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((pad + 10, pad + 16, pad + w + 10, pad + height + 16), fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(pad // 3))
    canvas.alpha_composite(sh)
    canvas.paste(c, (pad, pad))
    # tranche reliure
    d = ImageDraw.Draw(canvas)
    for i in range(10):
        d.line([(pad + i, pad), (pad + i, pad + height)], fill=(0, 0, 0, int(60 - i * 6)))
    return canvas

def mosaic_assets(b):
    """Renvoie (sol RGB, image numérotée RGB, régions [(couleur, masque bool)]) à la résolution de sol."""
    sol = Image.open(f'cache/{b}_sol.png').convert('RGB')
    edge = Image.open(f'cache/{b}_edge.png').convert('L').resize(sol.size, Image.LANCZOS)
    k = sol.size[0] / Image.open(f'cache/{b}_edge.png').size[0]
    arr = np.asarray(sol).astype(int)
    keys = np.array([PAL[i] for i in range(1, 13)] + [(255, 255, 255)])
    d = ((arr[:, :, None, :] - keys[None, None, :, :]) ** 2).sum(-1)
    lab = d.argmin(-1) + 1; lab[lab == 13] = 0
    e = np.asarray(edge) < 140
    regions = []
    for c in range(1, 13):
        m = (lab == c) & ~e
        cc, n = ndimage.label(m)
        for sl_i, sl in enumerate(ndimage.find_objects(cc), 1):
            if sl is None: continue
            mm = np.zeros(m.shape, bool); mm[sl] = cc[sl] == sl_i
            if mm.sum() < 6: continue
            regions.append((c, mm))
    num = Image.new('RGB', sol.size, 'white')
    num.paste((60, 60, 60), mask=Image.fromarray((e * 255).astype(np.uint8)))
    dn = ImageDraw.Draw(num)
    for x, y, r, col in json.load(open(f'cache/{b}.json')):
        if col == 0: continue
        fs = max(8, min(15, int(r * k * 1.05)))
        dn.text((x * k, y * k), str(col), fill=(110, 110, 110), font=font(FONT_5, fs), anchor='mm')
    # sol avec traits
    sol_l = sol.copy(); sol_l.paste((40, 40, 40), mask=Image.fromarray((e * 255).astype(np.uint8)))
    return sol_l, num, regions, e

def text_center(d, W, y, txt, f, fill, stroke=0, sfill=None, spacing=8):
    d.multiline_text((W // 2, y), txt, font=f, fill=fill, anchor='ma', align='center',
                     stroke_width=stroke, stroke_fill=sfill, spacing=spacing)

def write_video(frames_iter, out, fps=30, W=1080, H=1920):
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
                          '-s', f'{W}x{H}', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                          '-crf', '20', '-preset', 'medium', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for fr in frames_iter:
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
