import os
import sys
try:
	from setuptools import setup
except:
	from distutils.core import setup
from distutils.command.build_py import build_py
import blacktip

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

VERSION="0.0.1"

install_requires = []

setup(name='imgix',
	cmdclass={'build_py': build_py},
	version=VERSION,
	description='Python client library for imgix.',
	author='imgix',
	author_email='support@imgix.com',
	url='http://www.imgix.com/',
	packages=['imgix'],
	install_requires=install_requires
)
