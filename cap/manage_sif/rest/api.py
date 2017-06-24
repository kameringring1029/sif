# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, make_response
import peewee
# import json

db = MySQLDatabase('sif_event', user='web', charset='utf8')

class User(peewee.Model):
    cardId = peewee.IntegerField()
    cardName = peewee.TextField()
    cardSeries = peewee.TextField()

    class Meta:
        database = db

api = Flask(__name__)

@api.route('/getUser/<string:userId>', methods=['GET'])
def get_user(userId):
    try:
        user = User.get(User.userId == userId)
    except User.DoesNotExist:
        abort(404)

    result = {
        "result":True,
        "data":{
            "userId":user.userId,
            "userCompany":user.userCompany,
            "userDiscountRate":user.userDiscountRate
            }
        }

    return make_response(jsonify(result))
    # UnicodeÇ…ÇµÇΩÇ≠Ç»Ç¢èÍçáÇÕÅ´
    # return make_response(json.dumps(result, ensure_ascii=False))

@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=3000)

