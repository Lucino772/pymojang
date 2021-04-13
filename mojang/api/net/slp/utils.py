import struct
import io

__all__ = [
    '_write_varint',
    '_read_varint',
    '_write_string',
    '_read_string',
    '_write_short',
    '_read_short',
    '_write_long',
    '_read_long'
]

def _write_varint(value: int, buffer: io.BufferedWriter):
    while True:
        byte = value & 0x7f
        value >>= 7

        if value > 0:
            byte |= 0x80
        
        buffer.write(struct.pack('B', byte))
        
        if value == 0:
            break

def _read_varint(buffer: io.BufferedReader):
    val = 0
    for i in range(5):
        byte = buffer.read(1)

        val |= (ord(byte) & 0x7f) << (7*i)
        
        if ord(byte) & 0x80 == 0:
            break

    return val

def _write_string(value: str, buffer: io.BufferedWriter):
    encoded = value.encode('utf-8')
    _write_varint(len(encoded), buffer)
    buffer.write(encoded)

def _read_string(buffer: io.BufferedReader):
    size = _read_varint(buffer)
    encoded = buffer.read(size)
    return encoded.decode('utf-8')

def _write_short(value: int, buffer: io.BufferedWriter):
    buffer.write(struct.pack('H', value))

def _read_short(buffer: io.BufferedReader):
    return struct.unpack('H', buffer.read(2))[0]

def _write_long(value: int, buffer: io.BufferedWriter):
    buffer.write(struct.pack('q', value))

def _read_long(buffer: io.BufferedReader):
    return struct.unpack('q', buffer.read(8))[0]
