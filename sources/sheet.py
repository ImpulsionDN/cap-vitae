import sys, glob, io, cairosvg
from PIL import Image, ImageDraw
fs = sorted(glob.glob('mosa/*.svg'))
if len(sys.argv) > 2: fs = [f for f in fs if sys.argv[2] <= f.split('/')[-1][:2] <= sys.argv[3]]
ims = [Image.open(io.BytesIO(cairosvg.svg2png(url=f, output_width=240, output_height=256))) for f in fs]
cols = 6; rows = (len(ims) + cols - 1) // cols
M = Image.new('RGB', (cols * 250, rows * 280), 'white'); d = ImageDraw.Draw(M)
for i, (f, im) in enumerate(zip(fs, ims)):
    x, y = (i % cols) * 250, (i // cols) * 280
    M.paste(im, (x, y)); d.text((x + 4, y + 260), f.split('/')[-1], fill='black')
M.save(sys.argv[1])
