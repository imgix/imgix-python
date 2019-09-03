# -*- coding: utf-8 -*-

import re

from .urlhelper import UrlHelper

from .constants import DOMAIN_PATTERN, SRCSET_TARGET_WIDTHS


SRCSET_DPR_TARGET_RATIOS = range(1, 6)


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
    validate_domain(domain)
        Returns true if the supplied string parameter pattern matches a valid
        domain name accepted by imgix
    create_url(path, params=None)
        Create URL with the supplied path and `params` parameters dict.
    create_srcset(path, params=None)
        Create srcset attribute value with the supplied path and
        `params` parameters dict.
        Will generate a fixed-width DPR srcset if a width OR height and aspect
        ratio are passed in as parameters. Otherwise will generate a srcset
        with width-descriptor pairs.
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
        """
        Returns true if the supplied string parameter pattern matches a valid
        domain name accepted by imgix

        Parameters
        ----------
        domain : str

        Returns
        -------
        bool
        """

        err_str = str(
            'Domain must be passed in as fully-qualified domain names and ' +
            'should not include a protocol or any path element, i.e. ' +
            '"example.imgix.net".')

        if re.match(DOMAIN_PATTERN, domain) is None:
            raise ValueError(err_str)

    def create_url(self, path, params=None):
        """
        Create URL with supplied path and `params` parameters dict.

        Parameters
        ----------
        path : str
        params : dict
            Dictionary specifying URL parameters. Non-imgix parameters are
            added to the URL unprocessed. For a complete list of imgix
            supported parameters, visit https://docs.imgix.com/apis/url .
            (default None)

        Returns
        -------
        str
            imgix URL
        """
        if not params:
            params = {}

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

    def create_srcset(self, path, params=None):
        """
        Create srcset attribute value with the supplied path and
        `params` parameters dict.
        Will generate a fixed-width DPR srcset if a width OR height and aspect
        ratio are passed in as parameters. Otherwise will generate a srcset
        with width-descriptor pairs.

        Parameters
        ----------
        path : str
        params : dict
            Dictionary specifying URL parameters. Non-imgix parameters are
            added to the URL unprocessed. For a complete list of imgix
            supported parameters, visit https://docs.imgix.com/apis/url .
            (default None)

        Returns
        -------
        str
            srcset attribute value
        """
        if not params:
            params = {}

        width = params['w'] if 'w' in params else None
        height = params['h'] if 'h' in params else None
        aspect_ratio = params['ar'] if 'ar' in params else None

        if (width or (height and aspect_ratio)):
            return self._build_srcset_DPR(path, params)
        else:
            return self._build_srcset_pairs(path, params)

    def _build_srcset_pairs(self, path, params):
        srcset = ''

        for i in range(len(SRCSET_TARGET_WIDTHS)):
            current_width = SRCSET_TARGET_WIDTHS[i]
            current_params = params
            current_params['w'] = current_width
            srcset += self.create_url(path, current_params) \
                + ' ' + str(current_width) + 'w,\n'

        return srcset[0:-2]

    def _build_srcset_DPR(self, path, params):
        srcset = ''

        for i in range(len(SRCSET_DPR_TARGET_RATIOS)):
            current_ratio = SRCSET_DPR_TARGET_RATIOS[i]
            current_params = params
            current_params['dpr'] = i+1
            srcset += self.create_url(path, current_params) \
                + ' ' + str(current_ratio) + 'x,\n'

        return srcset[0:-2]
