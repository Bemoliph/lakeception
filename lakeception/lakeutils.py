# -*- coding: utf-8 -*-

import logging
import os
import random

from const import PROJECT

LOGGER = logging.getLogger()


def get_abs_asset_path(asset_path):
    """
    Resolves a relative asset path to an absolute file path.

    :param asset_path: Location of file, relative to assets folder.
    :return: Absolute file path to asset.
    """
    if os.path.isabs(asset_path):
        return asset_path
    else:
        return os.path.normpath(os.path.join(os.path.abspath(u'.'), PROJECT.ASSETS_FOLDER, asset_path))


def asset_exists(asset_path):
    """
    Determines if asset exists at given path.

    :param asset_path: Location of file, relative to assets folder.
    :return: True if asset exists, False if asset doesn't exist.
    """
    exists = os.path.isfile(get_abs_asset_path(asset_path))
    
    if not exists:
        LOGGER.warning(u'Referenced missing asset: %s', asset_path)
    
    return exists


# See "Giving up the temporary list"
# http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
def get_weighted_random_choice(ordered_weights):
    rnd = random.random() * sum(ordered_weights)
    for index, weight in enumerate(ordered_weights):
        rnd -= weight
        if rnd < 0:
            return index
