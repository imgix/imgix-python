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

First, it's recommended you create a virtual environment:
```
python -m venv env/imgix
source env/imgix/bin/activate
```

Then install the dev dependencies:
```
pip install .[dev]
```

To run the tests:
```
tox
```
This will run all tests and check PEP8 compliance. Our test suite runs
continuously on [Travis CI](https://travis-ci.org/imgix/imgix-python) with
every pull request.

To run tests in a specific environment:
```
tox -e p27  # Python 2.7
tox -e core  # Your local Python version
tox -e flake8  # To run the linter
tox -e p27-compat  # Python 2.7 with future compatibility aliases
```

Publishing to PyPI
------------------

To publish a new version of the package to PyPI, increment the version in [imgix/__init__.py](https://github.com/imgix/imgix-python/blob/main/imgix/__init__.py) run the following:

```bash
pip install wheel
pip install twine
python setup.py sdist
python setup.py bdist_wheel --universal
twine upload dist/*
```
