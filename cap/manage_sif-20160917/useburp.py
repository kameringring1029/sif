#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import os, sys
import time
import datetime

import usetwitter

time_format="%Y-%m-%d %H:%M:%S"


class UseBurp:


	##############################
	##  ##
	##############################
	def read_burplog(self, points):
		print "read_burplog\n"
	
		#現在時刻の取得と整形
		localtime = time.strftime(time_format)
		localtime = time.strftime(time_format, time.localtime())
		
		## point情報読み込みとDB更新
		f = open('/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_challenge_finalize.json', 'r')
		jsonData = json.load(f)['response_data']

		points.setRank(jsonData['after_user_info']['level'])
		points.setLpmax(jsonData['after_user_info']['energy_max'])
		points.setLpmaxtime(jsonData['after_user_info']['energy_full_time'])
		points.setExpnow(jsonData['after_user_info']['exp'])
		points.setExpmax(jsonData['after_user_info']['next_exp'])
		points.setLoveca(jsonData['after_user_info']['sns_coin'])
			
		points.setEventpoint(jsonData['event_info']['event_point_info']['after_total_event_point'])
	
		f.close	

#		print json.dumps(jsonData, sort_keys = True, indent = 4)

	

	def gatcha_bot(self, useSQL):
		print "gatcha_bot\n"

		f = open('/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_secretbox_pon.json', 'r')
		jsonData = json.load(f)['response_data']['secret_box_items']['unit'][0]['unit_id']

		tweet = "[勧誘報告BOT]\n" + useSQL.get_member(str(jsonData)) + " をてにいれた！"
		print "tweet:"+tweet
		usetwitter.UseTwitter().post_tweet(tweet)

		f.close	

