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
import useburp
import points


def getUrl(event):
	url = ""
	if event.find("sm") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_battle_endRoom.json"
	if event.find("cf") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_challenge_finalize.json"
	if event.find("mf") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_festival_liveReward.json"
	if event.find("ic") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_live_reward.json"
	if event.find("none") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_live_reward.json"
	if event.find("or") != -1:
		url = "/home/pi/sif/cap/mirrordir/prod-jp.lovelive.ge.klabgames.net_main.php_quest_questReward.json"

	print "getUrl" + url + "\n"
	return url


##########
## main ##
##########
if __name__=="__main__":

	# インスタンス生成
	useTwitter = usetwitter.UseTwitter()
	useSQL = usesql.UseSQL()
	useBurp = useburp.UseBurp()
	point = points.Points()

	event = "sm32"

	if os.path.isfile(getUrl(event)):
		print "analysis\n"
		useBurp.read_burplog(point, event)
		point.showPoints()
		if event != "none":
			print "out of event\n"
			useSQL.update_eventTable(point,event)
		useSQL.update_statusTable(point)

	elif os.path.isfile(getUrl("none")):
		print "analysis\n"
		useBurp.read_burplog(point, "none")
		point.showPoints()
		useSQL.update_statusTable(point)


	print "manage_sif.py end\n"

