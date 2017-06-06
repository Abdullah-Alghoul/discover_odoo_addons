# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import itertools
import logging
import operator
import sys

from .utils import OdooAddon, find_addons, is_installable


__version__ = '0.1dev'
LOG = logging.getLogger(__name__)
get_name = operator.attrgetter('name')
get_path = operator.attrgetter('addon_path')


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
    return parser


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    logging.basicConfig(level=logging.INFO)
    args = get_parser().parse_args(argv)

    found_addons = set()
    for addon_dir in args.addon_dir:
        found_addons |= set(find_addons(addon_dir))

    excluded = set()
    if args.exclude:
        for string in args.exclude:
            excluded |= set(utils.parse_names(string))

    if excluded:
        LOG.info('Excluding addons: %s', ', '.join(excluded))
        found_addons = {a for a in found_addons if a.name not in excluded}

    if not args.show_not_installable:
        not_installable = set(itertools.filterfalse(
            lambda a: a.installable, found_addons))
        if not_installable:
            LOG.info(
                'Found not installable addons: %s', ', '.join(
                    map(get_name, not_installable)))
            found_addons -= not_installable
    getters = {
        'name': get_name,
        'path': get_path,
    }
    print(args.separator.join(map(getters[args.print], found_addons)))


__all__ = [
    'OdooAddon',
    'find_addons',
    'is_installable',
    'main',
]
