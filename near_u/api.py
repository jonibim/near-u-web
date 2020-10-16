"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

from near_u.models import db, User, Sensor, Condition, Task, Configuration
from flask import Flask, jsonify, Blueprint, jsonify, request
from pydub import AudioSegment
from appserver import *
from datetime import datetime, timedelta
from near_u.controller import *
from functools import wraps
import base64
import jwt
import os

global THREAD 
THREAD = []

api = Blueprint('api', __name__)

### Sanity checks ####

@api.route('/ping', methods=('GET',))
def ping_pong():
    return jsonify('pong!')

#### Debugging ####

@api.route('/debug/sensors/')
def debug_sensors():
    sensors = Sensor.query.all()
    return jsonify({ 'Available sensors': [s.to_dict() for s in sensors] })

@api.route('/debug/condition/')
def debug_conditions():
    condition = Condition.query.all()
    return jsonify({ 'Available sensors': [s.to_dict() for s in condition] })

@api.route('/debug/sensors/<int:id>/')
def debug_sensor(id):
    sensor = Sensor.query.get(id)
    return jsonify({ 'Sensor': sensor.to_dict() })

@api.route('/debug/tasks/')
def debug_tasks():
    tasks = Task.query.all()
    return jsonify({ 'Available tasks': [t.to_dict() for t in tasks] })

@api.route('/debug/tasks/<int:id>/')
def debug_task(id):
    task = Task.query.get(id)
    return jsonify({ 'Task': task.to_dict() })

#### Requests/Responses ####

@api.route('/sensors/', methods=('GET',))
def fetch_sensors():
    if request.method == 'GET':
        sensors = Sensor.query.all()
        return jsonify({ 'sensors': [s.to_dict() for s in sensors] })

@api.route('/sensors/<int:id>/', methods=('GET',))
def sensor(id):
    if request.method == 'GET':
        sensor = Sensor.query.get(id)
        return jsonify({ 'Sensor': sensor.to_dict() })

@api.route('/tasks/', methods=('GET', 'POST'))
def fetch_tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        return jsonify({ 'tasks': [t.to_dict() for t in tasks] })
    elif request.method == 'POST':
        data = request.get_json()
        filename = './recordings/'+data['title']+'.mp3'
        #print(data['configuration']['message'])
        base64_img_bytes = data['configuration']['message'].encode('utf-8')
        with open(filename, 'wb') as file_to_save:
            decoded_image_data = base64.decodebytes(base64_img_bytes)
            file_to_save.write(decoded_image_data)
        sound = AudioSegment.from_file(filename,'webm') 
        sound.export(filename, format="mp3")
        configurations = [Configuration(
                notifications = data['configuration']['notifications'],
                repeat = data['configuration']['repeat'],
        )]
        task = Task(
            title=data['title'], 
            s_type=data['s_type'], 
            condition=data['condition'],
            ) 
        task.configurations = configurations
        db.session.add(task)
        db.session.commit()
        return jsonify(task.to_dict()), 201

@api.route('/tasks/<int:id>/', methods=('DELETE', 'PUT'))
def task(id):
    if request.method == 'DELETE':
        name=db.session.query(Task.title).filter(Task.id == id).scalar()
        response_object = {'status': 'success'}
        if os.path.exists('./recordings/'+name+'.mp3'):
            os.remove('./recordings/'+name+'.mp3')
        else:
            print("The file does not exist") 
        Task.query.filter_by(id=id).delete()
        Configuration.query.filter_by(task_id=id).delete()
        db.session.commit()
        return jsonify(response_object)
    elif request.method == 'PUT':
        data = request.get_json()
        for c in data['configurations']:
            task.configurations = Configuration(
                notifications = ['notifications'], 
                repeat = c['repeat'], 
            )
        db.session.commit()
        task = Task.query.get(data['id'])
        v

@api.route('/active/', methods=('GET','POST'))
def active():
    if request.method == 'GET':
        if (os.path.isfile(PATH_FOLDER + '/running')):
            with open(PATH_FOLDER + '/current', 'w') as json_file:
                data = js.load(json_file)
                return data,201
        else:
            return {'message':'false'},201
        # return jsonify({ 'sensors': [s.to_dict() for s in sensors] })
    elif request.method == 'POST':
        data = request.get_json()
        c_type = db.session.query(Condition.c_type).filter(Condition.id ==  data['condition']).scalar()
        json = [{
            'title': data['title'],
            'condition' : data['condition'],
            'c_type': c_type,
            'repeat': data['configurations'][0]['repeat']
        }]
        if (len(THREAD) > 0):
            if (os.path.isfile(PATH_FOLDER + '/running')):
                os.remove(PATH_FOLDER + "/running")
            THREAD[0].join()
        trh = Thread(target = writeJSONandExecute, args=(json)) 
        trh.daemon = True
        THREAD.append(trh)
        trh.start() 
        return '',200
    
@api.route('/deactive/', methods=('GET',))
def deactivate():
    if (len(THREAD) > 0):
        if (os.path.isfile(PATH_FOLDER + '/running')):
            os.remove(PATH_FOLDER + "/running")
        THREAD[0].join()
    return '',200



@api.route('/register', methods=['POST',])
def register():
    data = request.get_json()
    user = User.authenticate(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api.route('/login', methods=['POST',])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if not user:
        return jsonify({'message': 'Invalid credentials', 'authenticated': False}), 401

    token =jwt.encode({
        'sub': user.email,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('UTF-8') })

def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registration and / or authentication required',
            'authenticated': False
         }
        expired_msg = {
            'message': 'Expired token. Reauthentication required',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401
    return _verify
