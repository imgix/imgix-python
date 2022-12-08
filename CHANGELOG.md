# Changelog

## [4.0.0](https://github.com/imgix/imgix-python/compare/3.2.1...4.0.0) (2022-12-08)

### Breaking Changes

- feat: drop python 2 support ([#88](https://github.com/imgix/imgix-python/pull/88))
- fix: fixed-height produces dpr-based srcset ([#88](https://github.com/imgix/imgix-python/pull/88))
- feat: encode file path components ([#88](https://github.com/imgix/imgix-python/pull/88))

### Features

- feat: add path encoding to be disabled optionally ([#98](https://github.com/imgix/imgix-python/pull/98))
- feat: customize variable qualities in options ([#102](https://github.com/imgix/imgix-python/pull/102))
- feat: customize target device pixel ratios ([#103](https://github.com/imgix/imgix-python/pull/103))

## [3.2.1](https://github.com/imgix/imgix-python/compare/3.2.0...3.2.1) (2020-06-10)

- refactor: relax validation for min/max width values ([#80](https://github.com/imgix/imgix-python/pull/80))

## [3.2.0](https://github.com/imgix/imgix-python/compare/3.1.2...3.2.0) (2020-06-05)

- feat: create custom srcset ([#63](https://github.com/imgix/imgix-python/pull/63))
- feat: introduce variable image output quality ([#65](https://github.com/imgix/imgix-python/pull/65))
- fix: remove ensure even ([#72](https://github.com/imgix/imgix-python/pull/72))
- feat: throw exceptions from validators ([#77](https://github.com/imgix/imgix-python/pull/77))
- fix: convert tol to float ([#75](https://github.com/imgix/imgix-python/pull/75))

## [3.1.2](https://github.com/imgix/imgix-python/compare/3.1.1...3.1.2) (2020-03-11)

- Fix Python 2/3 compatibility issues
  ([\#57](https://github.com/imgix/imgix-python/pull/57))

## [3.1.1](https://github.com/imgix/imgix-python/compare/3.1.0...3.1.1) (2019-08-22)

- fix: include dpr parameter when generating fixed-width srcset
  ([\#50](https://github.com/imgix/imgix-python/pull/50))

## [3.1.0](https://github.com/imgix/imgix-python/compare/3.0.0...3.1.0) (2019-08-22)

- feat: add srcset generation
  ([\#48](https://github.com/imgix/imgix-python/pull/48))
- build(tox): improve code coverage reporting; parallelize testing
  ([\#49](https://github.com/imgix/imgix-python/pull/49))

## [3.0.0](https://github.com/imgix/imgix-python/compare/2.3.0...3.0.0) (2019-06-07)

- fix: remove deprecated domain sharding functionality
  ([\#44](https://github.com/imgix/imgix-python/pull/44))
- fix: remove deprecated [opts]{.title-ref} parameter
  ([\#46](https://github.com/imgix/imgix-python/pull/46))
- fix: remove deprecated [sign\_with\_library\_version]{.title-ref}
  parameter ([\#47](https://github.com/imgix/imgix-python/pull/47))

## [2.3.0](https://github.com/imgix/imgix-python/compare/2.2.0...2.3.0) (2019-06-06)

- feat: deprecate [domains]{.title-ref} in favor of
  [domain]{.title-ref}
  ([\#45](https://github.com/imgix/imgix-python/pull/45))

## [2.2.0](https://github.com/imgix/imgix-python/compare/2.1.0...2.2.0) (2019-05-07)

- deprecate domain sharding
  ([\#41](https://github.com/imgix/imgix-python/pull/41))([\#42](https://github.com/imgix/imgix-python/pull/42))

## 2.1.0 (2019-02-13)

- Domain validation added during [UrlBuilder]{.title-ref}
  initialization
- [sign\_with\_library\_version]{.title-ref} parameter from
  [UrlBuilder]{.title-ref} deprecated in favor of
  [include\_library\_param]{.title-ref}.

## 2.0.0 (2018-08-08)

- [UrlBuilder]{.title-ref}\'s [sign\_mode]{.title-ref} argument
  removed
- [opts]{.title-ref} parameter from
  [UrlBuilder.create\_url]{.title-ref} deprecated in favor of
  [params]{.title-ref}.

## 1.2.0 (2018-06-20)

- [sign\_mode]{.title-ref} argument deprecated
- License corrected to BSD-2-Clause.
- Docstrings added to classes and methods.

## 1.1.2 (2016-06-30)

- Proper encodeURIComponent-style URL encoding for web proxy sources.
  See \#21 for more information.

## 1.1.0 (2016-02-26)

- Added automatic Base64 encoding for all Base64 variant parameters.
- Properly encoding all query keys and values.

## 1.0.0 (2016-01-15)

- Change UrlBuilder\#create_url to accept dict instead of kwargs.
  This fixes an issue with reserved words that are also imgix params
  potentially causing errors.

## 0.2.1 (2016-01-15)

- Fixed a bug where any passed params that were falsy would not be
  passed through to imgix.

## 0.2.0 (2015-06-15)

- Introduces defaulting to HTTPS on all requests, per the
  imgix-blueprint.

## 0.1.0 (2015-06-11)

- Includes new functionality to sign every URL with an ixlib parameter
  for diagnostic purposes.

## 0.0.4 (2015-06-10)

- New README note about publishing packages
