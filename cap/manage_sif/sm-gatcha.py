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

time_format="%Y-%m-%d %H:%M:%S"


import usetwitter
import usecv
import usesql
import useburp
import usegatcha
import points


api = Flask(__name__)

@api.route('/test/<string:desc>', methods=['GET'])
def do_gatcha(desc):

    smGatcha = smgatcha()
    members = smGatcha.dogatcha("@test "+desc)

    result = {
        "result":True,
        "data":{
            "userId":desc,
            "members":members,
			"url":"http://koke.link/test/result.jpg"
            }
        }

    return make_response(jsonify(result))
    # UnicodeÉµ½­È¢êÍ«
    # return make_response(json.dumps(result, ensure_ascii=False))

@api.errorhandler(404)
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
		members = '['

		for num in range(0,11):

			members = members + "{"

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


			member_id = 30
			while member_id > 27 and member_id < 52:

				series = 0
				if rarity > 1:
					print str(desc.rsplit(' ',1)[1].encode('utf-8'))
					series = str(desc.rsplit(' ',1)[1].encode('utf-8'))
					if not('編' in series):
						series = 0

				member_id = self.useSQL.rand_member(rarity,names,series)
			(member_name, member_url) = self.useSQL.get_member(member_id)
			(member_info, member_fullimgurl_0, member_fullimgurl_1) = self.useSQL.get_member_info(member_id)

			members = members + '"id":"' + str(member_id) +'",'
			members = members + '"name":"' + str(member_name) +'",'
			members = members + '"fullimgurl_0":"' + str(member_fullimgurl_0) +'",'
			members = members + '"fullimgurl_1":"' + str(member_fullimgurl_1) +'",'
			members = members + '"info":"' + member_info +'"'

			filename = '/home/pi/sif/cap/manage_sif/icon'+str(num)+'.gif'
			command = "wget '"+str(member_url)+"' -O "+filename
			check = commands.getoutput(command)

#			print check
			icons.insert(num,filename+" "+str(rarity))

			if num == 10:
				members = members + "}"
			else:
				members = members + "},"

		members = members + "]"
		print "members:"+members


		self.useCV.create_gacha_image(icons)

		return members


		#self.useTwitter.post_tweet_image(status.id,tweet,'/home/pi/sif/cap/manage_sif/result.jpg')


if __name__ == '__main__':

    api.run(host='0.0.0.0', port=3000)

    print "end smgatcha"


