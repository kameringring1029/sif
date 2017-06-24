#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('daAevLmHJIeqvXBQ+oet1G/CRJROVvr78byQ5DOeJsmhZv28BFK8wo3D247qPq027I8jyx7LXkuyVnZOpHLubmQwmk4mBFknY9JLIZg7y3aZeZDL1saM1NLl7Myz8O+gBHhtFA3h7JyOgoKEX55XOQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fa6bd42bdbec0cc2960b16d746c2de29')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

