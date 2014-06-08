#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from behavior import behavior, statistics
import json

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'hawkwang':
        return '1111111'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)

@app.route('/behavior/api/v1.0/behaviors', methods = ['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'uid' in request.json:
        abort(400)

    # construct behavior item
    new_behavior = {}
    new_behavior['uid'] = request.json['uid']
    new_behavior['gid'] = request.json['gid']
    new_behavior['t'] = request.json['t']
    new_behavior['IP'] = request.json['IP']
    new_behavior['bcode'] = request.json['bcode']
    new_behavior['tcode'] = request.json['tcode']
    new_behavior['tid'] = request.json['tid']

    # get behavior log, use new thread to put it into database - behavior
    thread = behavior.behavior(new_behavior)
    thread.start()

    return 'ok', 201
#end def

@app.route('/behavior/api/v1.0/statistics', methods = ['POST'])
@auth.login_required
def create_statistics():
    if not request.json or not 'uid' in request.json:
        abort(400)

    # construct behavior item
    behavior_query = {}
    behavior_query['uid'] = request.json['uid']
    behavior_query['gid'] = request.json['gid']
    behavior_query['t'] = request.json['t']
    behavior_query['IP'] = request.json['IP']
    behavior_query['bcode'] = request.json['bcode']
    behavior_query['tcode'] = request.json['tcode']
    behavior_query['tid'] = request.json['tid']

    # get brief statistic report
    briefreport = statistics.getbrief(behavior_query)

    return jsonify( { 's': briefreport['self'], 't': briefreport['total'] } ), 201 
#end def



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
#end def

if __name__ == '__main__':
    #SERVER_NAME = '127.0.0.1'
    #SERVER_PORT = 5002
    app.run(host = '127.0.0.1', port = 5002, debug = True)
#endif
