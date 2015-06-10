try:
    # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
    from urllib.parse import quote
except ImportError:
    # Python 2.7
    import urlparse
    from urllib import urlencode
    from urllib import quote


__all__ = ['urlparse', 'urlencode', 'quote', ]
