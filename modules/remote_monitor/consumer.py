import threading
import time
# import random


class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, que=None, db=None, cols=None,
                 args=(), kwargs=None, verbose=None):
        super(self.__class__, self).__init__()
        self.target = target
        self.name = name
        self.q = que
        self.database = db
        self.columns = cols

    def run(self):
        while True:
            if not self.q.empty():
                item = self.q.get()
                self.database.write(self.columns, item)
                time.sleep(10)
