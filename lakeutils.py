# -*- coding: utf-8 -*-
import struct

def hex2rgb(hex_str):
    return struct.unpack('BBB', hex_str.decode('hex'))
