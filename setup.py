#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import io
import re

from setuptools import setup

with io.open("imgix/_version.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with codecs.open('README.md', encoding='utf-8') as fp:
    readme = fp.read()
with codecs.open('CHANGELOG.md', encoding='utf-8') as fp:
    changelog = fp.read()

test_require = [
    'pytest',
    'pytest-cov',
    'flake8',
]

setup(
    name='imgix',
    version=version,
    author='imgix',
    author_email='support@imgix.com',
    packages=['imgix'],
    url='https://github.com/imgix/imgix-python',
    license='BSD-2-Clause',
    description='Python client library for imgix.',
    long_description=u'\n\n'.join([readme, changelog]),
    long_description_content_type=u'text/markdown',
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'future',
    ],
    setup_requires=['pytest-runner'],
    extras_require={
        'dev': ['tox'],
        'test': test_require,
    },
    tests_require=test_require,
)
