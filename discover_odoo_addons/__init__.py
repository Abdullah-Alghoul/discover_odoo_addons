# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import operator
import sys

from .utils import (
    OdooAddon,
    discover_addons,
    walk_addons,
    is_installable,
    parse_names,
)

__version__ = '0.1dev'
LOG = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addon_dir', nargs='*', default='.')
    parser.add_argument(
        '-a', '--all',
        dest='show_not_installable',
        action='store_true',
        help='list all addons, even those that are not installable',
    )
    parser.add_argument(
        '-e', '--exclude',
        action='append',
        help='comma-separated list of addons to exclude.'
             'Can be used multiple times.',
    )
    parser.add_argument(
        '-s', '--separator',
        default=',',
        help='separator symbol used for joining addon names. '
             'Default: %(default)s',
    )
    parser.add_argument(
        '-p', '--print',
        default='name',
        choices=['name', 'path'],
        help='addon attribute to print. Choices: %(choices)s. '
             'Default: %(default)s.',
    )
    parser.add_argument(
        '-l', '--follow-links',
        action='store_true',
        help='follow symbolic links when searching for addons '
             '(if OS supports it).',
    )
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logging.basicConfig(level=logging.INFO)
    args = get_parser().parse_args(argv)

    excluded = set()
    if args.exclude:
        for string in args.exclude:
            excluded |= set(parse_names(string))
        LOG.info('Excluding addons: %s', ', '.join(excluded))

    addons = discover_addons(
        args.addon_dir,
        excluded=excluded,
        follow_links=args.follow_links,
        show_all=args.show_not_installable,
    )

    print(args.separator.join(map(operator.attrgetter(args.print), addons)))


__all__ = [
    'OdooAddon',
    'discover_addons',
    'is_installable',
    'main',
    'parse_names',
    'walk_addons',
]
