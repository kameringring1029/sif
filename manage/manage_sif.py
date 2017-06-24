#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import MySQLdb
import time
import datetime

time_format="%Y-%m-%d %H:%M:%S"


import usetwitter
import usecv
import usesql

###############
## LP NOTIFY ##
###############
def tweet_lp(useTwitter):
	print "tweet_lp"

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()


	sql = "select distinct user from status_multiuser"
	print "[SQL]:"+sql
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		sql = "select * from status_multiuser where (user='"+str(row[0])+"') and (time=(select max(time) from status_multiuser where user='"+str(row[0])+"'))"
		print "[SQL]:"+sql
		cursor.execute(sql)
		data = cursor.fetchall()
		
		print str(data[0])

		db_time, rank, lp_now, lp_max, exp_now, exp_max, pop_flag, username = data[0]

		timediff = int(time.mktime(datetime.datetime.now().timetuple())) - int(time.mktime(db_time.timetuple()))
		restore_lp = timediff / 60 / 6 ## 回復LP

		posttime = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
		realtime_lp = lp_now + restore_lp ## 現在のLP

		if pop_flag == 0:
			if realtime_lp >= lp_max:
			# LP満タン時の通知処理 #
				message = "@"+username+" "+posttime+"\n"+str(lp_max)+"/"+str(lp_max)+" LP overflow!"
				useTwitter.post_tweet(message)
				print "[Tweet]POST:"+message
				sql = "update status_multiuser set notice_flag=1 where (user='"+str(row[0])+"')"
				print "[SQL]:"+sql
				cursor.execute(sql)
				continue


		# 通常時のTweet処理 #
		if realtime_lp >= lp_max:
			message = "["+username+"] "+posttime+"\n<LP> "+str(lp_max)+"/"+str(lp_max)+"(full)\n<Rank> "+str(rank)+"\n<Exp> "+str(exp_now)+"/"+str(exp_max)+"\n---event---\nhttp://koke.link/sif"
		else:
			message = "["+username+"] "+posttime+"\n<LP> "+str(realtime_lp)+"/"+str(lp_max)+"\n<Rank> "+str(rank)+"\n<Exp> "+str(exp_now)+"/"+str(exp_max)+"\n---event---\nhttp://koke.link/sif"

		if username!='sif_notify_bot':
			useTwitter.post_tweet(message)
		print "[Tweet]POST:"+message
				

	connector.commit()
	cursor.close()
	connector.close()





##########
## main ##
##########
if __name__=="__main__":

	# インスタンス生成
	useTwitter = usetwitter.UseTwitter()
	useCV = usecv.UseCV()
	useSQL = usesql.UseSQL()

	loopno = 0
	filename = 1

	while filename != 0:
		filename = useTwitter.get_tweet_sc(loopno)
		#filename = "tweetsc.jpg"
		#filename = "sc-ipad.png"
		#filename = "scsample-1.jpg"
		#filename = "scsample-2.jpg"
		#filename = "scsample-3.jpg"

		if filename == 0:
			break

		loopno = loopno + 1

		useCV.trim_frame_by_SC(filename)
		useCV.analyze_LP("only_apl.jpg")
#		useSQL.update_statusTable(useTwitter)
		useCV.analyze_eventSC("only_apl.jpg")


#	useSQL.update_eventTable(useTwitter,"cf3")

#	tweet_lp(useTwitter)

	useSQL.closeDB()

	print "manage_sif.py end\n"

