#!/usr/bin/env python
#-*- coding:utf-8 -*-

import commands
import time


def tap_screen(x, y):
	com = 'adb shell input tap ' + str(x) + ' ' + str(y)
	out_adb(com)
	

def swipe_screen(x1, y1, x2, y2):
	dur = 200
	com = 'adb shell input swipe ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' ' + str(dur)
	out_adb(com)


def unsleep():
	com = 'adb shell input keyevent 82'
	out_adb(com)


def return_home():
	com = 'adb shell input keyevent 3'
	out_adb(com)


def get_screenshot():
	com = 'adb shell screencap -p /sdcard/screen.png'
	out_adb(com)
	com = 'adb pull /sdcard/screen.png'
	out_adb(com)



def out_adb(com):
	commands.getoutput(com)
	print com
	time.sleep(2)


def start_live():
    #api.run(host='0.0.0.0', port=3000)

	time.sleep(5)
	tap_screen(875, 350)
	return_home()


	# スリープ解除
#	unsleep()
#	swipe_screen(40, 1000, 40, 200)

	# スクフェス起動
	tap_screen(545, 1762)
	# 一覧左上タップ
	tap_screen(121, 396)

	#~~~~~~スクフェス~~~~~~~~~~~~~~~~~~~
	# 画面が横のため座標変換

#	time.sleep(12)

	# お知らせ OK
#	tap_screen(875, 830)
	# お知らせ 終了
#	tap_screen(1645, 50)
	# ライブ
	tap_screen(875, 1050)
	# EXPERT
	tap_screen(875, 200)
	# 曲 →スクロール
	#tap_screen(1650, 500)
	# 曲 ←スクロール
	#tap_screen(200, 500)
	# 曲 決定
	tap_screen(875, 500)
	# サポート 決定
	tap_screen(875, 150)
	# ライブ OK
	tap_screen(1650, 900)



