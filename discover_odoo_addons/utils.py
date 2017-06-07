# -*- coding: utf-8 -*-

import ast
import operator
import os
import sys

_get_name = operator.attrgetter('name')
PY3 = sys.version_info.major == 3
MANIFEST_NAMES = frozenset([
    '__manifest__',
    '__odoo__',
    '__openerp__',
    '__terp__',
])


if PY3:
    basestring = (str, bytes)


class OdooAddon(object):

    def __init__(self, addon_path, manifest_filename):
        super(OdooAddon, self).__init__()
        self._name = None
        self._installable = None
        self.path = addon_path
        self.manifest_filename = manifest_filename

    def __str__(self):
        return self.name

    def __nonzero__(self):
        return self.__bool__()

    def __bool__(self):
        return self.installable

    @property
    def manifest_path(self):
        return os.path.join(self.path, self.manifest_filename)

    @property
    def name(self):
        if self._name is None:
            self._name = os.path.basename(self.path)
        return self._name

    @property
    def installable(self):
        if self._installable is None:
            self._installable = is_installable(self.manifest_path)
        return self._installable


def walk_addons(addon_dir, follow_links=False, manifest_names=MANIFEST_NAMES):
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


def discover_addons(addon_dirs, excluded=frozenset(), follow_links=False,
                    show_all=False):
    if isinstance(addon_dirs, basestring):
        addon_dirs = [addon_dirs]
    for addon_dir in addon_dirs:
        for addon in walk_addons(addon_dir, follow_links=follow_links):
            if addon.name in excluded:
                continue
            if not show_all and not addon:
                continue

            yield addon
