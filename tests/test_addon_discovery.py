# -*- coding: utf-8 -*-

import os

import pytest

from discover_odoo_addons import find_addons, is_installable


@pytest.fixture
def repo():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'dummy_repo')


def test_is_installable_with_not_installable_addon(repo):
    addon_name = 'not_installable_addon'
    manifest_path = os.path.join(repo, addon_name, '__manifest__.py')
    assert is_installable(manifest_path) is False


def test_find_addons(repo):
    addons = list(find_addons(repo))
    assert len(addons) == 2
