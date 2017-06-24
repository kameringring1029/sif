#!/usr/bin/python
# -*- coding: utf-8 -*-


html_result =""
time_tweet =""

import cgi
import os, sys
import cv2
import numpy as np
import commands
import MySQLdb
import time
import datetime
import tweepy
import urllib

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
	
	#投稿する
	api.update_status(message)


##################
## GET TWEET SC ##
##################
def get_tweet_sc():
	global time_tweet

	#認証を行う
	consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
	consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
	access_token="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
	access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	
	if api.home_timeline()[0].text.find('@sif_notify_bot') != -1 :
		tweetimage = api.home_timeline()[0].entities['media'][0]['media_url'] + ":orig"
		time_tweet = api.home_timeline()[0].created_at
		time_tweet += datetime.timedelta(hours = 9)
		time_tweet = time_tweet.strftime(time_format)

		print time_tweet

		filename = 'tweetsc.jpg'

		urllib.urlretrieve(tweetimage, os.path.join('/var/www/up/', filename))

	else:
		print "no update info"

	if time_tweet != '':
		return filename
	else:
		return 0



###############
## LP NOTIFY ##
###############
def tweet_lp():

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()


	sql = "select * from status where time=(select max(time) from status)"
	print "[SQL]:"+sql
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		db_time, rank, lp_now, lp_max, exp_now, exp_max, pop_flag = row
		if pop_flag == 1:
			message = str(datetime.datetime.now())+" LP:"+str(lp_max)+"/"+str(lp_max)+"(max)"
			post_tweet(message)
			print "[Tweet]POST:"+message
			sys.exit()
		else:
			timediff = int(time.mktime(datetime.datetime.now().timetuple())) - int(time.mktime(db_time.timetuple()))
			restore_lp = timediff / 60 / 6
			realtime_lp = lp_now + restore_lp
			if realtime_lp >= lp_max:
				message = "@nigt_liliwh575 "+str(datetime.datetime.now())+" LP overflow!"
				post_tweet(message)
				print "[Tweet]POST:"+message
				sql = "update status set notice_flag=1 order by time desc limit 1"
				print "SQL:"+sql
				cursor.execute(sql)
			else:
				message = str(datetime.datetime.now())+" LP:"+str(realtime_lp)+"/"+str(lp_max)
				post_tweet(message)
				print "[Tweet]POST:"+message
				

	connector.commit()
	cursor.close()
	connector.close()



	

################
## 色抽出関数 ##
################
def extract_color( src, h_th_low, h_th_up, s_th, v_th ):

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
def analyze_eventSC(filename):

	image = cv2.imread(os.path.join('/var/www/up/', filename))
#	trim_image = image[700:image.shape[0], 300:image.shape[1]/2]

	## ポイント記載部分トリミング
	trim_image = image[830:870, 350:500]
	## ピンクで２値化（累計ポイント取得用）
	pink_image = extract_color(trim_image, 160,  0, 80,  232)
	cv2.imwrite(os.path.join('/var/www/up/', 'pink_image.png'), pink_image)
	commands.getoutput("tesseract /var/www/up/pink_image.png /var/www/up/now -psm 7 nobatch digits")


	## item用ネガポジ解析
	look_up_table = np.ones((256, 1), dtype = 'uint8' ) * 0
	for i in range(256):
		look_up_table[i][0] = 255 - i
	## item記載部分トリミング
	trim_image = image[870:920, 350:500]
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
## スクショLP解析関数 ##
########################
def analyze_LP(filename):

	image = cv2.imread(os.path.join('/var/www/up/', filename))
