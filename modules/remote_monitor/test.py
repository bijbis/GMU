# from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
# import time
# import socket
# from pymodbus3.constants import Endian
# from pymodbus3.payload import BinaryPayloadDecoder
#
#
# NUMBER_OF_REGS = 2
# # client = ModbusClient('120.157.57.189', port=502)
# ip = socket.gethostbyname('203.59.95.40')
# client = ModbusClient(ip, port=502)
# client.connect()
#
# while True:
#     rr2 = client.read_holding_registers(40091, NUMBER_OF_REGS, unit=1)
#     decoder = BinaryPayloadDecoder.from_registers(rr2.registers, endian=Endian.Big).decode_32bit_float() * 0.001
#     print(decoder)
#     time.sleep(2)
import urllib.request
pp = urllib.request.urlopen('http://203.59.95.40:9080/HOSTLINK/RVIY*').read()
# print(int(pp.split('RVI')[1].split('*')[0], 16) * 0.001)
print(int(pp.decode("utf-8").split('RVI')[1].split('*')[0], 16) * 0.001)
