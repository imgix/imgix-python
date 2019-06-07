Changelog
=========

`2.3.0`_ (2019-06-06)
---------------------
.. _2.3.0: https://github.com/imgix/imgix-python/compare/2.2.0...2.3.0

*    feat: deprecate `domains` in favor of `domain` (`#45`_)

.. _#45: https://github.com/imgix/imgix-python/pull/45


`2.2.0`_ (2019-05-07)
---------------------
.. _2.2.0: https://github.com/imgix/imgix-python/compare/2.1.0...2.2.0

*   deprecate domain sharding (`#41`_)(`#42`_)

.. _#41: https://github.com/imgix/imgix-python/pull/41
.. _#42: https://github.com/imgix/imgix-python/pull/42


2.1.0 (2019-02-13)
------------------

* Domain validation added during `UrlBuilder` initialization
* `sign_with_library_version` parameter from `UrlBuilder` deprecated in favor of `include_library_param`.


2.0.0 (2018-08-08)
------------------

* `UrlBuilder`'s `sign_mode` argument removed
* `opts` parameter from `UrlBuilder.create_url` deprecated in favor of `params`.


1.2.0 (2018-06-20)
------------------

* `sign_mode` argument deprecated
* License corrected to BSD-2-Clause.
* Docstrings added to classes and methods.


1.1.2 (2016-06-30)
------------------

* Proper encodeURIComponent-style URL encoding for web proxy sources. See #21
  for more information.


1.1.0 (2016-02-26)
------------------

* Added automatic Base64 encoding for all Base64 variant parameters.

* Properly encoding all query keys and values.


1.0.0 (2016-01-15)
------------------

* Change UrlBuilder#create_url to accept dict instead of kwargs. This fixes an
  issue with reserved words that are also imgix params potentially causing
  errors.


0.2.1 (2016-01-15)
------------------

* Fixed a bug where any passed params that were falsy would not be passed
  through to imgix.


0.2.0 (2015-06-15)
------------------

* Introduces defaulting to HTTPS on all requests, per the imgix-blueprint.


0.1.0 (2015-06-11)
------------------

* Includes new functionality to sign every URL with an ixlib parameter for
  diagnostic purposes.


0.0.4 (2015-06-10)
------------------

* New README note about publishing packages
