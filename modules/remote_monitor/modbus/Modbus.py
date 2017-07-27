from pymodbus3.client.sync import ModbusTcpClient as ModbusClient
from pymodbus3.constants import Endian
from pymodbus3.payload import BinaryPayloadDecoder
import socket
import struct


class Modbus:
    def __init__(self, uri='localhost', port=502):
        self.host = socket.gethostbyname(uri)
        self.client = ModbusClient(self.host, port=port)
        self.client.connect()
        # // TODO implement a fallback
        # if not self.client:
        #     raise RuntimeError('Error establishing connection with uri {}'.format(uri))

    def _read(self, response, typ='Float32', device='Meter', scalar=1.0):
        if typ == 'Float32':
            if device == 'Meter':
                raw = struct.pack('>HH', response.get_register(1), response.get_register(0))
                return float(struct.unpack('>f', raw)[0]) * scalar
            elif device == 'GMU':
                return BinaryPayloadDecoder.from_registers(response.registers,
                                                           endian=Endian.Big).decode_32bit_float() * scalar

    def read(self, register, n, unit=1, typ='Float32', device='Meter', scalar=1.0):
        response = self.client.read_holding_registers(register, n, unit=unit)
        return self._read(response, typ, device, scalar)

    def readN(self, registers, n, unit=1):
        # // TODO implement reading multiple registers
        pass
