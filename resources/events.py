from flask import request
from flask_restful import Resource, reqparse

from lock import lock
from models.event import EventModel
from models.user import UserModel, auth, g
from services.send_email import email_service
from models.user import is_signature_valid


class Events(Resource):

    @auth.login_required()
    def get(self, username: str = None):
        with lock.lock:
            try:
                if g.user.username == username:
                    events = EventModel.find_by_username(username)
                    return {'events': [event.json() for event in events]}, 200
                raise Exception('Error. User not allowed!')
            except Exception as e:
                return {'message': f'{type(e)}:{e}'}, 404

    def post(self, username: str = None):
        with lock.lock:
            data = request.get_json()
            data_str = request.data
            signature = request.headers['X-Hub-Signature-256']
            user = UserModel.find_by_username(username=username) if username else None
            try:
                if is_signature_valid(data_str.decode('utf-8'), signature, user):
                    event = EventModel(userid=user.id, data=data)
                    event.save_to_db()
                    info = dict(event.json())
                    info['username'] = user.username
                    info['email'] = user.email
                    #################################### send email
                    email_service.send_email([user.email], 'Event: {0}'.format(data['TriggerEventName']), info)
                    ####################################
                    return {'event': event.json()}, 201
                return {'message': 'Signature not valid'}, 400
            except Exception as e:
                return {'message': f'Internal Server Error: {type(e)}:{e}'}, 500

