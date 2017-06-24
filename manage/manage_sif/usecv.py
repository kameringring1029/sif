#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import cv2
import numpy as np
import commands


class UseCV:

	################
	## 色抽出関数 ##
	################
	def extract_color(self, src, h_th_low, h_th_up, s_th, v_th ):

		hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
		h, s, v = cv2.split(hsv)

		if h_th_low > h_th_up:
			ret, h_dst_1 = cv2.threshold(h, h_th_low, 255, cv2.THRESH_BINARY) 
			ret, h_dst_2 = cv2.threshold(h, h_th_up,  255, cv2.THRESH_BINARY_INV)
		
			dst = cv2.bitwise_or(h_dst_1, h_dst_2)

		else:
			ret, dst = cv2.threshold(h,   h_th_low, 255, cv2.THRESH_TOZERO) 
			ret, dst = cv2.threshold(dst, h_th_up,  255, cv2.THRESH_TOZERO_INV)

			ret, dst = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY)
		
		ret, s_dst = cv2.threshold(s, s_th, 255, cv2.THRESH_BINARY)
		ret, v_dst = cv2.threshold(v, v_th, 255, cv2.THRESH_BINARY)

		dst = cv2.bitwise_and(dst, s_dst)
		dst = cv2.bitwise_and(dst, v_dst)

		return dst




	##############################
	## イベントスクショ解析関数 ##
	##############################
	def analyze_eventSC(self, filename):
		print "analyze_eventSC"
	
		image = cv2.imread(os.path.join('/var/www/up/', filename))
	
		height_orig = image.shape[0]
		width_orig = image.shape[1]

		## ポイント記載部分トリミング
		trim_image = image[height_orig*0.77:height_orig*0.81, width_orig*0.15:width_orig*0.27]
		cv2.imwrite(os.path.join('/var/www/up/', 'trim_point.png'), trim_image)
		## ピンクで２値化（累計ポイント取得用）
		if height_orig > 900:
			pink_image = self.extract_color(trim_image, 160,  0, 80,  232)
		else:
			pink_image = self.extract_color(trim_image, 160,  0, 100,  3)
		cv2.imwrite(os.path.join('/var/www/up/', 'pink_image.png'), pink_image)
		commands.getoutput("tesseract /var/www/up/pink_image.png /var/www/up/now -psm 7 nobatch digits")


		## item用ネガポジ解析
		look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
		for i in range(256):
				look_up_table[i][0] = 255 - i
		## item記載部分トリミング
	#	trim_image = image[870:920, 350:500]
		trim_image = image[height_orig*0.807:height_orig*0.853, width_orig*0.215:width_orig*0.306]
		img_negaposi = cv2.LUT(trim_image, look_up_table)

	    # グレースケールに変換
		gray_image = cv2.cvtColor(img_negaposi, cv2.COLOR_BGR2GRAY)
		 
		# 二値変換
		thresh = 250
		max_pixel = 255
		ret, gray_image = cv2.threshold(gray_image,thresh,max_pixel,cv2.THRESH_BINARY)

		cv2.imwrite(os.path.join('/var/www/up/', 'trim_image.png'), trim_image)
		cv2.imwrite(os.path.join('/var/www/up/', 'gray_image.png'), gray_image)
		commands.getoutput("tesseract /var/www/up/gray_image.png /var/www/up/item -psm 7 nobatch digits")




	########################
	## ゲーム画面切取関数 ##
	########################
	def trim_frame_by_SC(self,filename):
	
		image = cv2.imread(os.path.join('/var/www/up/', filename))

		## ２値化（アプリ画面枠検知用）
		apl_image = self.extract_color(image, 0,  180, 10,  10)
		cv2.imwrite(os.path.join('/var/www/up/', 'apl_image.png'), apl_image)
	
		# 輪郭を取得
		contours, hierarchy = cv2.findContours(apl_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
		# i = 1 は画像全体の外枠になるのでカウントに入れない
		x1 = []
		y1 = []
		x2 = []
		y2 = []
		for i in range(1, len(contours)):
		# ret の中身は (x, y, w, h)
			ret = cv2.boundingRect(contours[i])
			x1.append(ret[0])
			y1.append(ret[1])
			x2.append(ret[0] + ret[2])
			y2.append(ret[1] + ret[3])
	
		x1_min = min(x1)
		y1_min = min(y1)
		x2_max = max(x2)
		y2_max = max(y2)

		## トリミング
		trim_image = image[y1_min:y2_max, x1_min:x2_max]
		cv2.imwrite('/var/www/up/only_apl.jpg', trim_image)
	
	#	for j in range(0, len(x1)):
	#		cv2.rectangle(image, (x1[j], y1[j]), (x2[j], y2[j]), (0, 255, 0), 2)
	
	


	########################
	## スクショLP解析関数 ##
	########################
	def analyze_LP(self,filename):
		print "analyze_LP"
	
		image = cv2.imread(os.path.join('/var/www/up/', filename))
		height_orig = image.shape[0]
		width_orig = image.shape[1]


		## ポイント記載部分トリミング
		trim_image = image[0:height_orig*0.1, width_orig*0.43:width_orig]
		cv2.imwrite(os.path.join('/var/www/up/', 'status_image.png'), trim_image)

		rank_image = image[height_orig*0.045:height_orig*0.090, width_orig*0.46:width_orig*0.54]
		cv2.imwrite(os.path.join('/var/www/up/', 'rank_image.png'), rank_image)
		commands.getoutput("tesseract /var/www/up/rank_image.png /var/www/up/rank -psm 7 nobatch digits")
		lp_image = image[height_orig*0.067:height_orig*0.099, width_orig*0.73:width_orig*0.81]
		cv2.imwrite(os.path.join('/var/www/up/', 'lp_image.png'), lp_image)
	    # グレースケールに変換
		lp_image = cv2.cvtColor(lp_image, cv2.COLOR_BGR2GRAY)
		cv2.imwrite(os.path.join('/var/www/up/', 'lp_image.png'), lp_image)
		commands.getoutput("tesseract /var/www/up/lp_image.png /var/www/up/lp -psm 7 nobatch digits")
	
		exp_image = image[height_orig*0.067:height_orig*0.099, width_orig*0.55:width_orig*0.70]
		cv2.imwrite(os.path.join('/var/www/up/', 'exp_image.png'), exp_image)
		commands.getoutput("tesseract /var/www/up/exp_image.png /var/www/up/exp -psm 7 nobatch digits")
	
	


