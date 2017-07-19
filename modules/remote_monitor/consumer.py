from db import Influx
from SeriesHelper import RemoteMonitor
import numpy as np
# import threading
# import time
# import queue

# Some General Configs #
database = Influx(database='influxDB', user='root', passcode='root', dbname='test',
                  port=8086, host='localhost')
columns = ['current', 'power', 'voltage']
RemoteMonitor.Meta.client = database.db
RemoteMonitor.Meta.series_name = 'remote_monitor'
RemoteMonitor.Meta.fields = columns

data = np.arange(1, 10).reshape(3, 3)


# class ConsumerThread(threading.Thread):
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs=None, verbose=None):
#         super(ConsumerThread, self).__init__()
#         self.target = target
#         self.name = name
#
#     def

# for each in data:
#     print(each)
#     # database.write(each)
database.write(columns, data)
