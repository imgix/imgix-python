# -*- coding: utf-8 -*-

import hashlib
import urllib

try: # Python 3
    from urllib.parse import urlencode
    from urllib.parse import quote
    import urllib.parse as urlparse
except ImportError: # Python 2.7
    import urlparse
    from urllib import urlencode
    from urllib import quote

from .constants import *

class UrlHelper(object):

    @classmethod
    def from_url(cls, url):
        pass

    def __init__(self, domain, path, scheme="http",
                 sign_key=None, sign_mode=SIGNATURE_MODE_QUERY, **parameters):
        self._scheme = scheme
        self._host = domain
        self._path = path
        self._sign_key = sign_key
        if sign_mode != SIGNATURE_MODE_QUERY:
            raise Exception("Path signatures are not supported yet.")
        self._sign_mode = sign_mode
        self._parameters = {}
        for key, value in parameters.items():
            self.set_parameter(key, value)

    def set_parameter(self, key, value):
        if not value:
            self.delete_parameter(key)
            return

        self._parameters[key] = value

    def delete_parameter(self, key):
        if key in self._parameters:
            del self._parameters[key]

    def _str_is_ascii(self, s):
        try:
            s.decode('ascii')
            return True
        except:
            return False

    def __str__(self):
        query_pairs = []

        for key in sorted(self._parameters.keys()):
            query_pairs.append((str(key), str(self._parameters[key])))

        path = self._path

        if path.startswith("http"):
            try:
                path = quote(path, safe="")
            except KeyError:
                path = quote(path.encode('utf-8'), safe="")

        if not path.startswith("/"):
            path = "/" + path  # Fix web proxy style URLs

        if not path.startswith("/http") and not self._str_is_ascii(path):
            try:
                path = quote(path)
            except KeyError:
                path = quote(path.encode('utf-8'))

        query = urlencode(query_pairs)
        if self._sign_key:
            delim = "" if query == "" else "?"
            signing_value = self._sign_key + path + delim + query
            signature = hashlib.md5(signing_value.encode('utf-8')).hexdigest()

            if query:
                query += "&s=" + signature
            else:
                query = "s=" + signature

        return urlparse.urlunparse([
            self._scheme,
            self._host,
            path,
            "",
            query,
            "",
        ])
