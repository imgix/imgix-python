![imgix logo](https://assets.imgix.net/imgix-logo-web-2014.pdf?page=2&fm=png&w=200&h=200)

[![Build Status](https://travis-ci.org/imgix/imgix-python.png?branch=master)](https://travis-ci.org/imgix/imgix-python)

A Python client library for generating URLs with imgix. imgix is a high-performance
distributed image processing service. More information can be found at
[http://www.imgix.com](http://www.imgix.com).

Installation
------------

To install the library from source, run the following command from inside
the root folder of the source code:

```bash
$ sudo python setup.py build install
```


Basic Usage
-----------

To begin creating imgix URLs programmatically, simply import the imgix library
and create a URL builder. The URL builder can be reused to create URLs for any
images on the domains it is provided.


```python
import imgix

builder = imgix.UrlBuilder("demos.imgix.net")
print builder.create_url("/bridge.png", w=100, h=100)

# Prints out:
# http://demos.imgix.net/bridge.png?h=100&w=100
```

For HTTPS support, simply specify the HTTPS flag like so:

```python
import imgix

builder = imgix.UrlBuilder("demos.imgix.net", use_https=True)
print builder.create_url("/bridge.png", w=100, h=100)

# Prints out:
# https://demos.imgix.net/bridge.png?h=100&w=100
```

Signed URLs
-----------

To produce a signed URL, you must enable secure URLs on your source and then
provide your signature key to the URL builder.

```python
import imgix

builder = imgix.UrlBuilder("demos.imgix.net", sign_key="test1234")
print builder.create_url("/bridge.png", w=100, h=100)

# Prints out:
# http://demos.imgix.net/bridge.png?h=100&w=100&s=7370d6e36bb2262e73b19578739af1af
```


Domain Sharded URLs
-------------------

Domain sharding enables you to spread image requests across multiple domains.
This allows you to bypass the requests-per-host limits of browsers. We
recommend 2-3 domain shards maximum if you are going to use domain sharding.

In order to use domain sharding, you need to add multiple domains to your
source. You then provide a list of these domains to a builder.

```python
import imgix

builder = imgix.UrlBuilder([
    "demos-1.imgix.net",
    "demos-2.imgix.net",
    "demos-3.imgix.net",
])

print builder.create_url("/bridge.png", w=100, h=100)
print builder.create_url("/flower.png", w=100, h=100)

# Prints out:
# http://demos-2.imgix.net/bridge.png?h=100&w=100
# http://demos-3.imgix.net/flower.png?h=100&w=100
```

By default, shards are calculated using a checksum so that the image path
always resolves to the same domain. This improves caching in the browser.
However, you can supply a different strategy that cycles through domains
instead. For example:

```python
import imgix

builder = imgix.UrlBuilder([
    "demos-1.imgix.net",
    "demos-2.imgix.net",
    "demos-3.imgix.net",
], shard_strategy=imgix.SHARD_STRATEGY_CYCLE)

for i in xrange(4):
    print builder.create_url("/bridge.png", w=100, h=100)

# Prints out:
# http://demos-1.imgix.net/bridge.png?h=100&w=100
# http://demos-2.imgix.net/bridge.png?h=100&w=100
# http://demos-3.imgix.net/bridge.png?h=100&w=100
# http://demos-1.imgix.net/bridge.png?h=100&w=100
```

Usage with UTF-8
---------------------------------------------------

For usage with non-ASCII characters, please be sure to that your project’s source files specify UTF-8 encoding:

```python
# -*- coding: utf-8 -*-
```

If you don't add this encoding, and you have an image with name for example 'tiburón.jpeg', you will get the following error trying to run your script:

```
SyntaxError: Non-ASCII character '***' in file test.py on line 6, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
```
