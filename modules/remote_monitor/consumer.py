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
            if not self.q[0].empty() and not self.q[1].empty():
                item_remote_monitor = self.q[0].get()
                item_plc_monitor = self.q[1].get()
                self.database.write(self.columns[0], item_remote_monitor, 'remote')
                self.database.write(self.columns[1], item_plc_monitor, 'plc')
                time.sleep(10)
