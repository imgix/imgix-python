""" test runner: python -m imgix.test """
# pylint: disable=C0111,W0312
import unittest

def runtests():
	loader = unittest.defaultTestLoader
	suite = loader.discover("./", "test_*.py")
	runner = unittest.TextTestRunner(verbosity=2)
	runner.run(suite)

if __name__ == "__main__":
	runtests()
