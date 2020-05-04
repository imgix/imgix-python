# -*- coding: utf-8 -*-

import imgix
import hashlib
import re

from imgix.constants import DPR_QUALITIES
from imgix.constants import SRCSET_TARGET_WIDTHS as TARGET_WIDTHS
from imgix.constants import IMAGE_MIN_WIDTH, IMAGE_MAX_WIDTH


DOMAIN = 'testing.imgix.net'
TOKEN = 'MYT0KEN'
JPG_PATH = 'image.jpg'


def _default_srcset(params={}):
    ub = imgix.UrlBuilder(domain=DOMAIN,
                          sign_key=TOKEN,
                          include_library_param=False)
    return ub.create_srcset(JPG_PATH, params)


def _parse_width(width):
    return int(width[0:-1])


def get_params(url):
    return url[url.index('?'): url.index('s=') - 1]


def make_signature_base(params):
    return TOKEN + '/' + JPG_PATH + params


def make_expected_signature(url):
    params = get_params(url)
    base = make_signature_base(params)
    return hashlib.md5(base.encode('utf-8')).hexdigest()


def get_actual_signature(url):
    return url[url.index('s=') + 2: len(url)]


def test_no_parameters_generates_srcset_pairs():
    srcset = _default_srcset()
    expected_number_of_pairs = 31
    assert(expected_number_of_pairs == len(srcset.split(',')))


def test_srcset_pair_values():
    # array of expected resolutions to be generated
    resolutions = TARGET_WIDTHS
    srcset = _default_srcset()
    srclist = srcset.split(',')
    index = 0

    for src in srclist:
        width = src.split(' ')[1]

        # extract width int values
        value = re.search(re.compile(r'\d+'), width)
        assert(int(value.group(0)) == resolutions[index])
        index += 1


def test_given_width_srcset_is_DPR():
    srcset = _default_srcset({'w': 100})
    device_pixel_ratio = 1
    srclist = srcset.split(',')

    for src in srclist:
        ratio = src.split(' ')[1]
        dpr_str = str(device_pixel_ratio) + 'x'
        assert(dpr_str == ratio)
        device_pixel_ratio += 1


def test_given_width_srcset_has_dpr_params():
    srcset = _default_srcset({'w': 100})
    srclist = srcset.split(',')

    for i in range(len(srclist)):
        src = srclist[i].split(' ')[0]
        assert(src.index("dpr=" + str(i+1)))


def test_variable_output_quality_default():
    srcset = _default_srcset({'w': 100})
    srclist = srcset.split(',')

    # Accumulate the values of the `DPR_QUALITIES` dictionary
    # as a `dpr_qualities` list.
    dpr_qualities = sorted([q for q in DPR_QUALITIES.values()], reverse=True)

    # Zip the `srclist` and `dpr_qualities` into the pairs
    # we expect them to occur in.
    for src, dpr_quality in zip(srclist, dpr_qualities):
        quality = "q=" + str(dpr_quality)
        assert(quality in src)


def test_disable_variable_output_quality():
    ub = imgix.UrlBuilder(DOMAIN, include_library_param=False)
    srcset = ub.create_srcset(JPG_PATH, disable_variable_quality=True)
    srclist = srcset.split(',')

    dpr_qualities = sorted([q for q in DPR_QUALITIES.values()], reverse=True)

    for src, dpr_quality in zip(srclist, dpr_qualities):
        quality = "q=" + str(dpr_quality)
        # Ensure we _do not_ find variable qualities in each src.
        assert(not (quality in src))


def test_given_width_signs_urls():
    srcset = _default_srcset({'w': 100})
    srclist = srcset.split(',')

    for src in srclist:
        url = src.split(' ')[0]
        assert('s=' in url)

        actual_signature = get_actual_signature(url)
        expected_signature = make_expected_signature(url)

        assert(expected_signature == actual_signature)


def test_given_height_srcset_generates_pairs():
    srcset = _default_srcset({'h': 100})
    expected_number_of_pairs = 31
    assert(expected_number_of_pairs == len(srcset.split(',')))


def test_given_height_respects_parameter():
    srcset = _default_srcset({'h': 100})
    srclist = srcset.split(',')

    for src in srclist:
        assert('h=100' in src)


def test_given_height_srcset_pairs_within_bounds():
    srcset = _default_srcset({'h': 100})
    srclist = srcset.split(',')

    min_parsed = srclist[0].split(' ')[1]
    max_parsed = srclist[-1].split(' ')[1]
    min_width = _parse_width(min_parsed)
    max_width = _parse_width(max_parsed)

    assert(min_width >= IMAGE_MIN_WIDTH)
    assert(max_width <= IMAGE_MAX_WIDTH)


