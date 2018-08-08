#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

from imgix._version import __version__
from setuptools import setup

with codecs.open('README.rst', encoding='utf-8') as fp:
    readme = fp.read()
with codecs.open('CHANGELOG.rst', encoding='utf-8') as fp:
    changelog = fp.read()


setup(
    name='imgix',
    version=__version__,
    author='imgix',
    author_email='support@imgix.com',
    packages=['imgix'],
    url='https://github.com/imgix/imgix-python',
    license='BSD-2-Clause',
    description='Python client library for imgix.',
    long_description=u'\n\n'.join([readme, changelog]),
    long_description_content_type=u'text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
    )
