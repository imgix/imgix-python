try:
    # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
    from urllib.parse import quote

    def iteritems(a_dict):
        return a_dict.items()

    def string_to_bytes(a_string):
        return bytes(a_string, 'utf-8')
except ImportError:
    # Python 2.7
    import urlparse
    from urllib import urlencode
    from urllib import quote

    def iteritems(a_dict):
        return a_dict.iteritems()

    def string_to_bytes(a_string):
        return bytes(a_string)


__all__ = ['string_to_bytes', 'iteritems', 'quote', 'urlparse', 'urlencode']
