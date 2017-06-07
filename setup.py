#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import shlex
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        # Import here, cause outside the eggs aren't loaded.
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8'),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


requirements = [
]

test_requirements = [
    'pytest>=3.0.0',
    'pytest-cov>=2.0.0',
]

setup(
    name='discover_odoo_addons',
    version=find_version('discover_odoo_addons', '__init__.py'),
    description='Helper script to find Odoo addons in a directory',
    long_description=long_description,
    author='Naglis Jonaitis',
    author_email='naglis@mailbox.org',
    url='https://github.com/naglis/discover_odoo_addons',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='odoo build ci addons discover',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={
        'test': PyTest,
    },
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'discover_odoo_addons = discover_odoo_addons:main',
        ],
    },
)
