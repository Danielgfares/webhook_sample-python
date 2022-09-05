import hashlib
import hmac
message = '{"TriggerEventId": "1234","TriggerEventDataTime": "time", "TriggerEventName": "name", "TriggerEventDescription": "null", "FQID": {"serverID": {"type": "1234", "hostname": "asdsaf"}, "parentId": "asdasda", "ObjectId": "asdasdqe21"}}'
signature = 'sha256={0}'.format(
        hmac.new(
            bytes('test123', 'utf-8'),
            bytes(str(eval(message)), 'utf-8'),
            hashlib.sha256
        ).hexdigest()
    )
print(signature)
