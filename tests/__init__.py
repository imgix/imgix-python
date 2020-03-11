import os

if os.environ.get('COMPAT_ENV'):
    # Due to how PyTest runs tests, it is not possible to
    # call `install_aliases` on a per-test basis.
    # To workaround this, we rely on Tox conditionally setting
    # this env variable to run all the tests with and without the
    # compatibility aliases.
    from future import standard_library
    standard_library.install_aliases()
