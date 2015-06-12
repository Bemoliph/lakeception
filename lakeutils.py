# -*- coding: utf-8 -*-
import struct

def hex2rgb(hexStr):
    return struct.unpack('BBB', hexStr.decode('hex'))

def hex2rgba(hexStr, alpha):
    return hex2rgb(hexStr) + (alpha,)
