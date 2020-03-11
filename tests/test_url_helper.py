# -*- coding: utf-8 -*-
import imgix

from future.moves.urllib.parse import urlparse
from imgix.urlhelper import UrlHelper


def test_create():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png')
    assert type(helper) is UrlHelper


def test_create_with_url_parameters():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       include_library_param=False,
                       params={"w": 400, "h": 300})
    assert str(helper) == "https://my-social-network.imgix.net/users/1.png?" \
                          "h=300&w=400"


def test_create_with_splatted_falsy_parameter():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       include_library_param=False,
                       params={"or": 0})
    assert str(helper) == "https://my-social-network.imgix.net" \
                          "/users/1.png?or=0"


def test_create_with_signature():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       sign_key="FOO123bar",
                       include_library_param=False)
    assert str(helper) == \
        "https://my-social-network.imgix.net/users/1.png" \
        "?s=6797c24146142d5b40bde3141fd3600c"


def test_create_with_paremeters_and_signature():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       sign_key="FOO123bar",
                       include_library_param=False,
                       params={"w": 400, "h": 300})
    assert str(helper) == \
        "https://my-social-network.imgix.net/users/1.png" \
        "?h=300&w=400&s=1a4e48641614d1109c6a7af51be23d18"


def test_create_with_fully_qualified_url():
    helper = UrlHelper("my-social-network.imgix.net",
                       "http://avatars.com/john-smith.png",
                       sign_key="FOO123bar",
                       include_library_param=False)
    assert str(helper) == \
        "https://my-social-network.imgix.net/"\
        "http%3A%2F%2Favatars.com%2Fjohn-smith.png" \
        "?s=493a52f008c91416351f8b33d4883135"


def test_create_with_fully_qualified_url_with_special_chars():
    helper = UrlHelper("my-social-network.imgix.net",
                       u"http://avatars.com/でのパ.png",
                       sign_key="FOO123bar",
                       include_library_param=False)
    assert str(helper) == "https://my-social-network.imgix.net/http%3A%2F%2F" \
                          "avatars.com%2F%E3%81%A7%E3%81%AE%E3%83%91.png" \
                          "?s=8e04a5dd9a659a6a540d7c817d3df1d3"


def test_create_with_mixed_strings_and_unicodes():
    helper = UrlHelper("my-social-network.imgix.net",
                       u"http://avatars.com/でのパ.png",
                       sign_key="FOO123bar",
                       params={"w": '400', u"h": u'300'},
                       include_library_param=False)
    assert str(helper) == "https://my-social-network.imgix.net/http%3A%2F%2F" \
                          "avatars.com%2F%E3%81%A7%E3%81%AE%E3%83%91.png" \
                          "?h=300&w=400&s=8b97a8fffdfa639af4bae846a9661c50"


def test_use_https():
    # Defaults to https
    helper = UrlHelper("my-social-network.imgix.net", "/users/1.png")
    assert urlparse(str(helper)).scheme == "https"

    helper = UrlHelper('my-social-network.imgix.net', "/users/1.png",
                       scheme="http")
    assert urlparse(str(helper)).scheme == "http"


def test_utf_8_characters():
    helper = UrlHelper('my-social-network.imgix.net', u'/ǝ',
                       include_library_param=False)
    assert str(helper) == "https://my-social-network.imgix.net/%C7%9D"


def test_more_involved_utf_8_characters():
    helper = UrlHelper('my-social-network.imgix.net',
                       u'/üsers/1/でのパ.png',
                       include_library_param=False)
    assert str(helper) == 'https://my-social-network.imgix.net/' \
                          '%C3%BCsers/1/%E3%81%A7%E3%81%AE%E3%83%91.png'


def test_param_values_are_escaped():
    helper = UrlHelper('my-social-network.imgix.net', 'demo.png',
                       params={"hello world": "interesting"},
                       include_library_param=False)

    assert str(helper) == "https://my-social-network.imgix.net/demo.png?" \
                          "hello%20world=interesting"


def test_param_keys_are_escaped():
    params = {"hello_world": "/foo\"> <script>alert(\"hacked\")</script><"}
    helper = UrlHelper('my-social-network.imgix.net', 'demo.png',
                       params=params,
                       include_library_param=False)

    assert str(helper) == "https://my-social-network.imgix.net/demo.png?" \
        "hello_world=%2Ffoo%22%3E%20%3Cscript%3Ealert%28%22" \
        "hacked%22%29%3C%2Fscript%3E%3C"


def test_base64_param_variants_are_base64_encoded():
    params = {"txt64": u"I cannøt belîév∑ it wors! 😱"}
    helper = UrlHelper('my-social-network.imgix.net', '~text',
                       params=params,
                       include_library_param=False)

    assert str(helper) == "https://my-social-network.imgix.net/~text?txt64=" \
        "SSBjYW5uw7h0IGJlbMOuw6l24oiRIGl0IHdvcu-jv3MhIPCfmLE"


def test_signing_url_with_ixlib():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png')
    assert str(helper) == (
        "https://my-social-network.imgix.net/users/1.png?ixlib=python-" +
        imgix._version.__version__)


def test_set_parameter():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       include_library_param=False)

    helper.set_parameter('w', 400)
    assert str(helper) == "https://my-social-network.imgix.net/" \
                          "users/1.png?w=400"

    helper.set_parameter('h', 300)
    assert str(helper) == "https://my-social-network.imgix.net/" \
                          "users/1.png?h=300&w=400"


def test_set_parameter_with_init_params():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       params={"or": 0},
                       include_library_param=False)

    helper.set_parameter('w', 400)
    helper.set_parameter('h', 300)
    assert str(helper) == "https://my-social-network.imgix.net" \
                          "/users/1.png?h=300&or=0&w=400"


def test_set_parameter_base64_encoded():
    helper = UrlHelper('my-social-network.imgix.net', '~text',
                       include_library_param=False)

    helper.set_parameter("txt64", u"I cannøt belîév∑ it wors! 😱")
    assert str(helper) == "https://my-social-network.imgix.net/~text?txt64=" \
                          "SSBjYW5uw7h0IGJlbMOuw6l24oiRIGl0IHdvcu-jv3MhIPCfmLE"


def test_set_parameter_with_none_value():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       params={'h': 300, 'w': 400},
                       include_library_param=False)

    helper.set_parameter("w", None)
    assert str(helper) == "https://my-social-network.imgix.net" \
                          "/users/1.png?h=300&w=None"


def test_set_parameter_with_false_value():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       params={'h': 300, 'w': 400},
                       include_library_param=False)

    helper.set_parameter("w", False)
    assert str(helper) == "https://my-social-network.imgix.net" \
                          "/users/1.png?h=300&w=False"


def test_delete_parameter():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       params={'h': 300, 'w': 400},
                       include_library_param=False)

    helper.delete_parameter('w')
    assert str(helper) == "https://my-social-network.imgix.net" \
                          "/users/1.png?h=300"


def test_delete_all_parameters():
    helper = UrlHelper('my-social-network.imgix.net', '/users/1.png',
                       params={'h': 300, 'w': 400},
                       include_library_param=False)

    helper.delete_parameter('w')
    helper.delete_parameter('h')
    assert str(helper) == "https://my-social-network.imgix.net/users/1.png"
