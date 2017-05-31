# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import ast
import collections
import logging
import os


LOG = logging.getLogger(__name__)
SearchResult = collections.namedtuple(
    'SearchResult', ['addon_name', 'manifest_filename'])
MANIFEST_NAMES = frozenset(['__openerp__', '__manifest__'])


def find_addons(start_dir, follow_links=True, manifest_names=MANIFEST_NAMES):
    manifest_filenames = frozenset(
        map(lambda n: '{0:s}.py'.format(n), manifest_names))
    for dirpath, _, filenames in os.walk(start_dir, followlinks=follow_links):
        filenames = set(filenames)
        for manifest_name in manifest_filenames:
            if manifest_name in filenames:
                addon_name = os.path.basename(dirpath)
                yield SearchResult(
                    addon_name, os.path.join(dirpath, manifest_name))


def is_installable(node):
    if type(node) == ast.Name:
        return node.id == 'True'
    elif type(node) == ast.Str:
        return node.s == 'True'
    else:
        raise TypeError('Unexpected type: %s for node' % type(node))


class ManifestNodeVisitor(ast.NodeVisitor):

    def __init__(self, *args, **kwargs):
        super(ManifestNodeVisitor, self).__init__(*args, **kwargs)
        self.installable = None

    def visit_Dict(self, d):
        installable_key_idx = [
            i for i, k in enumerate(d.keys)
            if type(k) == ast.Str and k.s == 'installable'
        ][:1]
        if installable_key_idx:
            self.installable = is_installable(
                d.values[installable_key_idx[0]])


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_dir', nargs='?', default='.')
    parser.add_argument(
        '-a', '--all',
        dest='show_not_installable',
        action='store_true',
        help='list all addons, even those that are not installable',
    )
    parser.add_argument(
        '-s', '--separator',
        default=',',
        help='separator symbol used for joining addon names. '
             'Default: %(default)s',
    )
    return parser


def main():
    logging.basicConfig(level=logging.INFO)
    args = get_parser().parse_args()

    found_addons = {
        a.addon_name: a.manifest_filename for a in find_addons(args.start_dir)}

    if not args.show_not_installable:
        not_installable = []
        for an, mp in found_addons.items():
            with open(mp) as f:
                node = ast.parse(f.read(), filename=mp)
                visitor = ManifestNodeVisitor()
                visitor.visit(node)
                if visitor.installable is False:
                    not_installable.append(an)
        if not_installable:
            LOG.info(
                'Found not installable addons: %s', ', '.join(not_installable))
            found_addons = {
                k: v
                for k, v in found_addons.items()
                if k not in not_installable
            }
    print(args.separator.join(found_addons))

if __name__ == '__main__':
    main()
