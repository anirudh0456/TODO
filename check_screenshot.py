import sys
from PIL import Image
im = Image.open(sys.argv[1]).convert("L"); px = list(im.getdata()); n = len(px)
dark = sum(1 for p in px if p < 15) / n; mean = sum(px) / n; var = sum((p - mean) ** 2 for p in px) / n
print(f"size={im.size} dark_fraction={dark:.3f} mean={mean:.1f} std={var ** .5:.1f}")
if dark > 0.97 or var ** .5 < 5: print("FAIL: screen looks blank/black"); sys.exit(1)
print("OK: screen has visible content")
