# -*- coding: utf-8 -*-
import imgix

from future.moves.urllib.parse import urlparse
from imgix import constants
from imgix import urlbuilder
from imgix.constants import IMAGE_MAX_WIDTH, IMAGE_MIN_WIDTH


def _get_domain(url):
    return urlparse(url).hostname


def _default_builder():
    return imgix.UrlBuilder('my-social-network.imgix.net',
                            include_library_param=False)


def _default_builder_with_signature():
    return imgix.UrlBuilder('my-social-network.imgix.net', True, "FOO123bar",
                            include_library_param=False)


def test_create():
    builder = imgix.UrlBuilder('my-social-network.imgix.net')
    assert type(builder) is imgix.UrlBuilder


def test_create_accepts_domains_single_str():
    domain = 'my-social-network-1.imgix.net'
    builder = imgix.UrlBuilder(domain)
    assert domain == _get_domain(builder.create_url('/users/1.png'))


def test_create_url_with_path():
    builder = _default_builder()
    url = builder.create_url("/users/1.png")
    assert url == "https://my-social-network.imgix.net/users/1.png"


def test_create_url_with_path_and_parameters():
    builder = _default_builder()
    url = builder.create_url("/users/1.png", {"w": 400, "h": 300})
    assert url == "https://my-social-network.imgix.net/users/1.png?h=300&w=400"


def test_create_url_with_params_kwarg():
    builder = _default_builder()
    url = builder.create_url("/users/1.png", params={"w": 400, "h": 300})
    assert url == "https://my-social-network.imgix.net/users/1.png?h=300&w=400"


def test_create_url_with_splatted_falsy_parameter():
    builder = _default_builder()
    url = builder.create_url("/users/1.png", {"or": 0})
    assert url == "https://my-social-network.imgix.net/users/1.png?or=0"


def test_create_url_with_path_and_signature():
    builder = _default_builder_with_signature()
    url = builder.create_url("/users/1.png")
    assert url == \
        "https://my-social-network.imgix.net/users/1.png" \
        "?s=6797c24146142d5b40bde3141fd3600c"


def test_create_url_with_path_and_paremeters_and_signature():
    builder = _default_builder_with_signature()
    url = builder.create_url("/users/1.png", {"w": 400, "h": 300})
    assert url == \
        "https://my-social-network.imgix.net/users/1.png" \
        "?h=300&w=400&s=1a4e48641614d1109c6a7af51be23d18"


def test_create_url_with_fully_qualified_url():
    builder = _default_builder_with_signature()
    url = builder.create_url("http://avatars.com/john-smith.png")
    assert url == \
        "https://my-social-network.imgix.net/"\
        "http%3A%2F%2Favatars.com%2Fjohn-smith.png" \
        "?s=493a52f008c91416351f8b33d4883135"


def test_create_url_with_fully_qualified_url_with_tilde():
    builder = _default_builder()
    url = builder.create_url("http://avatars.com/john~smith.png")
    assert url == \
        "https://my-social-network.imgix.net/"\
        "http%3A%2F%2Favatars.com%2Fjohn~smith.png"


def test_create_url_with_fully_qualified_url_and_parameters():
    builder = _default_builder_with_signature()
    url = builder.create_url("http://avatars.com/john-smith.png",
                             {"w": 400, "h": 300})
    assert url == \
        "https://my-social-network.imgix.net/" \
        "http%3A%2F%2Favatars.com%2Fjohn-smith.png" \
        "?h=300&w=400&s=a201fe1a3caef4944dcb40f6ce99e746"


def test_use_https():
    # Defaults to https
    builder = imgix.UrlBuilder('my-social-network.imgix.net')
    url = builder.create_url("/users/1.png")
    assert urlparse(url).scheme == "https"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', use_https=False)
    url = builder.create_url("/users/1.png")
    assert urlparse(url).scheme == "http"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', True)
    url = builder.create_url("/users/1.png")
    assert urlparse(url).scheme == "https"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', use_https=True)
    url = builder.create_url("/users/1.png")
    assert urlparse(url).scheme == "https"


def test_utf_8_characters():
    builder = _default_builder()
    url = builder.create_url(u'/ǝ')
    assert url == "https://my-social-network.imgix.net/%C7%9D"


