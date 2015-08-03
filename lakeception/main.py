# -*- coding: utf-8 -*-

import argparse
import logging

from lakeception import game


def _parse_args(args):
    """
    Parses arguments from a argv format.

    Parameters
    ----------
    args : list of str

    Returns
    -------
    argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="lakeception",
        description="Aww yeah, boats!",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Increase verbosity of output.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Turn on debugging mode.",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test the client lauches without issue."
    )
    return parser.parse_args(args)


def main(args):
    args = _parse_args(args)

    if verbose or debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        filename="lakeception.log",
        level=level,
    )

    g = game.Game(debug=args.debug)

    if args.test:
        return

    while not g.quitting:
        g.tick()


if __name__ == "__main__":
    main(sys.argv[1:])
