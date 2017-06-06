# -*- coding: utf-8 -*-

import ast
import collections
import os


# OdooAddon = collections.namedtuple(
    # 'OdooAddon', ['name', 'manifest_filename'])
MANIFEST_NAMES = frozenset([
    '__manifest__',
    '__odoo__',
    '__openerp__',
    '__terp__',
])


class OdooAddon(object):

    def __init__(self, addon_path, manifest_filename):
        super(OdooAddon, self).__init__()
        self._name = None
        self._installable = None
        self.addon_path = addon_path
        self.manifest_filename = manifest_filename

    @property
    def manifest_path(self):
        return os.path.join(self.addon_path, self.manifest_filename)

    @property
    def name(self):
        if self._name is None:
            self._name = os.path.basename(self.addon_path)
        return self._name

    @property
    def installable(self):
        if self._installable is None:
            self._installable = is_installable(self.manifest_path)
        return self._installable


def find_addons(addon_dir, follow_links=True, manifest_names=MANIFEST_NAMES):
    manifest_filenames = frozenset('{0}.py'.format(n) for n in manifest_names)
    for dirpath, _, filenames in os.walk(addon_dir, followlinks=follow_links):
        filenames = set(filenames)
        for manifest_name in manifest_filenames:
            if manifest_name in filenames:
                yield OdooAddon(dirpath, manifest_name)


def is_installable(manifest_path):
    with open(manifest_path) as f:
        manifest = ast.literal_eval(f.read())
        if isinstance(manifest, dict):
            if not manifest.get('installable', True):
                return False
    return True


def parse_names(string, sep=','):
    for name in string.split(sep):
        name = name.strip()
        if name:
            yield name
