# -*- coding: utf-8 -*-

from imgix import UrlBuilder

DOMAIN = 'testing.imgix.net'
TOKEN = 'MYT0KEN'
JPG_PATH = 'image.jpg'


def test_readme_500_to_2000():
    ub = UrlBuilder(DOMAIN, include_library_param=False)
    actual = ub.create_srcset(JPG_PATH, start=500, stop=2000)
    expected = "https://testing.imgix.net/image.jpg?w=500 500w,\n" + \
        "https://testing.imgix.net/image.jpg?w=580 580w,\n" + \
        "https://testing.imgix.net/image.jpg?w=673 673w,\n" + \
        "https://testing.imgix.net/image.jpg?w=780 780w,\n" + \
        "https://testing.imgix.net/image.jpg?w=905 905w,\n" + \
        "https://testing.imgix.net/image.jpg?w=1050 1050w,\n" + \
        "https://testing.imgix.net/image.jpg?w=1218 1218w,\n" + \
        "https://testing.imgix.net/image.jpg?w=1413 1413w,\n" + \
        "https://testing.imgix.net/image.jpg?w=1639 1639w,\n" + \
        "https://testing.imgix.net/image.jpg?w=1901 1901w,\n" + \
        "https://testing.imgix.net/image.jpg?w=2000 2000w"
    assert (expected == actual)


def test_readme_100_to_384_at_20():
    ub = UrlBuilder(DOMAIN, include_library_param=False)
    actual = ub.create_srcset(JPG_PATH, start=100, stop=384, tol=0.20)
    expected = "https://testing.imgix.net/image.jpg?w=100 100w,\n" + \
        "https://testing.imgix.net/image.jpg?w=140 140w,\n" + \
        "https://testing.imgix.net/image.jpg?w=196 196w,\n" + \
        "https://testing.imgix.net/image.jpg?w=274 274w,\n" + \
        "https://testing.imgix.net/image.jpg?w=384 384w"
    assert (expected == actual)


def test_readme_custom_widths():
    builder = UrlBuilder(DOMAIN, include_library_param=False)
    actual = builder.create_srcset(JPG_PATH, widths=[144, 240, 320, 446, 640])
    expected = "https://testing.imgix.net/image.jpg?w=144 144w,\n" + \
        "https://testing.imgix.net/image.jpg?w=240 240w,\n" + \
        "https://testing.imgix.net/image.jpg?w=320 320w,\n" + \
        "https://testing.imgix.net/image.jpg?w=446 446w,\n" + \
        "https://testing.imgix.net/image.jpg?w=640 640w"
    assert (expected == actual)


def test_readme_variable_quality():
    builder = UrlBuilder(DOMAIN, include_library_param=False)

    actual = builder.create_srcset(
        JPG_PATH, params={"w": 100}, disable_variable_quality=False)

    expected = "https://testing.imgix.net/image.jpg?dpr=1&q=75&w=100 1x,\n" + \
        "https://testing.imgix.net/image.jpg?dpr=2&q=50&w=100 2x,\n" + \
        "https://testing.imgix.net/image.jpg?dpr=3&q=35&w=100 3x,\n" + \
        "https://testing.imgix.net/image.jpg?dpr=4&q=23&w=100 4x,\n" + \
        "https://testing.imgix.net/image.jpg?dpr=5&q=20&w=100 5x"
    assert (expected == actual)
