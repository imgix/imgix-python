# -*- coding: utf-8 -*-

import warnings
import re

from .urlhelper import UrlHelper

from .constants import DOMAIN_PATTERN


class UrlBuilder(object):
    """
    Create imgix URLs

    The URL builder can be reused to create URLs for any images on the
    provided domain.

    Parameters
    ----------
    domain : str
        Domain to use while creating imgix URLs.
    use_https : bool
        If `True`, create HTTPS imgix image URLs. (default `True`)
    sign_key : str or None
        When provided, this key will be used to sign the generated image URLs.
        You can read more about URL signing on our docs:
        https://docs.imgix.com/setup/securing-images
    sign_with_library_version : bool
        Deprecated and to be removed in next major version
    include_library_param : bool
        If `True`, each created URL is suffixed with 'ixlib' parameter
        indicating the library used for generating the URLs. (default `True`)

    Methods
    -------
    create_url(path, opts={})
        Create URL with the supplied path and `opts` parameters dict.
    """
    def __init__(
            self,
            domain,
            use_https=True,
            sign_key=None,
            sign_with_library_version=None,
            include_library_param=True):

        if sign_with_library_version is not None:
            warnings.warn('`sign_with_library_version` has been deprecated ' +
                          'and will be removed in the next major version. ' +
                          'Use `include_library_param` instead.',
                          DeprecationWarning, stacklevel=2)

        self.validate_domain(domain)
        include_library_param = (
                                    sign_with_library_version
                                    if sign_with_library_version
                                    is not None else include_library_param)
        self._domain = domain
        self._sign_key = sign_key
        self._use_https = use_https
        self._include_library_param = include_library_param

    def validate_domain(self, domain):
        err_str = str(
            'domain must be passed in as fully-qualified domain names and ' +
            'should not include a protocol or any path element, i.e. ' +
            '"example.imgix.net".')

        if re.match(DOMAIN_PATTERN, domain) is None:
            raise ValueError(err_str)

    def create_url(self, path, params={}, opts={}):
        """
        Create URL with supplied path and `opts` parameters dict.

        Parameters
        ----------
        path : str
        opts : dict
            Dictionary specifying URL parameters. Non-imgix parameters are
            added to the URL unprocessed. For a complete list of imgix
            supported parameters, visit https://docs.imgix.com/apis/url .
            (default {})

        Returns
        -------
        str
            imgix URL
        """

        if opts:
            warnings.warn('`opts` has been deprecated. Use `params` instead.',
                          DeprecationWarning, stacklevel=2)
        params = params or opts
        domain = self._domain
        scheme = "https" if self._use_https else "http"

        url_obj = UrlHelper(
            domain,
            path,
            scheme,
            sign_key=self._sign_key,
            include_library_param=self._include_library_param,
            params=params)

        return str(url_obj)
