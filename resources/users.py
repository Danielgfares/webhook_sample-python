from flask_restful import Resource, reqparse
from lock import lock
from models.user import UserModel, auth, g


class Users(Resource):

    def get(self, id=None, username=None, email=None):
        with lock.lock:
            user = None
            if id:
                user = UserModel.find_by_id(id=id)
            elif username:
                user = UserModel.find_by_username(username=username)
            elif email:
                user = UserModel.find_by_email(email=email)
            if user:
                return {'user': user.json()}, 200
            else:
                return {'user': {}}, 404  # not found

    def post(self):
        with lock.lock:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('email', type=str, required=True, help='This field cannot be left blank')
            data = parser.parse_args()
            try:
                user = UserModel(username=data['username'], email=data['email'])
                user.hash_password(data['password'])
                user.save_to_db()
                return {'user': user.json()}, 201
            except Exception as e:
                return {'message': f'{type(e)}:{e}'}, 409

    @auth.login_required(role='user')
    def delete(self, username=None):
        with lock.lock:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')
            data = parser.parse_args()
            try:
                user = UserModel.find_by_username(username=username)
                if user.verify_password(password=data['password']):
                    user.delete()
                    return {'user': user.json()}, 200
                return {'message': 'not allowed'}, 500
            except Exception as e:
                return {'message': f'{type(e)}:{e}'}, 404