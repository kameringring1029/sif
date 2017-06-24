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



##########
## main ##
##########
if __name__=="__main__":

	# インスタンス生成
	useTwitter = usetwitter.UseTwitter()
	useSQL = usesql.UseSQL()

	useSQL.update_borderTable(useTwitter,"sm32")


	print "manage_sif.py end\n"

