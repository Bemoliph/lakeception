# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

import game

from const import PROJECT

LOGGER = logging.getLogger()


def _parse_args(args):
    u"""
    Parses arguments from an argv format.

    :param args: list of str
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog=PROJECT.NAME.lower(),
        description=u'{} v{} - {}'.format(
            PROJECT.NAME,
            PROJECT.VERSION,
            PROJECT.DESC,
        ),
    )
    
    parser.add_argument(
        u'-v', u'--verbose',
        action=u'store_true',
        help=u'Increases verbosity of logging from INFO to DEBUG levels.',
    )
    
    parser.add_argument(
        u'--debug',
        action=u'store_true',
        help=u'Enables developer tools and DEBUG level logging.',
    )
    
    parser.add_argument(
        u'--test',
        action=u'store_true',
        help=u'Tests that the client launches without issue.',
    )
    
    return parser.parse_args(args)


def log_unhandled_exceptions(func):
    u"""Catches unhandled exceptions to make sure they get logged."""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            LOGGER.exception(u'%s has crashed from an Unhandled Exception!', PROJECT.NAME)
    
    return wrapper


# Use wrapper for crash logging so it happens regardless of how the game is run.
# Without this, we'd have to duplicate the try/except in `__main__.py` to cover
# `python -m lakeception` vs `python lakeception/main.py` vs `bin/lakeception`.
@log_unhandled_exceptions
def run(raw_args):
    u"""Launches the game.  Entry point to all code."""
    args = _parse_args(raw_args)
    
    # Configure logging
    if args.verbose or args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logging.basicConfig(
        filename=u'{}.log'.format(PROJECT.NAME),
        format=u'%(asctime)s - %(levelname)8s - %(pathname)s:%(lineno)d - %(message)s',
        datefmt=u'%Y-%m-%d %H:%M:%S',
        level=log_level,
    )
    
    LOGGER.info(u'Starting %s %s!', PROJECT.NAME, PROJECT.VERSION)
    g = game.Game()
    
    if args.test:
        LOGGER.info(u'Stopping: Start-up test completed successfully.')
        return
    else:
        LOGGER.debug(u'Beginning main game loop.')
        g.start()
        
        LOGGER.info(u'Stopping %s.', PROJECT.NAME)

if __name__ == u'__main__':
    # Fix current working directory so assets aren't "missing" when main.py
    # is run directly from arbitrary working directories.
    os.chdir(os.path.join(os.path.dirname(__file__), u'..'))
    
    run(sys.argv[1:])