#	trim_image = image[700:image.shape[0], 300:image.shape[1]/2]

	## ポイント記載部分トリミング
	trim_image = image[0:110, 800:1600]
	cv2.imwrite(os.path.join('/var/www/up/', 'status_image.png'), trim_image)

	rank_image = trim_image[40:100, 30:160]
	cv2.imwrite(os.path.join('/var/www/up/', 'rank_image.png'), rank_image)
	commands.getoutput("tesseract /var/www/up/rank_image.png /var/www/up/rank -psm 7 nobatch digits")
	lp_image = trim_image[70:105, 470:590]
	cv2.imwrite(os.path.join('/var/www/up/', 'lp_image.png'), lp_image)
    # グレースケールに変換
	lp_image = cv2.cvtColor(lp_image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(os.path.join('/var/www/up/', 'lp_image.png'), lp_image)
	commands.getoutput("tesseract /var/www/up/lp_image.png /var/www/up/lp -psm 7 nobatch digits")

	exp_image = trim_image[70:105, 200:350]
	cv2.imwrite(os.path.join('/var/www/up/', 'exp_image.png'), exp_image)
	commands.getoutput("tesseract /var/www/up/exp_image.png /var/www/up/exp -psm 7 nobatch digits")




########################
## ユーザ情報更新関数 ##
########################
def update_statusTable():

	global html_result
	global time_tweet

	try:

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		## point情報読み込みとDB更新
		f = open('/var/www/up/rank.txt')
		rank = f.readline().rstrip() # 1行を読み込む
		f.close	
		f = open('/var/www/up/lp.txt')
		lp = f.readline().rstrip() # 1行を読み込む
		lpnow,lpmax = lp.split(" ")
		f.close	
#		if lpnow >= lpmax:
#			notice_flag = "TRUE"
#		else:
#			notice_flag = "FALSE"
		notice_flag = "FALSE"
		f = open('/var/www/up/exp.txt')
		exp = f.readline().rstrip() # 1行を読み込む
		expnow,expmax = exp.split(" ")
		f.close	

		sql = "insert into status values('"+time_tweet+"',"+rank+","+lpnow+","+lpmax+","+expnow+","+expmax+","+notice_flag+")"
		html_result += "[SQL]"+ sql + "\n"
			
		cursor.execute(sql)


		## DB commit and close
		connector.commit()
		cursor.close()
		connector.close()
		html_result += " DB updated." + "\n"


	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)







##############################
## イベントポイント更新関数 ##
##############################
def update_eventTable(event):

	global html_result
	global time_tweet

	try:

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		event_name = event

	
		## point情報読み込みとDB更新
		f = open('/var/www/up/now.txt')
		nowpoint = f.readline().rstrip() # 1行を読み込む
		f.close	
		f = open('/var/www/up/item.txt')
		nowitem = f.readline().rstrip() # 1行を読み込む
		f.close	

		if nowitem!='':
			sql = "insert into "+event_name+" values('"+time_tweet+"',"+nowpoint+","+nowitem+")"
			html_result += "[SQL]"+ sql + "\n"
		else:
			sql = "insert into "+event_name+" values('"+time_tweet+"',"+nowpoint+",0)"
			html_result += "[SQL]"+ sql + "\n"
#			html_result += "[SQLFailed] Failed to get nowitem<br>"
			
		cursor.execute(sql)


		## DB commit and close
		connector.commit()
		cursor.close()
		connector.close()
		html_result += " DB updated." + "\n"


	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "MySQL Error: %s" % str(e)


##############################
## イベントポイント参照関数 ##
##############################
def show_Table(event):

	global html_result

	try:

		connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
		cursor = connector.cursor()

		event_name = event

	
 		##select
		sql = "select * from " + event_name
		html_result += "[SQL]"+sql+"\n"
		cursor.execute(sql)
		result = cursor.fetchall()
		html_result += "+-----------------------+\n"
		for row in result:
			if event == "status":
				html_result += "| "+str(row[0])+", RANK:"+str(row[1])+", LP:"+str(row[2])+"/"+str(row[3])+", EXP:"+str(row[4])+"/"+str(row[5])+", POP:"+str(row[6])+" |\n"
			else:
				html_result += "| "+str(row[0])+", "+str(row[1])+", "+str(row[2])+" |\n"
		html_result += "+-----------------------+\n"

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
if __name__=="__main__":

	filename = get_tweet_sc()
#	filename = "tweetsc.png"
#	filename = 0

	## 最初のアクセス用処理
	if filename != 0:
		analyze_LP(filename)
		update_statusTable()
		show_Table("status")

		analyze_eventSC(filename)
		update_eventTable("cf2")
		show_Table("cf2")

	tweet_lp()

	## end script and output result
	print html_result

