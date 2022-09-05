import threading
from mail import mail, Message
from flask import current_app


class EmailService:
    __lock = threading.Lock()
    __instance = None

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            with cls.__lock:
                if not cls.__instance:
                    cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        if EmailService.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            EmailService.__instance = self

    def send_email(self, receiver: list[str], subject: str, info: dict):
        TO = receiver
        SUBJECT = subject
        TEXT = ['{0}: {1}\n'.format(column, info['data'][column]) for column in info['data']]
        s = f"Hi dear {info['username']},\nAn event triggered!\nHere it\'s correspondent information:\n\n"
        for i in TEXT:
            s += i
        msg = Message(subject=SUBJECT, sender=current_app.config.get('MAIL_USERNAME'), recipients=TO, body=s)
        mail.send(msg)  # send email


email_service = EmailService.get_instance()
