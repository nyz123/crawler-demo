# -*- coding: utf-8 -*-
from PIL import Image
from random import randint
 
old = Image.open(r"da.jpg")
new = Image.new('L', old.size, 255)
w, d = old.size
old = old.convert('L')
PEN_SIZE = 3
COLOR_DIFF = 7
LINE_LEN = 2
 
for i in range(PEN_SIZE + 1, w - PEN_SIZE - 1):
  for j in range(PEN_SIZE + 1, d - PEN_SIZE - 1):
    originalcolor = 255
    lcolor = sum([old.getpixel((i - r, j))
           for r in range(PEN_SIZE)]) // PEN_SIZE
    rcolor = sum([old.getpixel((i + r, j))
           for r in range(PEN_SIZE)]) // PEN_SIZE
    if abs(lcolor - rcolor) > COLOR_DIFF:
      originalcolor -= (255 - old.getpixel((i, j))) // 4
      for p in range(-LINE_LEN + randint(-1, 1), LINE_LEN + randint(-1, 1)):
        new.putpixel((i, j + p), originalcolor)
 
    ucolor = sum([old.getpixel((i, j - r))
           for r in range(PEN_SIZE)]) // PEN_SIZE
    dcolor = sum([old.getpixel((i, j + r))
           for r in range(PEN_SIZE)]) // PEN_SIZE
    if abs(ucolor - dcolor) > COLOR_DIFF:
      originalcolor -= (255 - old.getpixel((i, j))) // 4
      for p in range(-LINE_LEN + randint(-1, 1), LINE_LEN + randint(-1, 1)):
        new.putpixel((i + p, j), originalcolor)
 
    lucolor = sum([old.getpixel((i - r, j - r))
            for r in range(PEN_SIZE)]) // PEN_SIZE
    rdcolor = sum([old.getpixel((i + r, j + r))
            for r in range(PEN_SIZE)]) // PEN_SIZE
    if abs(lucolor - rdcolor) > COLOR_DIFF:
      originalcolor -= (255 - old.getpixel((i, j))) // 4
      for p in range(-LINE_LEN + randint(-1, 1), LINE_LEN + randint(-1, 1)):
        new.putpixel((i - p, j + p), originalcolor)
 
    rucolor = sum([old.getpixel((i + r, j - r))
            for r in range(PEN_SIZE)]) // PEN_SIZE
    ldcolor = sum([old.getpixel((i - r, j + r))
            for r in range(PEN_SIZE)]) // PEN_SIZE
    if abs(rucolor - ldcolor) > COLOR_DIFF:
      originalcolor -= (255 - old.getpixel((i, j))) // 4
      for p in range(-LINE_LEN + randint(-1, 1), LINE_LEN + randint(-1, 1)):
        new.putpixel((i + p, j + p), originalcolor)
 
new.save(r"pencil_drawing.jpg")