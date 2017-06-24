#!/usr/bin/python
#-*- coding: utf-8 -*-
import tweepy

consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
print "Access:", auth.get_authorization_url()
verifier = raw_input('Verifier:')
auth.get_access_token(verifier)
print "Access Token:", auth.access_token
print "Access Token Secret:", auth.access_token_secret