# a 17% testing threshold is used to account for rounding
def test_given_height_srcset_iterates_17_percent():
    increment_allowed = 0.17
    srcset = _default_srcset({'h': 100})
    srcslist = srcset.split(',')
    widths_list = [src.split(' ')[1] for src in srcslist]
    # a list of all widths as integers
    widths = [_parse_width(width) for width in widths_list]

    prev = widths[0]
    for i in range(1, len(widths)):
        width = widths[i]
        assert((width / prev) < (1 + increment_allowed))
        prev = width


def test_given_height_srcset_signs_urls():
    srcset = _default_srcset({'h': 100})
    srclist = srcset.split(',')
    srcs = [src.split(' ')[0] for src in srclist]

    for src in srcs:
        assert(src.index('s='))

        actual_signature = get_actual_signature(src)
        expected_signature = make_expected_signature(src)

        assert(expected_signature == actual_signature)


def test_given_width_and_height_is_DPR():
    srcset = _default_srcset({'w': 100, 'h': 100})
    device_pixel_ratio = 1
    srclist = srcset.split(',')

    for src in srclist:
        ratio = src.split(' ')[1]
        dpr_str = str(device_pixel_ratio) + 'x'
        assert(dpr_str == ratio)
        device_pixel_ratio += 1


def test_given_width_and_height_srcset_has_dpr_params():
    srcset = _default_srcset({'w': 100, 'h': 100})
    srclist = srcset.split(',')

    for i in range(len(srclist)):
        src = srclist[i].split(' ')[0]
        assert(src.index("dpr=" + str(i+1)))


def test_given_width_and_height_signs_urls():
    srcset = _default_srcset({'w': 100, 'h': 100})
    srclist = srcset.split(',')

    for src in srclist:
        url = src.split(' ')[0]
        assert('s=' in url)

        actual_signature = get_actual_signature(url)
        expected_signature = make_expected_signature(url)

        assert(expected_signature == actual_signature)


def test_given_aspect_ratio_srcset_generates_pairs():
    srcset = _default_srcset({'ar': '3:2'})
    expected_number_of_pairs = 31
    assert(expected_number_of_pairs == len(srcset.split(',')))


def test_given_aspect_ratio_srcset_pairs_within_bounds():
    srcset = _default_srcset({'ar': '3:2'})
    srclist = srcset.split(',')

    min_parsed = srclist[0].split(' ')[1]
    max_parsed = srclist[-1].split(' ')[1]
    min_size = _parse_width(min_parsed)
    max_size = _parse_width(max_parsed)

    assert(min_size >= IMAGE_MIN_WIDTH)
    assert(max_size <= IMAGE_MAX_WIDTH)


# a 17% testing threshold is used to account for rounding
def test_given_aspect_ratio_srcset_iterates_17_percent():
    increment_allowed = 0.17
    srcset = _default_srcset({'ar': '3:2'})
    srcslist = srcset.split(',')
    widths_list = [src.split(' ')[1] for src in srcslist]
    # a list of all widths as int
    widths = [_parse_width(width) for width in widths_list]

    prev = widths[0]
    for i in range(1, len(widths)):
        width = widths[i]
        assert((width / prev) < (1 + increment_allowed))
        prev = width


def test_given_aspect_ratio_srcset_signs_urls():
    srcset = _default_srcset({'ar': '3:2'})
    srclist = srcset.split(',')
    srcs = [src.split(' ')[0] for src in srclist]

    for src in srcs:
        assert(src.index('s='))

        actual_signature = get_actual_signature(src)
        expected_signature = make_expected_signature(src)

        assert(expected_signature == actual_signature)


def test_given_aspect_ratio_and_height_srcset_is_DPR():
    srcset = _default_srcset({'ar': '3:2', 'h': 500})
    device_pixel_ratio = 1
    srclist = srcset.split(',')

    for src in srclist:
        ratio = src.split(' ')[1]
        dpr_str = str(device_pixel_ratio) + 'x'
        assert(dpr_str == ratio)
        device_pixel_ratio += 1


def test_given_aspect_ratio_and_height_srcset_has_dpr_params():
    srcset = _default_srcset({'ar': '3:2', 'h': 500})
    srclist = srcset.split(',')

    for i in range(len(srclist)):
        src = srclist[i].split(' ')[0]
        assert(src.index("dpr=" + str(i+1)))


def test_given_aspect_ratio_and_height_srcset_signs_urls():
    srcset = _default_srcset({'ar': '3:2', 'h': 500})
    srclist = srcset.split(',')

    for src in srclist:
        url = src.split(' ')[0]
        assert('s=' in url)

        actual_signature = get_actual_signature(url)
        expected_signature = make_expected_signature(url)

        assert(expected_signature == actual_signature)


def test_given_fit_params_not_altered():
    params = {'fit': 'max'}
    _default_srcset(params)
    assert params == {'fit': 'max'}


def test_given_width_params_not_altered():
    params = {'w': 100}
    _default_srcset(params)

    assert params == {'w': 100}
