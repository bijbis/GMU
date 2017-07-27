import threading
import struct
import time
from modbus import Modbus
from pymodbus3.exceptions import ModbusException
from plc import hotlink
import sys
import os


class ProducerThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, que=None,
                 args=(), kwargs=None, verbose=None):
        super(self.__class__, self).__init__()
        self.target = target
        self.name = name
        self.q = que

    def run(self):
        # modbus = Modbus.Modbus('paulharrison.hopto.org')
        modbus = Modbus.Modbus('203.59.95.40')
        while True:
            item = []
            try:
                # Order: [current, power, voltage]
                # current_avg = modbus.read(3008, 2)  # 3008 stores average current
                # power_avg = modbus.read(3057, 2)    # 3057 stores average power
                # voltage_avg = modbus.read(3024, 2)  # 3024 stores average voltage

                cur_A = modbus.read(40073, 2, device='GMU')
                cur_B = modbus.read(40075, 2, device='GMU')
                cur_C = modbus.read(40077, 2, device='GMU')
                cur_Avg = modbus.read(40071, 2, device='GMU')
                vol_AB = modbus.read(40079, 2, device='GMU')
                vol_BC = modbus.read(40081, 2, device='GMU')
                vol_AC = modbus.read(40083, 2, device='GMU')
                vol_Avg = (vol_AB + vol_BC + vol_AC) / 3.0
                power = modbus.read(40091, n=2, device='GMU', scalar=0.001)
                item.append(cur_A)
                item.append(cur_B)
                item.append(cur_C)
                item.append(cur_Avg)
                item.append(vol_AB)
                item.append(vol_BC)
                item.append(vol_AC)
                item.append(vol_Avg)
                item.append(power)
                hlink = hotlink.Hotlink('http://203.59.95.40:9080/HOSTLINK/RVIY*')
                item.append(hlink.data)
            except struct.error:
                continue
            except ModbusException:
                print('Modbus I/O exception', file=sys.stderr)
                os._exit(1)
            self.q.put(item)
            time.sleep(4)
