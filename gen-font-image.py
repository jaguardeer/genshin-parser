import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2 as cv
import time

# note: font from https://www.dafontfree.io/genshin-impact-font/
## load font
fontpath = "./zh-cn.ttf"     
font = ImageFont.truetype(fontpath, 32)

## text config
text = "Energy Recharge+4.7%"
## colors are in BGR order
grey = (92, 77, 71)
cream = (215, 228, 233)
bgColor_BGR = cream
fgColor_BGR = grey

## create canvas
box = font.getbbox(text)
img = np.full((box[3], box[2], 3), bgColor_BGR, np.uint8)
img_pil = Image.fromarray(img)

## draw text
draw = ImageDraw.Draw(img_pil)
draw.text((0, 0), text, font = font, fill = fgColor_BGR)
img = np.array(img_pil)

## (WIP) resize to fit game text
scale = 19.5/25
img = cv.resize(img, None, fx = scale, fy = scale)

## display and write file
imgName = "test-template"
cv.imshow(imgName, img);cv.waitKey();cv.destroyAllWindows()
cv.imwrite(f"{imgName}.png", img)