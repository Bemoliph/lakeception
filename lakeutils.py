# -*- coding: utf-8 -*-
import struct

def hex2rgb(hex_str):
    return struct.unpack('BBB', hex_str.decode('hex'))

def hex2rgba(hex_str, alpha):
    return hex2rgb(hex_str) + (alpha,)
