# -*- coding: utf-8 -*-

import zlib

from .urlhelper import UrlHelper

from .constants import SHARD_STRATEGY_CYCLE
from .constants import SHARD_STRATEGY_CRC
from .constants import SIGNATURE_MODE_QUERY


class UrlBuilder(object):
    def __init__(
            self,
            domains,
            use_https=True,
            sign_key=None,
            sign_mode=SIGNATURE_MODE_QUERY,
            shard_strategy=SHARD_STRATEGY_CRC,
            sign_with_library_version=True):

        if not isinstance(domains, list):
            domains = [domains]

        self._domains = domains
        self._sign_key = sign_key
        self._sign_mode = sign_mode
        self._use_https = use_https
        self._shard_strategy = shard_strategy
        self._shard_next_index = 0
        self._sign_with_library_version = sign_with_library_version

    def create_url(self, path, **kwargs):
        if self._shard_strategy == SHARD_STRATEGY_CRC:
            crc = zlib.crc32(path.encode('utf-8')) & 0xffffffff
            index = crc % len(self._domains)  # Deterministically choose domain
            domain = self._domains[index]

        elif self._shard_strategy == SHARD_STRATEGY_CYCLE:
            domain = self._domains[self._shard_next_index]
            self._shard_next_index = (
                self._shard_next_index + 1) % len(self._domains)

        else:
            domain = self._domains[0]

        scheme = "https" if self._use_https else "http"

        url_obj = UrlHelper(
            domain,
            path,
            scheme,
            sign_key=self._sign_key,
            sign_mode=self._sign_mode,
            sign_with_library_version=self._sign_with_library_version,
            **kwargs)

        return str(url_obj)
