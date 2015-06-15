# -*- coding: utf-8 -*-

__version__ = '0.1.0'

from .urlbuilder import UrlBuilder

from .constants import SHARD_STRATEGY_CYCLE
from .constants import SHARD_STRATEGY_CRC
from .constants import SIGNATURE_MODE_QUERY
from .constants import SIGNATURE_MODE_PATH


__all__ = [
    'UrlBuilder', 'SHARD_STRATEGY_CRC', 'SHARD_STRATEGY_CYCLE',
    'SIGNATURE_MODE_QUERY', 'SIGNATURE_MODE_PATH', '__version__', ]
