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
    url='https://github.com/imgix/imgix-python',
    license='MIT',
    description='Python client library for imgix.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    )
