# -*- coding: utf-8 -*-
"""
imgix
~~~~~

A Python client library for generating URLs with imgix. Basic usage:

    >>> import imgix
    >>> builder = imgix.UrlBuilder("demos.imgix.net")
    >>> builder.create_url("/bridge.png", {'w': 100, 'h': 100})
    https://demos.imgix.net/bridge.png?h=100&w=100

... or generating signed URLs:

    >>> builder = imgix.UrlBuilder("demos.imgix.net", sign_key="test1234")
    >>> builder.create_url("/bridge.png", {'w': 100, 'h': 100})
    http://demos.imgix.net/bridge.png?h=100&w=100&s=7370d6e36bb2262e73b19578739af1af

Refer to `imgix.UrlBuilder` class documentation for all the supported options.
"""

from ._version import __version__

from .urlbuilder import UrlBuilder

from .constants import SHARD_STRATEGY_CYCLE
from .constants import SHARD_STRATEGY_CRC


__all__ = [
    'UrlBuilder', 'SHARD_STRATEGY_CRC', 'SHARD_STRATEGY_CYCLE',
    'SIGNATURE_MODE_QUERY', 'SIGNATURE_MODE_PATH', '__version__', ]
