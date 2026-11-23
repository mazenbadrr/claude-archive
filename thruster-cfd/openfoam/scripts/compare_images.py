#!/usr/bin/env python3
"""Place two renders side by side:  compare_images.py A.png B.png out.png"""
import sys
from PIL import Image, ImageDraw
a, b, out = Image.open(sys.argv[1]), Image.open(sys.argv[2]), sys.argv[3]
labels = (sys.argv[4], sys.argv[5]) if len(sys.argv) > 5 else ("RESIN (SLA)", "PLA (FDM)")
h = max(a.height, b.height); pad = 10
c = Image.new("RGB", (a.width + b.width + pad, h + 40), "white")
c.paste(a, (0, 40)); c.paste(b, (a.width + pad, 40))
d = ImageDraw.Draw(c)
d.text((a.width // 2 - 60, 10), labels[0], fill="black")
d.text((a.width + pad + b.width // 2 - 60, 10), labels[1], fill="black")
c.save(out); print("wrote", out)
