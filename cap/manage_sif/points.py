#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import time
import datetime

time_format="%Y-%m-%d %H:%M:%S"


class Points:

	time = datetime.datetime.now()
	rank = 0
	lp_now = 0
	lp_max = 0
	lp_max_time = ""
	exp_now = 0
	exp_max = 0
	loveca = 0
	eventpoint = 0;


	def setRank(self, rank):
		self.rank = rank

	def setLpmax(self, lp_max):
		self.lp_max = lp_max
			
	def setLpmaxtime(self, lp_max_time):
		tdatetime = datetime.datetime.strptime(lp_max_time, '%Y-%m-%d %H:%M:%S')
		self.lp_max_time = tdatetime

		delta = tdatetime - self.time
		self.setLpnow(self.lp_max - (delta.seconds / 60 / 6))
			
	def setLpnow(self, lp_now):
		if(lp_now <= self.lp_max):
			self.lp_now = lp_now
		else:
			self.lp_now = lp_max
	
	def setExpnow(self, exp_now):
		self.exp_now = exp_now

	def setExpmax(self, exp_max):
		self.exp_max = exp_max

	def setLoveca(self, loveca):
		self.loveca = loveca

	def setEventpoint(self, eventpoint):
		self.eventpoint = eventpoint

	def getRank(self):
		return self.rank 

	def getLpmax(self):
		return self.lp_max 
			
	def getLpmaxtime(self):
		return self.lp_max_time 
			
	def getLpnow(self):
		return self.lp_now
	
	def getExpnow(self):
		return self.exp_now

	def getExpmax(self):
		return self.exp_max
		#self.exp_max = exp_max

	def getLoveca(self):
		return self.loveca

	def getEventpoint(self):
		return self.eventpoint


	def showPoints(self):
		pointinfo = "Time: "+str(self.time.strftime("%Y/%m/%d %H:%M")) +\
					"\nRank: "+str(self.rank) +\
					"\nLP max time: "+str(self.lp_max_time) +\
					"\nLP: "+str(self.lp_now)+"/"+str(self.lp_max) +\
					"\nEXP: "+str(self.exp_now)+"/"+str(self.exp_max) +\
					"\nLoveca: "+str(self.loveca) +\
					"\nEvent point: "+str(self.eventpoint)

		print pointinfo


	def tweetPoints(self, useTwitter):
		pointinfo = "[ユーザ情報更新]" +\
					"\nTime: "+str(self.time.strftime("%Y/%m/%d %H:%M")) +\
					"\nRank: "+str(self.rank) +\
					"\nLP max time: "+str(self.lp_max_time) +\
					"\nLP: "+str(self.lp_now)+"/"+str(self.lp_max) +\
					"\nEXP: "+str(self.exp_now)+"/"+str(self.exp_max) +\
					"\nLoveca: "+str(self.loveca) +\
					"\nEvent point: "+str(self.eventpoint)
		
		useTwitter.post_tweet(pointinfo)

		print "tweet points."



