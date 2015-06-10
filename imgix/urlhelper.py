# -*- coding: utf-8 -*-

import hashlib
import urllib
import urlparse

from constants import *

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
        for key, value in parameters.iteritems():
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
            path = urllib.quote(self._path, safe="")

        if not path.startswith("/"):
            path = "/" + path  # Fix web proxy style URLs

        if not self._str_is_ascii(path):
            path = urllib.quote(self._path)

        query = urllib.urlencode(query_pairs)
        if self._sign_key:
            delim = "" if query == "" else "?"
            signing_value = self._sign_key + path + delim + query
            signature = hashlib.md5(signing_value).hexdigest()

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
