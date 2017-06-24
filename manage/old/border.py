#!/usr/bin/python
# -*- coding: utf-8 -*- 
  
import MySQLdb
import time
from datetime import datetime
import os, sys
import tweepy
 
time_format="%Y-%m-%d %H:%M:%S"


################
## GET BORDER ##
################
def get_border():
	#認証を行う
	consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
	consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
	access_token="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
	access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	
	tweet = api.user_timeline("llborder_update")[0].text
	line = tweet.split("\n")
	double = line[1].split(u'：')[1].split("pts")[0]
	single = line[2].split(u'：')[1].split("pts")[0]
	time = line[3].split(u'：')[1].split(" (")[0]

	if tweet != '':
		return [time, double, single]
	else:
		return [0, 0, 0]


############################
## イベントborder参照関数 ##
############################
def show_Table(event):

	try:

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		event_name = event

	
 		##select
		sql = "select * from " + event_name
		print "[SQL]"+sql
		cursor.execute(sql)
		result = cursor.fetchall()
		print "+-------------------------------------+"
		for row in result:
			if event == "status_test":
				print "| "+str(row[0])+", RANK:"+str(row[1])+", LP:"+str(row[2])+"/"+str(row[3])+", EXP:"+str(row[4])+"/"+str(row[5])+", POP:"+str(row[6])+" |"
			else:
				print "| "+str(row[0])+", "+str(row[1])+", "+str(row[2])+" |"
		print "+-------------------------------------+"

		## DB commit and close
		connector.commit()
		cursor.close()
		connector.close()


	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)


	


##########
## main ##
##########
if __name__ == "__main__":

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()

	event_name = "cf2_border"

	#現在時刻の取得と整形
	localtime = time.strftime(time_format)
	localtime = time.strftime(time_format, time.localtime())
	
	time, double, single = get_border()

	print time+"/"+double+"/"+single

	sql = "insert into "+event_name+" values('"+localtime+"',"+double+","+single+")"
	print "[SQL]:"+sql
	cursor.execute(sql)


	connector.commit()
	cursor.close()
	connector.close()

	show_Table(event_name)