def test_more_involved_utf_8_characters():
    builder = _default_builder()
    url = builder.create_url(u'/üsers/1/米国でのパーティーします。.png')
    assert url == \
        "https://my-social-network.imgix.net/%C3%BCsers/1/" \
        "%E7%B1%B3%E5%9B%BD%E3%81%A7%E3%81%AE%E3%83%91%E3%83%BC%E3%83" \
        "%86%E3%82%A3%E3%83%BC%E3%81%97%E3%81%BE%E3%81%99%E3%80%82.png"


def test_param_values_are_escaped():
    builder = _default_builder()
    url = builder.create_url('demo.png', {"hello world": "interesting"})

    assert url == "https://my-social-network.imgix.net/demo.png?" \
        "hello%20world=interesting"


def test_param_keys_are_escaped():
    builder = _default_builder()
    url = builder.create_url('demo.png', {
        "hello_world": "/foo\"> <script>alert(\"hacked\")</script><"})

    assert url == "https://my-social-network.imgix.net/demo.png?" \
        "hello_world=%2Ffoo%22%3E%20%3Cscript%3Ealert%28%22" \
        "hacked%22%29%3C%2Fscript%3E%3C"


def test_base64_param_variants_are_base64_encoded():
    builder = _default_builder()
    url = builder.create_url('~text', {
        "txt64": u"I cannøt belîév∑ it wors! 😱"})

    assert url == "https://my-social-network.imgix.net/~text?txt64=" \
        "SSBjYW5uw7h0IGJlbMOuw6l24oiRIGl0IHdvcu-jv3MhIPCfmLE"


def test_signing_url_with_ixlib():
    builder = imgix.UrlBuilder('my-social-network.imgix.net')
    url = builder.create_url("/users/1.png")
    assert url == (
        "https://my-social-network.imgix.net/users/1.png?ixlib=python-" +
        imgix._version.__version__)


def test_invalid_domain_append_slash():
    url_append_slash = 'assets.imgix.net/products'

    # Should fail if the expected error isn't raised
    try:
        imgix.UrlBuilder(url_append_slash)
    except ValueError:
        assert(True)
    else:
        assert(False)


def test_invalid_domain_prepend_scheme():
    url_prepend_protocol = 'https://assets.imgix.net'

    # Should fail if the expected error isn't raised
    try:
        imgix.UrlBuilder(url_prepend_protocol)
    except ValueError:
        assert(True)
    else:
        assert(False)


def test_invalid_domain_append_dash():
    url_append_dash = 'assets.imgix.net-products'

    # Should fail if the expected error isn't raised
    try:
        imgix.UrlBuilder(url_append_dash)
    except ValueError:
        assert(True)
    else:
        assert(False)


def test_include_library_param_true():
    url = ("https://assets.imgix.net/image.jpg?ixlib=python-" +
           imgix._version.__version__)
    ub = imgix.UrlBuilder("assets.imgix.net", include_library_param=True)

    assert url == ub.create_url("image.jpg")


def test_include_library_param_false():
    url = 'https://assets.imgix.net/image.jpg'
    ub = imgix.UrlBuilder("assets.imgix.net", include_library_param=False)

    assert url == ub.create_url("image.jpg")


def test_target_widths_default():
    expected = constants.SRCSET_TARGET_WIDTHS
    actual = urlbuilder.target_widths()
    assert len(actual) == len(expected)
    assert actual == expected


def test_target_widths_100_7401():
    idx_of_7401 = -1
    expected = constants.SRCSET_TARGET_WIDTHS[:idx_of_7401]
    actual = urlbuilder.target_widths(start=100, stop=7401)
    assert actual == expected


def test_target_widths_328_4087():
    idx_of_328, idx_of_4087 = 8, -5
    expected = constants.SRCSET_TARGET_WIDTHS[idx_of_328: idx_of_4087]
    actual = urlbuilder.target_widths(start=328, stop=4087)
    assert len(actual) == len(expected)
    assert actual[0] == expected[0]
    assert actual[-1] == expected[-1]


def test_target_widths_100_max():
    idx_of_100 = constants.SRCSET_TARGET_WIDTHS[0]
    idx_of_8192 = constants.SRCSET_TARGET_WIDTHS[-1]
    expected = [idx_of_100, idx_of_8192]
    actual = urlbuilder.target_widths(tol=10000000000)
    assert actual == expected
    assert actual[0] == IMAGE_MIN_WIDTH
    assert actual[-1] == IMAGE_MAX_WIDTH


def test_target_widths_328_to_328():
    expected = [328]
    actual = urlbuilder.target_widths(start=328, stop=328)
    assert actual == expected
