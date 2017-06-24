#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import time
import datetime
import tweepy
import urllib

time_format="%Y-%m-%d %H:%M:%S"


class UseTwitter:
	
	time_tweet =""
	username =""
	request =""
	flag = 0

	#認証
	consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
	consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
	access_token="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
	access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
		

	################
	## POST TWEET ##
	################
	def post_tweet(self,message):
		#投稿する
		self.api.update_status(message)


	################
	## POST TWEET WITH IMAGE ##
	################
	def post_tweet_image(self,reply_id,message,image_path):
		#投稿する
		self.api.update_with_media(in_reply_to_status_id=reply_id,filename=image_path,status=message)



	##################
	## GET TWEET SC ##
	##################
	def get_tweet_sc(self, loopno):

		filename = 0

		if self.api.home_timeline()[loopno].text.find('@sif_notify_bot') != -1 :
			tweetimage = self.api.home_timeline()[loopno].entities['media'][0]['media_url'] + ":orig"
			self.time_tweet = self.api.home_timeline()[loopno].created_at
			self.time_tweet += datetime.timedelta(hours = 9)
			self.time_tweet = self.time_tweet.strftime(time_format)
	
			self.username = self.api.home_timeline()[loopno].author.screen_name
	
			print "time_tweet:"+self.time_tweet
			print "author:@"+self.username
	
			filename = 'tweetsc.jpg'
	
			urllib.urlretrieve(tweetimage, os.path.join('/var/www/up/', filename))
	
		else:
			print "no update info"
	
		if self.time_tweet != '':
			print "get SC from tweet"
			return filename
		else:
			return 0


	####################
	## GET GATCHA REQ ##
	####################
	def get_gatcha_request(self):

		if self.api.home_timeline()[0].text.find('@sif_notify_bot') != -1 :
			self.request = self.api.home_timeline()[0].text
			self.time_tweet = self.api.home_timeline()[0].created_at
			self.time_tweet += datetime.timedelta(hours = 9)
			self.time_tweet = self.time_tweet.strftime(time_format)
	
			self.username = self.api.home_timeline()[0].author.screen_name
	
			print "time_tweet:"+self.time_tweet
			print "author:@"+self.username
			print "request:"+self.request

			flag = 1
	
	
		else:
			flag = 0
			print "no update info"
	
		return flag
	


	################
	## GET BORDER ##
	################
	def get_border(self):
		print "get_border"
	
		tweet = self.api.user_timeline("sifjp_trackbot")[0].text

		#print tweet

		line = tweet.split("\n")
		T1 = line[1].split(u': ')[1].split(" (")[0]
		T2 = line[2].split(u': ')[1].split(" (")[0]
		T3 = line[3].split(u': ')[1].split(" (")[0]
		time = line[4].split(u' ')[1]+" "+line[4].split(u' ')[2]
	
		if tweet != '':
			return [time, T1, T2, T3]
		else:
			return [0, 0, 0, 0]


