#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

"""
python implemention for QDataStream (Qt 4.0 - Qt 5.6)

"""

import sys
import struct
import io

Qt_1_0 = 1
Qt_2_0 = 2
Qt_2_1 = 3
Qt_3_0 = 4
Qt_3_1 = 5
Qt_3_3 = 6
Qt_4_0 = 7
Qt_4_1 = Qt_4_0
Qt_4_2 = 8
Qt_4_3 = 9
Qt_4_4 = 10
Qt_4_5 = 11
Qt_4_6 = 12
Qt_4_7 = Qt_4_6
Qt_4_8 = Qt_4_7
Qt_4_9 = Qt_4_8
Qt_5_0 = 13
Qt_5_1 = 14
Qt_5_2 = 15
Qt_5_3 = Qt_5_2
Qt_5_4 = 16
Qt_5_5 = Qt_5_4
Qt_5_6 = 17

SinglePrecision = 0
DoublePrecision = 1


#懒得支持 Qt 4 以下的格式了。

class Serializer:
    def __init__(self):
        self.buffer = io.BytesIO()
        self.byte_order = "big"
        self.version = Qt_4_6
        self.floatingPointPrecision = DoublePrecision

    def write_char(self, c):
        if len(c) != 1:
            raise Exception("write_char() only accept bytes of length 1.")
        self.buffer.write(c)

    def write_int8(self, i):
        self.buffer.write(struct.pack("b", i))

    def write_bool(self, b):
        self.write_int8(1 if b else 0)

    def write_uint8(self, i):
        self.buffer.write(struct.pack("B", i))

    def write_int16(self, i):
        pattern = ">h" if self.byte_order == "big" else "<h"
        self.buffer.write(struct.pack(pattern, i))

    def write_uint16(self, i):
        pattern = ">H" if self.byte_order == "big" else "<H"
        self.buffer.write(struct.pack(pattern, i))

    def write_int32(self, i):
        pattern = ">i" if self.byte_order == "big" else "<i"
        self.buffer.write(struct.pack(pattern, int(i)))

    def write_uint32(self, i):
        pattern = ">I" if self.byte_order == "big" else "<I"
        self.buffer.write(struct.pack(pattern, int(i)))

    def write_int64(self, i):
        pattern = ">q" if self.byte_order == "big" else "<q"
        self.buffer.write(struct.pack(pattern, int(i)))

    def write_uint64(self, i):
        pattern = ">Q" if self.byte_order == "big" else "<Q"
        self.buffer.write(struct.pack(pattern, int(i)))

    def write_float(self, f):
        if self.version >= Qt_4_6 and self.floatingPointPrecision == DoublePrecision:
            self.write_double(f)
        else:
            pattern = ">f" if self.byte_order == "big" else "<f"
            self.buffer.write(struct.pack(pattern, f))

    def write_double(self, d):
        if self.version >= Qt_4_6 and self.floatingPointPrecision == SinglePrecision:
            self.write_float(d)
        else:
            pattern = ">d" if self.byte_order == "big" else "<d"
            self.buffer.write(struct.pack(pattern, d))

    def write_bytes(self, bs):
        if not bs:
            self.write_uint32(0xffffffff)
            return
        self.write_uint32(len(bs))
        self.buffer.write(bs)

    def write_raw_bytes(self, bs):
        self.buffer.write(bs)

    def write_string(self, s):
        if not s:
            self.write_bytes(b"")
            return
        if self.byte_order == "big":
            self.write_bytes(s.encode("utf-16be"))
        else:
            self.write_bytes(s.encode("utf-16le"))

    def write_map(self, d, key_type_or_func, value_type_or_func):
        self.write_uint32(len(d))
        for k, v in d.items():
            if hasattr(key_type_or_func, "__call__"):
                key_type_or_func(self, k)
            else:
                self.write(key_type_or_func, k)
            if hasattr(value_type_or_func, "__call__"):
                value_type_or_func(self, v)
            else:
                self.write(value_type_or_func, v)

    def write_list(self, l, element_type_or_func):
        self.write_uint32(len(l))
        if hasattr(element_type_or_func, "__call__"):
            for e in l:
                element_type_or_func(self, e)
        else:
            for e in l:
                self.write(element_type_or_func, e)

    def write(self, vt, v):
        return {
            "int8": self.write_int8,
            "uint8": self.write_uint8,
            "int16": self.write_int16,
            "uint16": self.write_uint16,
            "int32": self.write_int32,
            "uint32": self.write_uint32,
            "int64": self.write_int64,
            "uint64": self.write_uint64,
            "float": self.write_float,
            "double": self.write_double,
            "str": self.write_string,
            "bytes": self.write_bytes,
            "bool": self.write_bool,
        }[vt](v)

    def get_value(self):
        return self.buffer.getvalue()


