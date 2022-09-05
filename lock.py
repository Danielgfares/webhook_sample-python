import threading


class MyLock(object):
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
        if MyLock.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MyLock.__instance = self
            self.lock = threading.Lock()


lock = MyLock.get_instance()
