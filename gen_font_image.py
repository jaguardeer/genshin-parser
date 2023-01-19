import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2 as cv
import time
from util import *

def main():
	# note: font from https://www.dafontfree.io/genshin-impact-font/
	## load font
	fontPath = "./zh-cn.ttf"     
	fontSize = 32
	font = ImageFont.truetype(fontPath, fontSize)
	## colors are in BGR order
	gray = (92, 77, 71)
	cream = (215, 228, 233)
	bgColor = cream
	fgColor = gray

	show(drawText("ATK", font, fgColor, bgColor))
	img = createTemplate("ATK", font, fgColor, bgColor)
	## display and write file
	show(img)
	imgName = "test-template"
	cv.imwrite(f"{imgName}.png", img)

def drawText(text, font, fgColor, bgColor):
	## create canvas
	box = font.getbbox(text)
	img = np.full((box[3], box[2], 3), bgColor, np.uint8)
	img_pil = Image.fromarray(img)
	## draw text
	draw = ImageDraw.Draw(img_pil)
	draw.text((0, 0), text, font = font, fill = fgColor)
	img = np.array(img_pil)
	return img

def binarize(img):
	grayImg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	_, binImg = cv.threshold(grayImg, 128 ,255, cv.THRESH_BINARY_INV)
	return binImg

## returns a template for use in template_match.py
def createTemplate(text, font, fgColor, bgColor):
	## gen binarized image
	textImg = drawText(text, font, fgColor, bgColor)
	binImg = binarize(textImg)

	## find bounding box
	boundBox = cv.boundingRect(binImg)
	finalImg = crop(textImg, boundBox)

	return finalImg

if __name__ == "__main__": main()
