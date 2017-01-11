# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys

import const
import game

LOGGER = logging.getLogger(u'{}.main'.format(const.PROJECT.NAME))

def _parse_args(args):
    '''
    Parses arguments from a argv format.

    Parameters
    ----------
    args : list of str

    Returns
    -------
    argparse.ArgumentParser
    '''
    parser = argparse.ArgumentParser(
        prog=const.PROJECT.NAME.lower(),
        description=u'{} {} - {}'.format(
            const.PROJECT.NAME,
            const.PROJECT.VERSION,
            const.PROJECT.DESC,
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
    '''
    Catches unhandled exceptions to make sure they get logged.
    '''
    
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            LOGGER = logging.getLogger('{}.main'.format(const.PROJECT.NAME))
            LOGGER.exception(u'%s has crashed from an Unhandled Exception!', const.PROJECT.NAME)
    
    return wrapper

# Use wrapper for crash logging so it happens regardless of how the game is run.
# Without this, we'd have to duplicate the try/except in __main__.py to cover
# `python -m lakeception` vs `python lakeception/main.py` vs `bin/lakeception`.
@log_unhandled_exceptions
def run(args):
    args = _parse_args(args)
    
    # Configure logging
    if args.verbose or args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logging.basicConfig(
        filename=u'{}.log'.format(const.PROJECT.NAME),
        format=u'%(asctime)s - %(levelname)8s - %(name)s - %(message)s',
		datefmt=u'%Y-%m-%d %H:%M:%S',
        level=log_level,
    )
    
    LOGGER.info(u'Starting %s %s!', const.PROJECT.NAME, const.PROJECT.VERSION)
    g = game.Game()
    
    if args.test:
        LOGGER.info(u'Stopping: Start-up test completed successfully.')
        return
    else:
        LOGGER.debug(u'Beginning main game loop.')
        g.start()
        
        LOGGER.info(u'Stopping: User requested to quit.')

if __name__ == u'__main__':
    # Fix current working directory so assets aren't "missing" when main.py
    # is run directly from arbitrary working directories.
    os.chdir(os.path.join(os.path.dirname(__file__), u'..'))
    
    run(sys.argv[1:])
