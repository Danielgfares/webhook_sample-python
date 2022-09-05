# from models.event import EventModel
# from models.user import UserModel
#
# usernames = ['user']
# events = ['Type1', 'Type2']
#
# 
# def creat_data():
#     for username in usernames:
#         for i in range(5):
#             userfullname = u'{}{}'.format(username, i)
#
#             user = UserModel(username=userfullname, email='danigfares997@gmail.com')
#             user.hash_password('test123')
#             try:
#                 print(userfullname)
#                 user.save_to_db()
#                 print('created')
#             except:
#                 user = UserModel.find_by_username(username=userfullname)
#             for e in events:
#                 data = "{" \
#                        "'TriggerEventId': '1234'," \
#                        "'TriggerEventDataTime': 'time'," \
#                        "'TriggerEventName': 'name'," \
#                        "'TriggerEventDescription': 'null'," \
#                        " 'FQID': {" \
#                        "'serverID': {" \
#                        "'type': '1234'," \
#                        "'hostname': 'asdsaf'" \
#                        "}," \
#                        "'parentId': 'asdasda'," \
#                        "'ObjectId': 'asdasdqe21'" \
#                        "}" \
#                        "}"
#                 event = EventModel(userref=user.to_dbref(), data=data)
#                 event.save_to_db()
#             print('created 3 events for this user')
#
#
# fun = creat_data
