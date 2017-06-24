#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask
from flask import request

import requests
import json
import re

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1499031330', # Channel ID
    'X-Line-ChannelSecret':'fa6bd42bdbec0cc2960b16d746c2de29', # Channel secre
    'X-Line-Trusted-User-With-ACL':'sbi9803m' # MID (of Channel)
}

def post_event( to, content):
    msg = {
        'to': [to],
        'toChannel': 1383378250, # Fixed  value
        'eventType': "138311608800106203", # Fixed value
        'content': content
    }
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

def post_text( to, text ):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)


commands = (
    (re.compile('test', 0), lambda x: 'testest'),
    (re.compile('test2', 0), lambda x:'testtestetset'),
)

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def hello():
    msgs = request.json['result']
    for msg in msgs:
        text = msg['content']['text']
        for matcher, action in commands:
            if matcher.search(text):
                response = action(text)
                break
        else:
            response = 'yes'

        post_text(msg['content']['from'],response)

    return ''

if __name__ == "__main__":
    context = ('cert/cert.pem', 'cert/privkey.pem')
    app.run(host='koke.link', port=443, ssl_context=context, threaded=True, debug=True)

