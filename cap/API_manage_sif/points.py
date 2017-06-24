#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import time
import datetime

time_format="%Y-%m-%d %H:%M:%S"


class Points:

	time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
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
		self.lp_max_time = lp_max_time
			
	def setLpnow(self):
		if(lp_now != 0):
			self.lp_now = lp_now
	
	def setExpnow(self, exp_now):
		self.exp_now = exp_now

	def setExpmax(self, exp_next):
		self.exp_max = self.exp_now + exp_next

	def setLoveca(self, loveca):
		self.loveca = loveca

	def setEventpoint(self, eventpoint):
		self.eventpoint = eventpoint


	def showPoints(self):
		pointinfo = "Time: "+str(self.time) +\
					"\nRank: "+str(self.rank) +\
					"\nLP max time: "+str(self.lp_max_time) +\
					"\nLP: "+str(self.lp_now)+"/"+str(self.lp_max) +\
					"\nEXP: "+str(self.exp_now)+"/"+str(self.exp_max) +\
					"\nLoveca: "+str(self.loveca) +\
					"\nEvent point: "+str(self.eventpoint)

		print pointinfo


	def tweetPoints(self, useTwitter):
		pointinfo = "[ユーザ情報更新]" +\
					"\nTime: "+str(self.time) +\
					"\nRank: "+str(self.rank) +\
					"\nLP max time: "+str(self.lp_max_time) +\
					"\nLP: "+str(self.lp_now)+"/"+str(self.lp_max) +\
					"\nEXP: "+str(self.exp_now)+"/"+str(self.exp_max) +\
					"\nLoveca: "+str(self.loveca) +\
					"\nEvent point: "+str(self.eventpoint)
		
		useTwitter.post_tweet(pointinfo)

		print "tweet points."



