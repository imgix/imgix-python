# -*- coding: utf-8 -*-
import re

from .constants import DOMAIN_PATTERN, SRCSET_TARGET_WIDTHS as TARGET_WIDTHS
from .constants import SRCSET_DPR_TARGET_RATIOS as TARGET_RATIOS
from .constants import IMAGE_MAX_WIDTH as MAX_WIDTH
from .constants import IMAGE_MIN_WIDTH as MIN_WIDTH
from .constants import SRCSET_WIDTH_TOLERANCE as TOLERANCE
from .constants import DPR_QUALITIES
from .validators import validate_min_max_tol, validate_widths
from .urlhelper import UrlHelper


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

    def create_srcset(self, path, params={}, **kwargs):
        """
        Create a srcset attribute.

        A srcset attribute consists of one or more non-empty URL. Each URL
        represents an image candidate string and each candidate string is
        separated by a comma (U+002C) character (,). Read more about the
        srcset attribute here:

        https://html.spec.whatwg.org/multipage/images.html#srcset-attributes

        This function produces two types of image candidate strings,

        * pixel density descriptors (x) and
        * width descriptors (w)

        Pixel density-described strings are produced when

        * a height (h) and an aspect (ar) ratio are present in `params`, or
        * only a width (w) is present in the `params`

        Example, a width (or a height _and_ aspect ratio):
        'https://example.test.com/image/path.png?dpr=1&w=320 1x'

        Width-described strings are produced if neither a width nor a
        height-aspect-ratio pair are present in `params`.

        Example, no width, no height, no aspect ratio:
        'https://example.test.com/image/path.png?w=100 100w'

        Parameters
        ----------
        path : str
            Path to the image file, e.g. 'image/path.png'.
        params : dict, optional
            Parameters that will be transformed into query parameters,
            including 'w' or 'ar' and 'h' if generating a pixel density
            described srcset, {} by default.
        start : int, optional
            Starting minimum width value, MIN_WIDTH by default.
        stop : int, optional
            Stopping maximum width value, MAX_WIDTH by default.
        tol : float, optional
            Tolerable amount of width value variation, TOLERANCE by default.
        widths: list, optional
            List of target widths, `TARGET_WIDTHS` by default.
        Returns
        -------
        str
            Srcset attribute string.
        """
        widths_list = kwargs.get('widths', None)
        if widths_list:
            validate_widths(widths_list)
            return self._build_srcset_pairs(path, params, targets=widths_list)

        # Attempt to assign `start`, `stop`, and `tol` from `kwargs`.
        # If the key does not exist, assign `None`.
        start = kwargs.get('start', None)
        stop = kwargs.get('stop', None)
        tol = kwargs.get('tol', None)

        # Attempt to generate the specified target widths.
        # Assign defaults where appropriate, then validate
        # this group. If validation succeeds, generate the
        # target widths.
        if start is None:
            start = MIN_WIDTH
        if stop is None:
            stop = MAX_WIDTH
        if tol is None:
            tol = TOLERANCE

        validate_min_max_tol(start, stop, tol)

        targets = \
            target_widths(start=start, stop=stop, tol=tol)

        if (self._is_dpr(params)):
            disable_variable_quality = \
                kwargs.get('disable_variable_quality', False)
            return self._build_srcset_DPR(
                path,
                params,
                disable_variable_quality=disable_variable_quality)
        else:
            return self._build_srcset_pairs(path, params, targets)

    def _build_srcset_pairs(
            self, path, params, targets=TARGET_WIDTHS):
        # prevents mutating the params dict
        srcset_params = dict(params)
        srcset_entries = []

        for w in targets:
            srcset_params['w'] = w
            srcset_entries.append(self.create_url(path, srcset_params) +
                                  " " + str(w) + "w")

        return ",\n".join(srcset_entries)

    def _build_srcset_DPR(
            self, path, params, targets=TARGET_RATIOS,
            disable_variable_quality=False):
        # If variable quality output is _not disabled_, then output
        # quality values, 'q', will vary in accordance with the
        # default `DPR_QUALITIES` [1x => q=75, ... 5x => 20].
        #
        # If 'q' is explicitly passed, it takes precedence over
        # the default `DPR_QUALITIES`. Right now, this means that
        # if 'q' is passed, it's value will be used for the output
        # quality of each dpr image (i.e. for 1x through 5x).
        #
        # Note: if `q` is passed with `params`, then it will be
        # present in the URL's query params whether or not
        # `disabled_variable_quality` is `True` or `False`.

        # prevents mutating the params dict
        srcset_params = dict(params)
        srcset_entries = []

        for dpr in targets:
            srcset_params['dpr'] = dpr

            if not disable_variable_quality:
                quality = params.get('q', DPR_QUALITIES[dpr])
                srcset_params['q'] = quality

            srcset_entries.append(self.create_url(path, srcset_params) +
                                  " " + str(dpr) + "x")

        return ",\n".join(srcset_entries)

    def _is_dpr(self, params):
        has_width = 'w' in params
        has_height = 'h' in params
        has_aspect_ratio = 'ar' in params

        return has_width or (has_height and has_aspect_ratio)


def target_widths(start=MIN_WIDTH, stop=MAX_WIDTH, tol=TOLERANCE):
    """
    Generate a list of target widths.

    This function generates a list of target widths used to width-describe
    image candidate strings (URLs) within a srcset attribute.

    For example, if the target widths are [100, 200, 300], they would become:

    'https://example.test.com/image/path.png?w=100 100w
    https://example.test.com/image/path.png?w=200 200w
    https://example.test.com/image/path.png?w=300 300w'

    in the srcset attribute string. Read more about image candidate strings
    and width descriptors here:

    https://html.spec.whatwg.org/multipage/images.html#image-candidate-string

    Parameters
    ----------
    start : int, optional
        Starting minimum width value, MIN_WIDTH by default.
    stop : int, optional
        Stopping maximum width value, MAX_WIDTH by default.
    tol : float, optional
        Tolerable amount of image width-variation, TOLERANCE by default.

    Returns
    -------
    list
        A list of even integer values.
    """
    validate_min_max_tol(start, stop, tol)
    # If any value differs from the default, we're constructing a custom
    # target widths list.
    CUSTOM = any([tol != TOLERANCE, start != MIN_WIDTH, stop != MAX_WIDTH])

    if not CUSTOM:
        return TARGET_WIDTHS

    if start == stop:
        return [int(start)]

    resolutions = []

    while start < stop and start < MAX_WIDTH:
        resolutions.append(int(round(start)))
        start *= 1 + tol * 2

    # The most recently appended value may, or may not, be
    # the `stop` value. In order to be inclusive of the
    # stop value, check for this case and add it, if necessary.
    if resolutions[-1] < stop:
        resolutions.append(int(stop))

    return resolutions
