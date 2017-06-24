#!/usr/bin/python
# -*- coding: utf-8 -*-


import os, sys
import MySQLdb
import time
import datetime

time_format="%Y-%m-%d %H:%M:%S"


class UseSQL:

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()

	########################
	## ユーザ情報更新関数 ##
	########################
	def update_statusTable(self, useTwitter):
		print "update_statusTable"

		try:
	
			## point情報読み込みとDB更新
			f = open('/var/www/up/rank.txt')
			rank = f.readline().strip() # 1行を読み込む
			rank = rank.replace(" ","")
			f.close	
			f = open('/var/www/up/lp.txt')
			lp = f.readline().strip() # 1行を読み込む
			lp = lp.replace("7 ","/")
			lpnow,lpmax = lp.split("/")
			f.close	
			notice_flag = "FALSE"
			f = open('/var/www/up/exp.txt')
			exp = f.readline().strip() # 1行を読み込む
			exp = exp.replace("7 ","/")
			expnow,expmax = exp.split("/")
			f.close	

			sql = "insert into status_multiuser values('"+useTwitter.time_tweet+"',"+rank+","+lpnow+","+lpmax+","+expnow+","+expmax+","+notice_flag+",'"+useTwitter.username+"')"
			print "[SQL]"+ sql 
			
			self.cursor.execute(sql)

			## DB commit 
			self.connector.commit()
			print " DB updated." 


		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)







	##############################
	## イベントポイント更新関数 ##
	##############################
	def update_eventTable(self, useTwitter,event):
		print "update_eventTable"
	
		try:


			event_name = event

			#現在時刻の取得と整形
			localtime = time.strftime(time_format)
			localtime = time.strftime(time_format, time.localtime())
		
			## point情報読み込みとDB更新
			f = open('/var/www/up/now.txt')
			nowpoint = f.readline().strip() # 1行を読み込む
			f.close	
			f = open('/var/www/up/item.txt')
			nowitem = f.readline().strip() # 1行を読み込む
			f.close	

			border_time, double, single = useTwitter.get_border()
			print border_time+"/"+double+"/"+single
	
			if useTwitter.time_tweet=='':
				useTwitter.time_tweet = "2016/"+border_time+":00"

			if nowitem=='':
				nowitem = 0

			sql = "insert into "+event_name+" values('"+useTwitter.time_tweet+"',"+str(nowpoint)+","+str(nowitem)+","+str(double)+","+str(single)+")"
			print "[SQL]"+ sql 
			
			self.cursor.execute(sql)


			## DB commit and close
			self.connector.commit()
			print " DB updated." 


		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)


	##############################
	## イベントポイント参照関数 ##
	##############################
	def show_Table(self, event):


		try:
	
			event_name = event
	
	
 			##select
			sql = "select * from " + event_name
			print "[SQL]"+sql
			cursor.execute(sql)
			result = cursor.fetchall()
			print "+-----------------------+"
			for row in result:
				if event == "status":
					print "| "+str(row[0])+", RANK:"+str(row[1])+", LP:"+str(row[2])+"/"+str(row[3])+", EXP:"+str(row[4])+"/"+str(row[5])+", POP:"+str(row[6])+" |"
				else:
					print "| "+str(row[0])+", "+str(row[1])+", "+str(row[2])+", "+str(row[3])+", "+str(row[4])+" |"
			print "+-----------------------+"
	
			## DB commit and close
			connector.commit()
	

		except MySQLdb.Error, e:
			try:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			except IndexError:
				print "MySQL Error: %s" % str(e)





	################
	## DB終了関数 ##
	################
	def closeDB(self):
		self.cursor.close()
		self.connector.close()

