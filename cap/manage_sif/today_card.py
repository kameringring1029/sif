#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta

import os, sys
import MySQLdb
import time
import datetime
import random
import re
import commands

time_format="%Y-%m-%d %H:%M:%S"


import usetwitter
import usecv
import usesql
import useburp
import points


def get_rare(pattern):
	rand = random.randint(0,99)

	if pattern == "alpaca":
		if rand > 90:
			rarity = 2
		else :
			rarity = 1
	else:
		if rand == 99:
			rarity = 4
		elif rand > 94:
			rarity = 3
		elif rand > 84:
			rarity = 2
		else :
			rarity = 1

	return rarity


def get_names(request):

	unit = str(request.encode('utf-8'))
	print unit

	if (unit.find('μ') > -1)or(unit.find('muse') > -1):
		if (unit.find('1') > -1) or (unit.find('一') > -1):
			return ('星空凛','西木野真姫','小泉花陽')
		if (unit.find('2') > -1) or (unit.find('二') > -1):
			return ('高坂穂乃果','南ことり','園田海未')
		if (unit.find('3') > -1) or (unit.find('三') > -1):
			return ('絢瀬絵里','東條希','矢澤にこ')
		return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ')
	if (unit.find('Printemps') > -1)or(unit.find('printemps') > -1)or(unit.find('プランタン') > -1)or(unit.find('ぷらんたん') > -1):
		return ('高坂穂乃果','南ことり','小泉花陽')
	if (unit.find('lily') > -1)or(unit.find('リリホワ') > -1):
		return ('園田海未','星空凛','東條希')
	if (unit.find('BiBi') > -1)or(unit.find('bibi') > -1)or(unit.find('Bibi') > -1)or(unit.find('ビビ') > -1):
		return ('絢瀬絵里','西木野真姫','矢澤にこ')
	if (unit.find('にこりんぱな') > -1):
		return ('星空凛','小泉花陽','矢澤にこ')

	if (unit.find('Aqours') > -1) or (unit.find('aqours') > -1)or (unit.find('アクア') > -1)or (unit.find('あくあ') > -1):
		if (unit.find('1') > -1) or (unit.find('一') > -1):
			return ('津島善子','国木田花丸','黒澤ルビィ')
		if (unit.find('2') > -1) or (unit.find('二') > -1):
			return ('高海千歌','桜内梨子','渡辺曜')
		if (unit.find('3') > -1) or (unit.find('三') > -1):
			return ('松浦果南','黒澤ダイヤ','小原鞠莉')
		return ('高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')
	if (unit.find('cyaron') > -1)or(unit.find('CYaRon') > -1)or(unit.find('シャロン') > -1)or(unit.find('しゃろん') > -1):
		return ('高海千歌','渡辺曜','黒澤ルビィ')
	if (unit.find('AZALEA') > -1)or(unit.find('azalea') > -1)or(unit.find('アゼリア') > -1)or(unit.find('あぜりあ') > -1):
		return ('松浦果南','黒澤ダイヤ','国木田花丸')
	if (unit.find('Kiss') > -1)or(unit.find('kiss') > -1)or(unit.find('キス') > -1)or(unit.find('きす') > -1):
		return ('桜内梨子','津島善子','小原鞠莉')

	if (unit.find('穂乃果') > -1)or(unit.find('ほのか') > -1):
		return ('高坂穂乃果')
	if (unit.find('絵里') > -1)or(unit.find('えり') > -1)or(unit.find('エリーチカ') > -1)or(unit.find('エリチカ') > -1):
		return ('絢瀬絵里')
	if (unit.find('ことり') > -1):
		return ('南ことり')
	if (unit.find('海未') > -1)or(unit.find('うみ') > -1):
		return ('園田海未')
	if (unit.find('凛') > -1)or(unit.find('りん') > -1):
		return ('星空凛')
	if (unit.find('真姫') > -1)or(unit.find('まき') > -1)or(unit.find('マッキー') > -1):
		return ('西木野真姫')
	if (unit.find('希') > -1)or(unit.find('のぞみ') > -1)or(unit.find('ノゾー') > -1)or(unit.find('のんたん') > -1):
		return ('東條希')
	if (unit.find('花陽') > -1)or(unit.find('はなよ') > -1)or(unit.find('ぱな') > -1):
		return ('小泉花陽')
	if (unit.find('にこ') > -1):
		return ('矢澤にこ')

	if (unit.find('千歌') > -1)or(unit.find('ちか') > -1)or(unit.find('チカ') > -1):
		return ('高海千歌')
	if (unit.find('梨子') > -1)or(unit.find('りこ') > -1):
		return ('桜内梨子')
	if (unit.find('果南') > -1)or(unit.find('かなん') > -1):
		return ('松浦果南')
	if (unit.find('ダイヤ') > -1)or(unit.find('だいや') > -1):
		return ('黒澤ダイヤ')
	if (unit.find('曜') > -1)or(unit.find('よう') > -1):
		return ('渡辺曜')
	if (unit.find('善子') > -1)or(unit.find('よしこ') > -1)or(unit.find('ヨハネ') > -1):
		return ('津島善子')
	if (unit.find('花丸') > -1)or(unit.find('まる') > -1)or(unit.find('マル') > -1):
		return ('国木田花丸')
	if (unit.find('鞠莉') > -1)or(unit.find('まり') > -1)or(unit.find('マリー') > -1):
		return ('小原鞠莉')
	if (unit.find('ルビィ') > -1)or(unit.find('るびぃ') > -1):
		return ('黒澤ルビィ')

	if (unit.find('アルパカ') > -1):
		return ('アルパカ')

	return ('高坂穂乃果','絢瀬絵里','南ことり','園田海未','星空凛','西木野真姫','東條希','小泉花陽','矢澤にこ','高海千歌','桜内梨子','松浦果南','黒澤ダイヤ','渡辺曜','津島善子','国木田花丸','小原鞠莉','黒澤ルビィ')

def get_oauth():
	# 以下4つのキー等は適宜取得して置き換えてください。
	consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
	consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
	access_key="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
	access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth


if __name__ == '__main__':
	auth = get_oauth()
	# インスタンス生成
	useTwitter = usetwitter.UseTwitter()
	useCV = usecv.UseCV()
	useBurp = useburp.UseBurp()
	useSQL = usesql.UseSQL()
	point = points.Points()

	if random.randint(0,100) < 20:
		rarity = 4
	else:
		rarity = 2

	(member_info, fullimg_0, fullimg_1) = useSQL.get_member_info(useSQL.rand_member(rarity, get_names(''), 0))

	filename_0 = '/home/pi/sif/cap/manage_sif/fullimg_0.jpg'
	command = "wget '"+str(fullimg_0)+"' -O "+filename_0
	check = commands.getoutput(command)
	filename_1 = '/home/pi/sif/cap/manage_sif/fullimg_1.jpg'
	command = "wget '"+str(fullimg_1)+"' -O "+filename_1
	check = commands.getoutput(command)

	useCV.create_member_image(filename_0, filename_1)

	member_info = "【今日のSR/UR勧誘】\n" + member_info + "\n#スクフェス"

	print member_info

	useTwitter.post_tweet_image(0,member_info,'/home/pi/sif/cap/manage_sif/fullimg_merge.jpg')

	print "today_card.py end\n"



