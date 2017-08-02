from producer import ProducerThread
from consumer import ConsumerThread
from queue import Queue
from db import Influx
from SeriesHelper import RemoteMonitor, PlcMonitor
import time


if __name__ == '__main__':
    q_remote_monitor = Queue()
    q_plc_monitor = Queue()
    database = Influx(database='influxDB', user='root', passcode='root', dbname='gmu',
                      port=8086, host='localhost')
    columns1 = ['current_A',
                'current_B',
                'current_C',
                'current_Avg',
                'voltage_AB',
                'voltage_BC',
                'voltage_AC',
                'voltage_Avg',
                'power'
               ]

    columns2 = ['battery_voltage',
                'plc_voltage',
                'charging_current',
                'plc_power'
                ]
    RemoteMonitor.Meta.client = database.db
    RemoteMonitor.Meta.series_name = 'remote_monitor'
    RemoteMonitor.Meta.fields = columns1

    PlcMonitor.Meta.client = database.db
    PlcMonitor.Meta.series_name = 'gmu_monitor'
    PlcMonitor.Meta.fields = columns2

    p = ProducerThread(name='ModbusPull', que=[q_remote_monitor, q_plc_monitor])
    c = ConsumerThread(name='InfluxDBwriter', que=[q_remote_monitor, q_plc_monitor], db=database, cols=[columns1, columns2])
    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
