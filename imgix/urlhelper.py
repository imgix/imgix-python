# -*- coding: utf-8 -*-

import hashlib

from .constants import SIGNATURE_MODE_QUERY

from .compat import urlencode
from .compat import urlparse
from .compat import quote
from . import __version__


class UrlHelper(object):
    def __init__(
            self,
            domain,
            path,
            scheme="http",
            sign_key=None,
            sign_mode=SIGNATURE_MODE_QUERY,
            sign_with_library_version=True,
            **kwargs):

        self._scheme = scheme
        self._host = domain
        self._path = path
        self._sign_key = sign_key
        self._sign_with_library_version = sign_with_library_version

        if sign_mode != SIGNATURE_MODE_QUERY:
            raise Exception("Path signatures are not supported yet.")

        self._sign_mode = sign_mode
        self._parameters = {}
        for key, value in kwargs.items():
            self.set_parameter(key, value)

    @classmethod
    def from_url(cls, url):
        pass

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

        if self._sign_with_library_version:
            query_pairs.append(("ixlib", "python-" + __version__))

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
            "", ])
