try:
    # Python 3
    import urllib.parse as urlparse
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import unquote

    def iteritems(a_dict):
        return a_dict.items()

    def b(s):
        return s.encode("latin-1")

except ImportError:
    # Python 2.7
    import urlparse
    from urllib import urlencode
    from urllib import quote
    from urllib import unquote

    def iteritems(a_dict):
        return a_dict.iteritems()

    def b(s):
        return s

__all__ = ['iteritems', 'quote', 'unquote', 'urlparse', 'urlencode']
