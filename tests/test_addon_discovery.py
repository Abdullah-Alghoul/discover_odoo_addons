# -*- coding: utf-8 -*-

import os

import pytest

from discover_odoo_addons import (
    OdooAddon,
    discover_addons,
    is_installable,
    main,
    parse_names,
    walk_addons,
)


@pytest.fixture
def repo():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'dummy_repo')


def test_is_installable_with_not_installable_addon(repo):
    addon_name = 'not_installable_addon'
    manifest_path = os.path.join(repo, addon_name, '__manifest__.py')
    assert is_installable(manifest_path) is False


def test_walk_addons(repo):
    assert len(list(walk_addons(repo))) == 2


def test_discover_addons_show_all_False_finds_one_addon(repo):
    assert len(list(discover_addons(repo, show_all=False))) == 1


def test_discover_addons_exclude_simple_finds_no_addons(repo):
    assert list(discover_addons(repo, excluded={'simple', })) == []


@pytest.mark.parametrize('test_input, expected', [
    ('a,,b', ['a', 'b']),
    ('a,b,', ['a', 'b']),
    (',a,b, ', ['a', 'b']),
])
def test_parse_names(test_input, expected):
    assert list(parse_names(test_input)) == expected


def test_OdooAddon(repo):
    addon1_name = 'not_installable_addon'
    addon2_name = 'simple'
    addon1_path = os.path.join(repo, addon1_name)
    addon2_path = os.path.join(repo, addon2_name)
    addon1 = OdooAddon(addon1_path, '__manifest__.py')
    addon2 = OdooAddon(addon2_path, '__manifest__.py')

    assert bool(addon1) is False
    assert bool(addon2) is True

    assert str(addon1) == addon1_name
    assert str(addon2) == addon2_name

    assert addon1.manifest_path == os.path.join(addon1_path, '__manifest__.py')


@pytest.mark.parametrize('args, expected_addons', [
    ([], ['simple']),
    (['--exclude', 'simple'], []),
    (['--all'], ['simple', 'not_installable_addon']),
])
def test_main_prints_module_names(args, expected_addons, repo, capfd):
    args.extend([
        '--separator',
        '\n',
        repo,
    ])
    main(args)
    out, _ = capfd.readouterr()
    addons = out.strip().splitlines()
    assert sorted(addons) == sorted(expected_addons)
