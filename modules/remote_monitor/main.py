from producer import ProducerThread
from consumer import ConsumerThread
from queue import Queue
from db import Influx
from SeriesHelper import RemoteMonitor
import time


if __name__ == '__main__':
    q = Queue()
    database = Influx(database='influxDB', user='root', passcode='root', dbname='gmu',
                      port=8086, host='localhost')
    columns = ['current_A',
               'current_B',
               'current_C',
               'current_Avg',
               'voltage_AB',
               'voltage_BC',
               'voltage_AC',
               'voltage_Avg',
               'power',
               'plc_power'
               ]
    RemoteMonitor.Meta.client = database.db
    RemoteMonitor.Meta.series_name = 'remote_monitor'
    RemoteMonitor.Meta.fields = columns
    p = ProducerThread(name='ModbusPull', que=q)
    c = ConsumerThread(name='InfluxDBwriter', que=q, db=database, cols=columns)
    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
