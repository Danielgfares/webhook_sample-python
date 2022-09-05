import hashlib
import hmac

from flask import g, current_app
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

from f import F

auth = HTTPBasicAuth()


class UserModel(object):
    collection = None  # db.get_instance().get_database.user
    id = None
    username = None
    password = None
    fpassword = None
    email = None

    def __init__(self, username=None, email=None):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    def json(self):
        return {
            'username': self.username,
            'password': self.password,
            'fpassword': self.fpassword,
            'email': self.email
        }

    def save_to_db(self):
        try:
            user = UserModel.find_by_username(self.username)
            if user:
                raise Exception("User with name [{}] already exists!".format(self.username))
        except:
            pass

        result = self.collection.insert_one(self.json())
        self.id = result.inserted_id

    def delete_from_db(self):
        user = UserModel.find_by_id(id=self.id)
        self.collection.find_one_and_delete({'-id': self.id})

    def update_data(self, username=None, password=None, email=None):
        if username and username != self.username:
            user = UserModel.find_by_username(username)
            if user:
                raise Exception("User with name {} already exists".format(username))
            self.username = username
        if password:
            self.hash_password(password)
        if email and email != self.email:
            self.email = email

        self.collection.find_one_and_update(
            {'_id': self.id},
            {
                '$set': {
                    'username': self.username,
                    'password': self.password,
                    'fpassword': self.fpassword,
                    'email': self.email
                }
            }
        )
        return self.json()

    def hash_password(self, password: str):
        self.fpassword = F.get_instance().get_f.encrypt(password.encode('utf-8')).decode('utf-8')
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password) and password == self.get_pass()

    def get_pass(self):
        s: str = F.get_instance().get_f.decrypt(self.fpassword.encode('utf-8')).decode('utf-8')
        return s

    @classmethod
    def find_all(cls):
        docs = cls.collection.find()
        users = list()
        for doc in docs:
            user = UserModel(doc['username'], doc['email'])
            user.id = doc['_id']
            user.password = doc['password']
            user.fpassword = doc['fpassword']
            users.append(user)
        return users

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.secret_key, expires_in=expiration)
        return s.dumps({'username': self.username})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token

        user = cls.find_by_username(username=data['username'])

        return user

    @classmethod
    def find_by_username(cls, username: str):
        doc = None
        try:
            doc = cls.collection.find_one({'username': username})
        except:
            raise Exception("User not found")
        if doc:
            user = UserModel(doc['username'], doc['email'])
            user.id = doc['_id']
            user.password = doc['password']
            user.fpassword = doc['fpassword']
            return user

    @classmethod
    def find_by_email(cls, email):
        doc = cls.collection.find_one({'email': email})
        user = UserModel(doc['username'], doc['email'])
        user.id = doc['_id']
        user.password = doc['password']
        user.fpassword = doc['fpassword']
        return user

    @classmethod
    def find_by_id(cls, id):
        doc = cls.collection.find_one({'_id': id})
        user = UserModel(doc['username'], doc['email'])
        user.id = doc['_id']
        user.password = doc['password']
        user.fpassword = doc['fpassword']
        return user


@auth.verify_password
def verify_password(token, password):
    user = UserModel.verify_auth_token(token)
    if user:  # and user.verify_password(password=password):
        g.user = user
        return user


@auth.get_user_roles
def get_user_roles(user):
    if user and type(user) is UserModel:
        return ['user']


def is_signature_valid(message, message_signature, user: UserModel):
    token = user.get_pass()
    signature = 'sha256={0}'.format(
        hmac.new(
            bytes(token, 'utf-8'),
            bytes(message, 'utf-8'),
            hashlib.sha256
        ).hexdigest()
    )
    return hmac.compare_digest(message_signature, signature)
