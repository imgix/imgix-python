# -*- coding: utf-8 -*-

import re

from .urlhelper import UrlHelper

from .constants import DOMAIN_PATTERN, target_widths


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
    include_library_param : bool
        If `True`, each created URL is suffixed with 'ixlib' parameter
        indicating the library used for generating the URLs. (default `True`)

    Methods
    -------
    create_url(path, params={})
        Create URL with the supplied path and `params` parameters dict.
    """
    def __init__(
            self,
            domain,
            use_https=True,
            sign_key=None,
            include_library_param=True):

        self.validate_domain(domain)

        self._domain = domain
        self._sign_key = sign_key
        self._use_https = use_https
        self._include_library_param = include_library_param

    def validate_domain(self, domain):
        err_str = str(
            'Domain must be passed in as fully-qualified domain names and ' +
            'should not include a protocol or any path element, i.e. ' +
            '"example.imgix.net".')

        if re.match(DOMAIN_PATTERN, domain) is None:
            raise ValueError(err_str)

    def create_url(self, path, params={}):
        """
        Create URL with supplied path and `params` parameters dict.

        Parameters
        ----------
        path : str
        params : dict
            Dictionary specifying URL parameters. Non-imgix parameters are
            added to the URL unprocessed. For a complete list of imgix
            supported parameters, visit https://docs.imgix.com/apis/url .
            (default {})

        Returns
        -------
        str
            imgix URL
        """

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

    def create_srcset(self, path, params={}):
        width = params['w'] if 'w' in params else None
        height = params['h'] if 'h' in params else None
        aspect_ratio = params['ar'] if 'ar' in params else None

        if (width or (height and aspect_ratio)):
            return self.__build_srcset_DPR(path, params)
        else:
            return self.__build_srcset_pairs(path, params)

    def __build_srcset_pairs(self, path, params={}):
        srcset = ''
        widths = target_widths()

        for i in range(len(widths)):
            current_width = widths[i]
            current_params = params.copy()
            current_params['w'] = current_width
            srcset += self.create_url(path, current_params) \
                + ' ' + str(current_width) + 'w,\n'

        return srcset[0:-2]

    def __build_srcset_DPR(self, path, params={}):
        srcset = ''
        target_ratios = [1, 2, 3, 4, 5]
        url = self.create_url(path, params)

        for i in range(len(target_ratios)):
            current_ratio = target_ratios[i]
            srcset += url + ' ' + str(current_ratio) + 'x,\n'

        return srcset[0:-2]
