import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2
import time

# note: font from https://www.dafontfree.io/genshin-impact-font/

## Make canvas and set the color
## Colors are in BGR order
grey = (92, 77, 71)
cream = (215, 228, 233)
bgColor_BGR = cream
img = np.full((200,400,3),bgColor_BGR,np.uint8)
fgColor_BGR = grey

## Use cv2.FONT_HERSHEY_XXX to write English.
text = time.strftime("%Y/%m/%d %H:%M:%S %Z", time.localtime()) 
#cv2.putText(img,  text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, fgColor_BGR, 1, cv2.LINE_AA)

## Write from font file
fontpath = "./genshin-font.ttf"     
font = ImageFont.truetype(fontpath, 32)
img_pil = Image.fromarray(img)
draw = ImageDraw.Draw(img_pil)
draw.text((5, 10),  "Energy Recharge+9.7%\nElemental Mastery+35\nDEF+5.1%\nCRIT DMG+13.2%", font = font, fill = fgColor_BGR)
img = np.array(img_pil)

## Display 
cv2.imshow("res", img);cv2.waitKey();cv2.destroyAllWindows()
cv2.imwrite("res.png", img)