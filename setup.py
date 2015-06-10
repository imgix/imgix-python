import re

from setuptools import setup


metadata = dict(
    re.findall("__([a-z]+)__ = '([^']+)'", open('imgix/__init__.py').read()))


setup(
    name='imgix',
    version=metadata['version'],
    author='imgix',
    author_email='support@imgix.com',
    packages=['imgix'],
    url='http://www.imgix.com/',
    license='MIT',
    description='Python client library for imgix.',
    )
