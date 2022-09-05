from decouple import config as config_decouple
from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask_restful import Api
from config import config
from db import db
from mail import mail
from f import f

from models.user import UserModel
from models.event import EventModel

from resources.events import Events
from resources.users import Users
from resources.login import Login

app = Flask(__name__)
environment = config['development']
if config_decouple('PRODUCTION', cast=bool, default=False):
    environment = config['production']

app.config.from_object(environment)

api = Api(app)
CORS(app, resources={r'/*': {'origins': '*'}})

mail.init_app(app)
db.get_instance().init_app(app)
EventModel.collection = db.get_database.event
UserModel.collection = db.get_database.user
f.get_instance().init_app(app)

@app.route('/')
def render():
    return render_template("index.html")


api.add_resource(Users, '/user/',
                 '/user/id/<string:id>',
                 '/user/username/<string:username>',
                 '/user/email/<string:email>')

api.add_resource(Login, '/login/')

api.add_resource(Events, '/event/',
                 '/events/<string:username>',
                 '/event/<string:username>')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
