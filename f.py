from cryptography.fernet import Fernet
import threading
from flask import Flask


class F(object):
    f: Fernet = None
    __key__: bytes = None
    app: Flask = None
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
        if F.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            F.__instance = self

    def init_app(self, app):
        if not app or not isinstance(app, Flask):
            raise TypeError("Invalid Flask application instance")
        self.app = app
        app.extensions = getattr(app, "extensions", {})
        if not self.f:
            self.initiate()

    @property
    def get_f(self):
        if not self.f:
            self.initiate()
        return self.f

    def initiate(self):
        self.__key__ = self.app.config.get('F_KEY').encode('utf-8')
        self.f = Fernet(self.__key__)


f = F()
