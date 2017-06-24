#!/usr/bin/python
#coding=utf-8

import cv2
import numpy as np
from PIL import Image


def overlay_face(icons):

	# 認識対象ファイルの読み込み
	image_path = "base.jpg"
	image = cv2.imread(image_path)



	h = 58
	w = 65
	x = 0

	for i in range(0,11):
		# 上書きする画像の読み込み
		ol_imgae_path = icons[i]
		ol_image = Image.open(icons[i]+'.gif').convert('RGB').save(icons[i]+'.jpg')
		ol_image = cv2.imread(ol_imgae_path+'jpg',cv2.IMREAD_COLOR)   # アルファチャンネル(透過)も読みこむようにIMREAD_INCHANGEDを指定
		print "debug"+str(i)
		# 画像をリサイズ
		resized_ol_image = resize_image(ol_image, h, w)

		print "icon"+str(i)

		if i < 6:
			x = 20 + 72 * i
			y = 47
		if i > 5:
			x = 65 + 72 * (i - 6)
			y = 143

		# 上書きした画像の作成
		image = overlayOnPart(image, resized_ol_image, x, y)

	# 認識結果の出力
	cv2.imwrite("result.jpg", image)


def overlayOnPart(src_image, overlay_image, posX, posY):

    ol_height, ol_width = overlay_image.shape[:2]

    src_image_RGBA = cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
    overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)

    src_image_PIL=Image.fromarray(src_image_RGBA)
    overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

    src_image_PIL = src_image_PIL.convert('RGBA')
    overlay_image_PIL = overlay_image_PIL.convert('RGBA')

    tmp = Image.new('RGBA', src_image_PIL.size, (255, 255,255, 0))
    tmp.paste(overlay_image_PIL, (posX, posY), overlay_image_PIL)
    result = Image.alpha_composite(src_image_PIL, tmp)

    return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGRA)


def resize_image(image, height, width):

    org_height, org_width = image.shape[:2]

    if float(height)/org_height > float(width)/org_width:
        ratio = float(height)/org_height
    else:
        ratio = float(width)/org_width

    resized = cv2.resize(image,(int(org_height*ratio),int(org_width*ratio)))

    return resized    


if __name__ == '__main__':

	icons = []
	for i in range(0,11):
		icons.insert(i,"icon"+str(i))


	overlay_face(icons)
