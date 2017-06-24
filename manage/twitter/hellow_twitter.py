#!/usr/bin/python
#-*- coding: utf-8 -*-
import tweepy

#認証を行う
consumer_key = "E7PLfevrHNVI9ozuQlF6xXDgG"
consumer_secret = "CfobRZOWqXvPytSbn3zUDklsS81bUWXJjd3RIEYcUKnOnd1kQx"
access_token="721661385977909249-wtx82HRTTSzm1mJgOnW0vbjR13tWCOr"
access_secret = "uFeckhWHjU5JHBOGIvPLEHQgSbfRk3SjrxUBMyLNRNh7X"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#Hello, world!と投稿する
api.update_status('Hello, world!')

