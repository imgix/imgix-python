# -*- coding: utf-8 -*-

import imgix
import hashlib
import re


def _default_srcset(params={}):
    ub = imgix.UrlBuilder('testing.imgix.net',
                          sign_key='MYT0KEN',
                          include_library_param=False)
    return ub.create_srcset('image.jpg', params)


def _parse_width(width):
    return int(width[0:-1])


def test_no_parameters_generates_srcset_pairs():
    srcset = _default_srcset()
    expected_number_of_pairs = 31
    assert(expected_number_of_pairs == len(srcset.split(',')))


def test_srcset_pair_values():
    # array of expected resolutions to be generated
    resolutions = [100, 116, 134, 156, 182, 210, 244, 282,
                   328, 380, 442, 512, 594, 688, 798, 926,
                   1074, 1246, 1446, 1678, 1946, 2258, 2618,
                   3038, 3524, 4088, 4742, 5500, 6380, 7400, 8192]
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


def test_given_width_signs_urls():
    srcset = _default_srcset({'w': 100})
    srclist = srcset.split(',')

    for src in srclist:
        url = src.split(' ')[0]
        assert('s=' in url)

        # extract the sign parameter
        generated_signature = url[url.index('s=')+2:len(url)]

        params = url[url.index('?'):url.index('s=')-1]
        signature_base = 'MYT0KEN' + '/image.jpg' + params
        expected_signature = hashlib.md5(signature_base
                                         .encode('utf-8')).hexdigest()

        assert(expected_signature == generated_signature)


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
    min = _parse_width(min_parsed)
    max = _parse_width(max_parsed)

    assert(min >= 100)
    assert(max <= 8192)


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
        params = src[src.index('?'):len(src)]
        params = params[0:params.index('s=')-1]
        # extract the sign parameter
        generated_signature = src[src.index('s=')+2:len(src)]

        signature_base = 'MYT0KEN' + '/image.jpg' + params
        expected_signature = hashlib.md5(signature_base
                                         .encode('utf-8')).hexdigest()

        assert(expected_signature == generated_signature)


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

        # extract the sign parameter
        generated_signature = url[url.index('s=')+2:len(url)]

        params = url[url.index('?'):url.index('s=')-1]
        signature_base = 'MYT0KEN' + '/image.jpg' + params
        expected_signature = hashlib.md5(signature_base
                                         .encode('utf-8')).hexdigest()

        assert(expected_signature == generated_signature)


def test_given_aspect_ratio_srcset_generates_pairs():
    srcset = _default_srcset({'ar': '3:2'})
    expected_number_of_pairs = 31
    assert(expected_number_of_pairs == len(srcset.split(',')))


def test_given_aspect_ratio_srcset_pairs_within_bounds():
    srcset = _default_srcset({'ar': '3:2'})
    srclist = srcset.split(',')

    min_parsed = srclist[0].split(' ')[1]
    max_parsed = srclist[-1].split(' ')[1]
    min = _parse_width(min_parsed)
    max = _parse_width(max_parsed)

    assert(min >= 100)
    assert(max <= 8192)


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
        params = src[src.index('?'):len(src)]
        params = params[0:params.index('s=')-1]
        # extract the sign parameter
        generated_signature = src[src.index('s=')+2:len(src)]

        signature_base = 'MYT0KEN' + '/image.jpg' + params
        expected_signature = hashlib.md5(signature_base
                                         .encode('utf-8')).hexdigest()

        assert(expected_signature == generated_signature)


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

        # extract the sign parameter
        generated_signature = url[url.index('s=')+2:len(url)]

        params = url[url.index('?'):url.index('s=')-1]
        signature_base = 'MYT0KEN' + '/image.jpg' + params
        expected_signature = hashlib.md5(signature_base
                                         .encode('utf-8')).hexdigest()

        assert(expected_signature == generated_signature)
