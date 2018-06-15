Contributing
============

imgix-python is developed by Imgix and we happily accept contributions.

If you wish to add a new feature or fix a bug:

- Check for open [issues](https://github.com/imgix/imgix-python/issues) or open
  a fresh issue to start a discussion around a feature idea or a bug.
- Fork this repository on Github to start making your changes.
- Write a test which shows that the bug was fixed or that the feature works
  as expected.
- Send a pull request and bug the maintainer until it gets merged and published.
  :) Make sure to add yourself to ``AUTHORS.txt``.


Running the tests
-----------------

To run the tests, simply:
```
tox
```
This will run all tests and check PEP8 compliance. Our test suite runs
continuously on [Travis CI](https://travis-ci.org/imgix/imgix-python) with
every pull request.


Publishing to PyPI
------------------

To publish a new version of the package to PyPI, increment the version in [imgix/__init__.py](https://github.com/imgix/imgix-python/blob/master/imgix/__init__.py) run the following:

```bash
pip install wheel
pip install twine
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```
