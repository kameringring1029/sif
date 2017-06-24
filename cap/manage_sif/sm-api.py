#!/usr/bin/env python
#-*- coding:utf-8 -*-

from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from tweepy.api import API
from datetime import timedelta
from flask import Flask, jsonify, abort, make_response
import peewee

import os, sys
import MySQLdb
import time
import datetime
import random
import re
import commands

import urllib2, sys
import json

time_format="%Y-%m-%d %H:%M:%S"


import usetwitter
import usecv
import usesql
import useburp
import usegatcha
import useadb
import points


api = Flask(__name__)

########
# for alarm 
#######
@api.route('/alarm/<string:desc>', methods=['GET'])
def alarm(desc):

	useadb.start_live()


def get_weather(desc):

	citycode = 130010
	resp = urllib2.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
	resp = json.loads(resp)

	if desc == "telop":
		return resp['forecasts'][0]['telop']
	if desc == "tempmin":
		if not isinstance(resp['forecasts'][0]['temperature']['min'], type(None)):
			return resp['forecasts'][0]['temperature']['min']['celsius'] 
	if desc == "tempmax":
		if not isinstance(resp['forecasts'][0]['temperature']['max'], type(None)):
			return resp['forecasts'][0]['temperature']['max']['celsius'] 

	return "-"




########
# for event 
#######
@api.route('/event/<string:desc>', methods=['GET'])
def get_eventinfo(desc):

	event = "sm32"

	print event

	useSQL = usesql.UseSQL()
	mine_list = useSQL.get_points(event)
	border_list = useSQL.get_points(event+"_border")

	status_list = useSQL.get_latest_status()

	result = {
		"result":True,
		"data":{
			"userId":"userid",
			"members":"members",
			"url":"http://koke.link/test/result.jpg"
		},
		"status":{
			"rank":status_list[1],
			"lp_now":status_list[2],
			"lp_max":status_list[3],
			"exp_now":status_list[4],
			"exp_max":status_list[5],
		},
		"points":{
			"mine":mine_list,
			"border":border_list,
			"eventname":event
		},
		"weather":{
			"today":get_weather("telop"),
			"today_temp_min":get_weather("tempmin"),
			"today_temp_max":get_weather("tempmax")
		}
	}

	return make_response(jsonify(result))
	# UnicodeÉµ½­È¢êÍ«
	# return make_response(json.dumps(result, ensure_ascii=False))



########
# for gatcha
#######
@api.route('/unity/<string:desc>', methods=['GET'])
def do_gatcha(desc):

    smGatcha = smgatcha()
    members = smGatcha.dogatcha("@test "+desc)


    result = {
            "members":[members[0],members[1],members[2],members[3],members[4],members[5],members[6],members[7],members[8],members[9],members[10]]
        }

    return make_response(jsonify(result))
    # UnicodeÉµ½­È¢êÍ«
    # return make_response(json.dumps(result, ensure_ascii=False))


api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)




class smgatcha:
	""" Let's stare abstractedly at the User Streams ! """
	# インスタンス生成
	useTwitter = usetwitter.UseTwitter()
	useCV = usecv.UseCV()
	useBurp = useburp.UseBurp()
	useSQL = usesql.UseSQL()
	useGatcha = usegatcha.UseGatcha()
	point = points.Points()

	def dogatcha(self, desc):
		# Ubuntuの時は気づかなかったんだけど、Windowsで動作確認してたら
		# created_atはUTC（世界標準時）で返ってくるので日本時間にするために9時間プラスする。

		dobu = 1
		UR_flug = 1
		SR_flug = 1

		icons = []
		membersArray = []

		for num in range(0,11):

			members = {}

			names = self.useGatcha.get_names(desc)
			if isinstance(names, str):
				if names.find("アルパカ"):
					rarity = self.useGatcha.get_rare("alpaca")
			else:
				rarity = self.useGatcha.get_rare("normal")

			if (desc.find('UR') > -1)and(rarity==1)and(random.randint(0,1)):
				rarity = 4
			if (desc.find('SR') > -1)and(rarity==1)and(random.randint(0,1)):
				rarity = 3

			if rarity > 1:
				dobu = 0
			elif (dobu == 1) and (num == 10):
			## SR確定
				rarity = 2
				dobu = 0


		#	member_id = 30
		#	while member_id > 27 and member_id < 52:

			series = 0
			if rarity > 1:
				print str(desc.rsplit(' ',1)[1].encode('utf-8'))
				series = str(desc.rsplit(' ',1)[1].encode('utf-8'))
				if not('編' in series):
					series = 0

			member_id = self.useSQL.rand_member(rarity,names,series)
			(member_rare, member_name, member_series, member_url) = self.useSQL.get_member(member_id)
			(member_info, member_fullimgurl_0, member_fullimgurl_1) = self.useSQL.get_member_info(member_id)
			if (member_name != 'アルパカ' and member_rare == 'R') or (member_name == 'アルパカ' and member_rare == 'SR'):
				member_desc = member_rare + member_name
			else:
				member_desc = member_rare + member_name + "(" + member_series + ")"


			members["id"] = str(member_id)
			members["rarity"] = str(rarity)
			members["name"] = str(member_name)
			members["series"] = str(member_series)
			members["desc"] = str(member_desc)
			members["fullimgurl_0"] = str(member_fullimgurl_0)
			members["fullimgurl_1"] = str(member_fullimgurl_1)
			members["info"] = str(member_info)

			filename = '/home/pi/sif/cap/manage_sif/icon'+str(num)+'.gif'
			command = "wget '"+str(member_url)+"' -O "+filename
#			check = commands.getoutput(command)

#			print check
			icons.insert(num,filename+" "+str(rarity))

			if num < 11:
				membersArray.insert(num, members)

		#members = members + "]"
		# print "members:"+members[num]


	#	self.useCV.create_gacha_image(icons)

		return membersArray


		#self.useTwitter.post_tweet_image(status.id,tweet,'/home/pi/sif/cap/manage_sif/result.jpg')


if __name__ == '__main__':

	print "start sm-api"
	
#	api.run(host='0.0.0.0', port=3000)
	api.run(host='192.168.100.103', port=3000)

	print "end sm-api"


