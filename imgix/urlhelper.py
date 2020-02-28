# -*- coding: utf-8 -*-
from base64 import urlsafe_b64encode
from future.moves.urllib.parse import quote, urlunparse
from future.utils import iteritems
import hashlib

from .compat import b
from ._version import __version__


class UrlHelper(object):
    """
    Helper class to create single domain imgix URLs. Example:

      >>> str(UrlHelper('demos.imgix.net', '/bridge.png', params={'w': 100}))
      https://demos.imgix.net/bridge.png?w=100

    Parameters
    ----------
    domain : str
    path : str
    scheme : { 'https', 'http' }
    sign_key : str or None
        When provided, this key will be used to sign the generated image URLs.
        You can read more about URL signing on our docs:
        https://docs.imgix.com/setup/securing-images
    include_library_param : bool
        If `True`, each created URL is suffixed with 'ixlib' parameter
        indicating the library used for generating the URLs. (default `True`)
    params : dict
        Dictionary specifying URL parameters. Non-imgix parameters are
        added to the URL unprocessed. For a complete list of imgix
        supported parameters, visit https://docs.imgix.com/apis/url .
        (default {})

    Methods
    -------
    set_parameter(key, value)
    delete_parameter(key)
    """
    def __init__(
            self,
            domain,
            path,
            scheme="https",
            sign_key=None,
            include_library_param=True,
            params={}):

        self._scheme = scheme
        self._host = domain
        self._path = path
        self._sign_key = sign_key
        self._include_library_param = include_library_param
        self._parameters = {}

        for key, value in iteritems(params):
            self.set_parameter(key, value)

    @classmethod
    def from_url(cls, url):
        pass

    def set_parameter(self, key, value):
        """
        Set a url parameter.

        Parameters
        ----------
        key : str
            If key ends with '64', the value provided will be automatically
            base64 encoded.
        """
        if value is None or isinstance(value, (int, float, bool)):
            value = str(value)

        if key.endswith('64'):
            value = urlsafe_b64encode(value.encode('utf-8'))
            value = value.replace(b('='), b(''))

        self._parameters[key] = value

    def delete_parameter(self, key):
        """
        Deletes the value associated with `key` from recorded parameters.

        Parameters
        ----------
        key : str

        Raises
        ------
        KeyError
            If key doesn't exist in recorded parameters.
        """
        if key in self._parameters:
            del self._parameters[key]

    def _str_is_ascii(self, s):
        try:
            b(s).decode('ascii')
            return True
        except Exception:
            return False

    def __str__(self):
        """
        Generate URL from the recorded parameters.

        Returns
        -------
        str
        """
        query = {}

        for key in self._parameters:
            query[key] = self._parameters[key]

        path = self._path

        if self._include_library_param:
            query["ixlib"] = "python-" + __version__

        if path.startswith("http"):
            try:
                path = quote(path, safe="~()*!.'")
            except KeyError:
                path = quote(path.encode('utf-8'), safe="~()*!.'")

        if not path.startswith("/"):
            path = "/" + path  # Fix web proxy style URLs

        if not path.startswith("/http") and not self._str_is_ascii(path):
            try:
                path = quote(path)
            except KeyError:
                path = quote(path.encode('utf-8'))

        query = "&".join(
            (quote(key, "") + "=" + quote(query[key], ""))
            for key in sorted(query))

        if self._sign_key:
            delim = "" if query == "" else "?"
            signing_value = self._sign_key + path + delim + query
            signature = hashlib.md5(signing_value.encode('utf-8')).hexdigest()
            if query:
                query += "&s=" + signature
            else:
                query = "s=" + signature

        return urlunparse([
            self._scheme,
            self._host,
            path,
            "",
            query,
            "", ])
