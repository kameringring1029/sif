#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import os, sys
import time
import datetime

import usetwitter

time_format="%Y-%m-%d %H:%M:%S"


class UseBurp:



	def getUrl(self, event):
		url = ""
		if event.find("sm") != -1:
			url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_battle_endRoom.json"
		if event.find("cf") != -1:
			url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_challenge_finalize.json"
		if event.find("mf") != -1:
			url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_festival_liveReward.json"
		if event.find("ic") != -1:
			url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_live_reward.json"
		if event.find("or") != -1:
			url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_quest_questReward.json"
		
		return url



	##############################
	##  ##
	##############################
	def read_burplog(self, points, event):
		print "read_burplog\n"

		#event="or1"
	
		#現在時刻の取得と整形
		localtime = time.strftime(time_format)
		localtime = time.strftime(time_format, time.localtime())
		
		## point情報読み込みとDB更新
		f = open(self.getUrl(event), 'r')
		jsonData = json.load(f)['response_data']

		if event.find("or") != -1:
			jsonAfterUserInfo = jsonData['live_result']['after_user_info']
		else:
			jsonAfterUserInfo = jsonData['after_user_info']

		points.setRank(jsonAfterUserInfo['level'])
		points.setLpmax(jsonAfterUserInfo['energy_max'])
		points.setLpmaxtime(jsonAfterUserInfo['energy_full_time'])
		points.setExpnow(jsonAfterUserInfo['exp'] - jsonAfterUserInfo['previous_exp'])
		points.setExpmax(jsonAfterUserInfo['next_exp'] - jsonAfterUserInfo['previous_exp'])
		points.setLoveca(jsonAfterUserInfo['sns_coin'])
	
	
		if event != "none":
			if event.find("or") != -1:
				points.setEventpoint(jsonData['event_info']['live_event_point_info']['after_total_event_point'])
			else:
				points.setEventpoint(jsonData['event_info']['event_point_info']['after_total_event_point'])
	
		f.close	


	

	def gatcha_bot(self, useSQL):
		print "gatcha_bot\n"

		f = open('/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_secretbox_pon.json', 'r')
		jsonData = json.load(f)['response_data']['secret_box_items']['unit'][0]['unit_id']

		tweet = "[勧誘報告BOT]\n" + useSQL.get_member(str(jsonData)) + " をてにいれた！"
		print "tweet:"+tweet
		usetwitter.UseTwitter().post_tweet(tweet)

		f.close	

