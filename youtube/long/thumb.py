import sys, os
sys.path.insert(0, '..'); sys.argv = ['x', '/tmp']
import render_long as L
from PIL import Image, ImageDraw
bg = Image.fromarray(L.background()); L.stars(bg, 1); img = bg.convert('RGBA')
F = L.F; R = L.R
img = Image.alpha_composite(img, L.layer([('11:11', F(R.SERIF_B, 300), L.GOLD2, 0, 120, 1920, 'c')]))
img = Image.alpha_composite(img, L.layer([('22:22   ·   00:00   ·   12:12', F(R.SERIF_B, 110), L.CREAM, 0, 480, 1920, 'c')]))
img = Image.alpha_composite(img, L.layer([('LES 24 HEURES MIROIRS EXPLIQUÉES', F(R.SANS, 72, 700), L.GOLD, 0, 700, 1920, 'c')]))
img = Image.alpha_composite(img, L.layer([('Ce que votre ange veut vous dire', F(R.SERIF_I, 80), L.ROSE, 0, 830, 1920, 'c')]))
img.convert('RGB').resize((1280, 720), Image.LANCZOS).save('Miniature_24_heures_miroirs.jpg', quality=92)
