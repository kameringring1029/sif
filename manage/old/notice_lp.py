#!/usr/bin/python
# -*- coding: utf-8 -*- 
  
import MySQLdb
import time
from datetime import datetime
import os, sys
import tweepy
 
time_format="%Y-%m-%d %H:%M:%S"


################
## POST TWEET ##
################
def post_tweet(message):
	#認証を行う
	consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
	consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
	access_token="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
	access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	
	#Hello, world!と投稿する
	api.update_status(message)

	


##########
## main ##
##########
if __name__ == "__main__":

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()


	sql = "select * from status where time=(select max(time) from status)"
	print "[SQL]:"+sql
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		db_time, rank, lp_now, lp_max, exp_now, exp_max, pop_flag = row
		if pop_flag == 1:
			message = str(datetime.now())+" LP:"+str(lp_max)+"/"+str(lp_max)+"(max)"
			post_tweet(message)
			print "[Tweet]POST:"+message
			sys.exit()
		else:
			timediff = int(time.mktime(datetime.now().timetuple())) - int(time.mktime(db_time.timetuple()))
			restore_lp = timediff / 60 / 6
			realtime_lp = lp_now + restore_lp
			if realtime_lp >= lp_max:
				message = "@nigt_liliwh575 "+str(datetime.now())+" LP overflow!"
				post_tweet(message)
				print "[Tweet]POST:"+message
				sql = "update status set notice_flag=1 order by time desc limit 1"
				print "SQL:"+sql
				cursor.execute(sql)
			else:
				message = str(datetime.now())+" LP:"+str(realtime_lp)+"/"+str(lp_max)
				post_tweet(message)
				print "[Tweet]POST:"+message
				

	connector.commit()
	cursor.close()
	connector.close()


