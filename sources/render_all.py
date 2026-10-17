import glob, json, os, sys, numpy as np
from PIL import Image
import mosaic
for f in sorted(glob.glob('mosa/*.svg')):
    b = os.path.basename(f)[:-4]
    if os.path.exists(f'cache/{b}.json'): continue
    e, mk, lab, cells, co = mosaic.render(f)
    Image.fromarray(np.where(e, 70, 255).astype(np.uint8)).save(f'cache/{b}_edge.png', dpi=(300, 300))
    mosaic.preview(cells, co, e, f'cache/{b}_sol.png')
    json.dump([[int(x), int(y), float(r), int(c)] for x, y, r, c in mk], open(f'cache/{b}.json', 'w'))
    print(b, len(mk), flush=True)
