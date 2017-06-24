#!/usr/bin/python
# -*- coding: utf-8 -*- 
  
import MySQLdb
import time
import datetime
 
time_format="%Y-%m-%d %H:%M:%S"

if __name__ == "__main__":

	connector = MySQLdb.connect(host="localhost", db="sif_event", user="web", passwd="password", charset="utf8")
	cursor = connector.cursor()

	#現在時刻の取得と整形
	localtime = time.strftime(time_format)
	localtime = time.strftime(time_format, time.localtime())

	sql = "select * from status where time=(select max(time) from status)"
	print "SQL:"+sql
	cursor.execute(sql)
	result = cursor.fetchall()
	for row in result:
		time, rank, lp_now, lp_max, exp_now, exp_max, pop_flag = row
		if pop_flag == 1:
			sys.exit()
		else:
			

	connector.commit()
	  
	cursor.close()
	connector.close()


