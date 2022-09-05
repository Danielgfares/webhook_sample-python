from datetime import datetime

from models.user import UserModel


class EventModel(object):
    collection = None  # db.get_instance().get_database.event
    id = None
    userid = None
    time = None
    data = None

    def __init__(self, userid: str, data: dict, user: UserModel = None):
        if user:
            self.user = user
            self.userid = userid
        else:
            self.user = UserModel.find_by_id(userid)
            self.userid = userid

        self.data = data
        self.time = datetime.utcnow().isoformat()

    def __repr__(self):
        return '<Event %r>' % self.id

    def json(self):
        return {
            'userid': f'{self.user.id.__str__()}',
            'time': f'{self.time}',
            'data': self.data
        }

    def save_to_db(self):
        result = self.collection.insert_one(self.json())
        self.id = result.inserted_id

    def delete_from_db(self):
        event = EventModel.find_by_id(id=self.id)
        self.collection.find_one_and_delete({'_id': self.id})

    def update_data(self, data: dict):
        self.collection.find_one_and_update(
            {'_id': self.id},
            {
                '$set': {
                    'data': data
                }
            }
        )
        return self.json()

    @classmethod
    def find_by_username(cls, username):
        user = UserModel.find_by_username(username)
        return cls.find_by_user_model(user)

    @classmethod
    def find_by_userid(cls, userid):
        user = UserModel.find_by_id(userid)
        return cls.find_by_user_model(user)

    @classmethod
    def find_by_user_model(cls, user: UserModel):
        docs = cls.collection.find({'userid': user.id.__str__()})
        events = list()
        for doc in docs:
            event = EventModel(userid=user.id, data=doc['data'], user=user)
            event.id = doc['_id']
            events.append(event)
        return events

    @classmethod
    def find_by_id(cls, id):
        doc = cls.collection.find_one({'_id': id})
        event = EventModel(userid=doc['userid'], data=doc['data'])
        event.id = doc['_id']
        return event
