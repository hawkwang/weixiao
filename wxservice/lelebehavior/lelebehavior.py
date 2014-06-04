#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, abort, make_response, request
from wxanalyzer.webpage.event import getEvent
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

#for event
@app.route('/todo/api/v1.0/events', methods = ['POST'])
@auth.login_required
def get_event():
    if not request.json or not 'url' in request.json:
        abort(400)
    url = request.json['url']
    success,msg,e = getEvent(url)
    result = {
        'success': success,
        'msg': msg,
        'event': e
    }

    strEvent = str(success) + '||' + msg 
    if success==1:
        strEvent = strEvent + '||' + e['city'] + '||' + e['title'] + '||' + e['description']
        strEvent = strEvent + '||' + e['date'] + '||' + e['time']
        strEvent = strEvent + '||' + e['location'] + '||' + e['fee']
        strEvent = strEvent + '||' + e['image'] + '||' + e['url']
    return strEvent, 201
    #return json.dumps(result), 201
    #return jsonify({'event': e['title']}), 201
    #return jsonify( { 'result': result, 'event': e['title'] } ), 201
#end def



@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_tasks():
    return jsonify( { 'tasks': tasks } )
#end def

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
@auth.login_required
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': task[0] } )
#end def

@app.route('/todo/api/v1.0/tasks', methods = ['POST'])
@auth.login_required
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify( { 'task': task } ), 201
#end def

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify( { 'task': task[0] } )
#end def

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify( { 'result': True } )
#end def

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
#end def

if __name__ == '__main__':
    #SERVER_NAME = '127.0.0.1'
    #SERVER_PORT = 5001
    app.run(host = '127.0.0.1', port = 5001, debug = True)
#endif
