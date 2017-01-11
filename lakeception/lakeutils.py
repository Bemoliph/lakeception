# -*- coding: utf-8 -*-

import logging
import os

import const

LOGGER = logging.getLogger(u'{}.utils'.format(const.PROJECT.NAME))

def get_file_path(asset_path):
    '''Resolves a relative asset path to an absolute path.'''
    if os.path.isabs(asset_path):
        return asset_path
    else:
        return os.path.join(os.path.abspath("."), asset_path)

def asset_exists(asset_path):
    '''Determines if asset exists at given path.'''
    exists = os.path.isfile(get_file_path(asset_path))
    
    if not exists:
        LOGGER.warning(u'Referenced missing asset: %s', asset_path)
    
    return exists

def hex_to_rgba(hex_value):
    # (r, g, b, a)
    return (hex_value >> 24, hex_value >> 16 & 255, hex_value >> 8 & 255, hex_value & 255)

def hex_to_rgb(hex_value):
    # (r, g, b)
    return (hex_value >> 16, hex_value >> 8 & 255, hex_value & 255)