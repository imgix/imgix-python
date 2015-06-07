# -*- coding: utf-8 -*-

import imgix
import urlparse

def default_builder():
    return imgix.UrlBuilder('my-social-network.imgix.net')

def default_builder_with_signature():
    return imgix.UrlBuilder('my-social-network.imgix.net', False, "FOO123bar")

def test_smoke():
    assert True

def test_url_builder_create():
    builder = imgix.UrlBuilder('my-social-network.imgix.net')
    assert type(builder) is imgix.UrlBuilder

def test_url_builder_create_url_with_path():
    builder = default_builder()
    url = builder.create_url("/users/1.png")
    assert url == "http://my-social-network.imgix.net/users/1.png"

def test_url_builder_create_url_with_path_and_parameters():
    builder = default_builder()
    url = builder.create_url("/users/1.png", w=400, h=300)
    assert url == "http://my-social-network.imgix.net/users/1.png?h=300&w=400"

def test_url_builder_create_url_with_path_and_signature():
    builder = default_builder_with_signature()
    url = builder.create_url("/users/1.png")
    assert url == "http://my-social-network.imgix.net/users/1.png?s=6797c24146142d5b40bde3141fd3600c"

def test_url_builder_create_url_with_path_and_paremeters_and_signature():
    builder = default_builder_with_signature()
    url = builder.create_url("/users/1.png", w=400, h=300)
    assert url == "http://my-social-network.imgix.net/users/1.png?h=300&w=400&s=1a4e48641614d1109c6a7af51be23d18"

def test_url_builder_create_url_with_fully_qualified_url():
    builder = default_builder_with_signature()
    url = builder.create_url("http://avatars.com/john-smith.png")
    assert url == "https://my-social-network.imgix.net/http%3A%2F%2Favatars.com%2Fjohn-smith.png?s=493a52f008c91416351f8b33d4883135"

def test_url_builder_create_url_with_fully_qualified_url_and_parameters():
    builder = default_builder_with_signature()
    url = builder.create_url("http://avatars.com/john-smith.png", w=400, h=300)
    assert url == "https://my-social-network.imgix.net/http%3A%2F%2Favatars.com%2Fjohn-smith.png?h=300&w=400&s=a201fe1a3caef4944dcb40f6ce99e746"

def test_url_builder_use_https():
    # Defaults to http
    builder = imgix.UrlBuilder('my-social-network.imgix.net')
    url = builder.create_url("/users/1.png")
    assert urlparse.urlparse(url).scheme == "http"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', use_https=False)
    url = builder.create_url("/users/1.png")
    assert urlparse.urlparse(url).scheme == "http"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', True)
    url = builder.create_url("/users/1.png")
    assert urlparse.urlparse(url).scheme == "https"

    builder = imgix.UrlBuilder('my-social-network.imgix.net', use_https=True)
    url = builder.create_url("/users/1.png")
    assert urlparse.urlparse(url).scheme == "https"