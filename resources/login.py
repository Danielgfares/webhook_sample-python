from flask_restful import Resource, reqparse
from lock import lock
from models.user import UserModel


class Login(Resource):

    def get(self):
        with lock.lock:
            return {'message': "Not developed yet"}, 404

    def post(self):
        with lock.lock:
            # POST LOGIN not used for security purposes
            parser = reqparse.RequestParser()  # create parameters parser from request
            # define all input parameters need and its type
            parser.add_argument('username', type=str, required=True, help='This field cannot be left blank')
            parser.add_argument('password', type=str, required=True, help='This field cannot be left blank')

            data = parser.parse_args()

            if data:
                user = UserModel.find_by_username(username=data['username'])
                if user:
                    if user.verify_password(password=data['password']):
                        token = user.generate_auth_token()
                        return {'token': token.decode('ascii')}, 200
                    return {'message': "password incorrect"}, 400
                return {'message': "An error occurred. Username not found"}, 404
            return {'message': "An error occurred parsing arguments."}, 500

    def delete(self):
        return {'message': "Not developed yet"}, 404

    def put(self):
        return {'message': "Not developed yet"}, 404

