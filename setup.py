from imgix._version import __version__
from setuptools import setup

setup(
    name='imgix',
    version=__version__,
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
