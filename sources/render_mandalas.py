import cairosvg, sys
from mandala_gen import render
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    cairosvg.svg2png(bytestring=render(s).encode(), write_to=f'mcache/m{s:02d}.png', output_width=2250)
    cairosvg.svg2png(bytestring=render(s, True, True).encode(), write_to=f'mcache/m{s:02d}c.png', output_width=900)