class Deserializer:
    def __init__(self, buffer):
        self.buffer = io.BytesIO(buffer)
        self.byte_order = "big"
        self.double = False
        self.version = Qt_4_6
        self.floatingPointPrecision = DoublePrecision

    def read_int8(self):
        i, = struct.unpack("b", self.buffer.read(1))
        return i

    def read_bool(self):
        return bool(self.read_int8())

    def read_uint8(self):
        i, = struct.unpack("B", self.buffer.read(1))
        return i

    def read_int16(self):
        pattern = ">h" if self.byte_order == "big" else "<h"
        i, = struct.unpack(pattern, self.buffer.read(2))
        return i

    def read_uint16(self):
        pattern = ">H" if self.byte_order == "big" else "<H"
        i, = struct.unpack(pattern, self.buffer.read(2))
        return i

    def read_int32(self):
        pattern = ">i" if self.byte_order == "big" else "<i"
        i, = struct.unpack(pattern, self.buffer.read(4))
        return i

    def read_uint32(self):
        pattern = ">I" if self.byte_order == "big" else "<I"
        i, = struct.unpack(pattern, self.buffer.read(4))
        return i

    def read_int64(self):
        pattern = ">q" if self.byte_order == "big" else "<q"
        i, = struct.unpack(pattern, self.buffer.read(8))
        return i

    def read_uint64(self):
        pattern = ">Q" if self.byte_order == "big" else "<Q"
        i, = struct.unpack(pattern, self.buffer.read(8))
        return i

    def read_float(self):
        if self.version >= Qt_4_6 and self.floatingPointPrecision == DoublePrecision:
            return self.read_double()
        else:
            pattern = ">f" if self.byte_order == "big" else "<f"
            f, = struct.unpack(pattern, self.buffer.read(4))
            return f

    def read_double(self):
        if self.version >= Qt_4_6 and self.floatingPointPrecision == SinglePrecision:
            return self.read_float()
        else:
            pattern = ">d" if self.byte_order == "big" else "<d"
            d, = struct.unpack(pattern, self.buffer.read(8))
            return d

    def read_bytes(self):
        length = self.read_uint32()
        if length == 0xffffffff:
            return b""
        return self.buffer.read(length)

    def read_raw_bytes(self, length):
        return self.buffer.read(length)

    def read_string(self):
        buf = self.read_bytes()
        if self.byte_order == "little":
            return buf.decode("utf-16le")
        else:
            return buf.decode("utf-16be")

    def read_list(self, element_type_or_func):
        length = self.read_uint32()
        l = []
        if hasattr(element_type_or_func, "__call__"):
            for i in range(length):
                l.append(element_type_or_func(self))
        else:
            for i in range(length):
                l.append(self.read(element_type_or_func))
        return l

    def read_map(self, key_type_or_func, value_type):
        length = self.read_uint32()
        d = {}
        for i in range(length):
            if hasattr(key_type_or_func, "__call__"):
                key = key_type_or_func(self)
            else:
                key = self.read(key_type_or_func)
            if hasattr(key_type_or_func, "__call__"):
                value = key_type_or_func(self)
            else:
                value = self.read(value_type)
            d[key] = value
        return d

    def read(self, vt):
        return {
            "int8": self.read_int8,
            "uint8": self.read_uint8,
            "int16": self.read_int16,
            "uint16": self.read_uint16,
            "int32": self.read_int32,
            "uint32": self.read_uint32,
            "int64": self.read_int64,
            "uint64": self.read_uint64,
            "float": self.read_float,
            "double": self.read_double,
            "str": self.read_string,
            "bytes": self.read_bytes,
            "bool": self.read_bool,
        }[vt]()


if __name__ == "__main__":
    try:
        from PyQt4.QtCore import QDataStream, QByteArray, QBuffer, QIODevice
    except ImportError:
        sys.exit(1)

    serializer = Serializer()
    #serializer.byte_order = "little"
    serializer.write_int8(64)
    serializer.write_uint8(0xee)
    serializer.write_int16(64)
    serializer.write_uint16(0xffee)
    serializer.write_int32(0x100020)
    serializer.write_uint32(0xffeeddcc)
    serializer.write_int64(0x1000200040)
    serializer.write_uint64(0xffeeddccbbaa9988)
    serializer.write_float(64)
    serializer.write_bytes(b"fish is here.")
    serializer.write_string("实在太帅了。")
    h1 = serializer.get_value()

    buf = QByteArray()
    d = QDataStream(buf, QIODevice.WriteOnly)
    #d.setByteOrder(QDataStream.LittleEndian)
    d.setVersion(QDataStream.Qt_4_6)
    d.writeInt8(chr(64))
    d.writeUInt8(chr(0xee))
    d.writeInt16(6  4)
    d.writeUInt16(0xffee)
    d.writeInt32(0x100020)
    d.writeUInt32(0xffeeddcc)
    d.writeInt64(0x1000200040)
    d.writeUInt64(0xffeeddccbbaa9988)
    d.writeFloat(64)
    d.writeBytes(b"fish is here.")
    d.writeQString("实在太帅了。")
    h2 = bytes(buf)

    print(repr(h1))
    print(repr(h2))
    print(h1 == h2)
