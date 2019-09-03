.. image:: https://assets.imgix.net/imgix-logo-web-2014.pdf?page=2&fm=png&w=200&h=200
        :alt: imgix logo

.. image:: https://travis-ci.org/imgix/imgix-python.png?branch=master
        :alt: Build Status
        :target: https://travis-ci.org/imgix/imgix-python

A Python client library for generating URLs with imgix. imgix is a high-performance
distributed image processing service. More information can be found at
http://www.imgix.com.

Installation
------------

.. code-block:: bash

    $ pip install imgix

Basic Usage
-----------

To begin creating imgix URLs programmatically, simply import the imgix library
and create a URL builder. The URL builder can be reused to create URLs for any
images on the domains it is provided.


.. code-block:: python

    import imgix

    builder = imgix.UrlBuilder("demos.imgix.net")
    print builder.create_url("/bridge.png", {'w': 100, 'h': 100})

    # Prints out:
    # http://demos.imgix.net/bridge.png?h=100&w=100

For HTTPS support, simply specify the HTTPS flag like so:

.. code-block:: python

    import imgix

    builder = imgix.UrlBuilder("demos.imgix.net", use_https=True)
    print builder.create_url("/bridge.png", {'w': 100, 'h': 100})

    # Prints out:
    # https://demos.imgix.net/bridge.png?h=100&w=100

Signed URLs
-----------

To produce a signed URL, you must enable secure URLs on your source and then
provide your signature key to the URL builder.

.. code-block:: python

    import imgix

    builder = imgix.UrlBuilder("demos.imgix.net", sign_key="test1234")
    print builder.create_url("/bridge.png", {'w': 100, 'h': 100})

    # Prints out:
    # http://demos.imgix.net/bridge.png?h=100&w=100&s=7370d6e36bb2262e73b19578739af1af

Srcset Generation
-----------------

The imgix-python package allows for generation of custom srcset attributes, which can be invoked through :code:`create_srcset()`. By default, the srcset generated will allow for responsive size switching by building a list of image-width mappings.

.. code-block:: python

    builder = imgix.UrlBuilder("demos.imgix.net", sign_key="my-token", include_library_param=False)
    srcset = builder.create_srcset("image.png")
    print srcset

Will produce the following attribute value, which can then be served to the client:

.. code-block:: html

    https://demos.imgix.net/image.png?w=100&s=e415797545a77a9d2842dedcfe539c9a 100w,
    https://demos.imgix.net/image.png?w=116&s=b2da46f5c23ef13d5da30f0a4545f33f 116w,
    https://demos.imgix.net/image.png?w=134&s=b61422dead929f893c04b8ff839bb088 134w,
                                            ...
    https://demos.imgix.net/image.png?w=7400&s=ad671301ed4663c3ce6e84cb646acb96 7400w,
    https://demos.imgix.net/image.png?w=8192&s=a0fed46e2bbcc70ded13dc629aee5398 8192w

In cases where enough information is provided about an image's dimensions, :code:`create_srcset()` will instead build a srcset that will allow for an image to be served at different resolutions. The parameters taken into consideration when determining if an image is fixed-width are :code:`w`, :code:`h`, and :code:`ar`. By invoking :code:`create_srcset()` with either a width **or** the height and aspect ratio (along with :code:`fit=crop`, typically) provided, a different srcset will be generated for a fixed-size image instead.

.. code-block:: python

    builder = imgix.UrlBuilder("demos.imgix.net", sign_key="my-token", include_library_param=False)
    srcset = builder.create_srcset("image.png", {'h':800, 'ar':'3:2', 'fit':'crop'})
    print srcset

Will produce the following attribute value:

.. code-block:: html

    https://demos.imgix.net/image.png?ar=3%3A2&dpr=1&fit=crop&h=800&s=6cf5c443d1eb98bc3d96ea569fcef088 1x,
    https://demos.imgix.net/image.png?ar=3%3A2&dpr=2&fit=crop&h=800&s=d60a61a5f34545922bd8dff4e53a0555 2x,
    https://demos.imgix.net/image.png?ar=3%3A2&dpr=3&fit=crop&h=800&s=590f96aa426f8589eb7e449ebbeb66e7 3x,
    https://demos.imgix.net/image.png?ar=3%3A2&dpr=4&fit=crop&h=800&s=c89c2fd3148957647e86cfc32ba20517 4x,
    https://demos.imgix.net/image.png?ar=3%3A2&dpr=5&fit=crop&h=800&s=3d73af69d78d49eef0f81b4b5d718a2c 5x

For more information to better understand srcset, we highly recommend `Eric Portis' "Srcset and sizes" article <https://ericportis.com/posts/2014/srcset-sizes/>`_ which goes into depth about the subject.

Usage with UTF-8
----------------

For usage with non-ASCII characters, please be sure to that your project’s source files specify UTF-8 encoding:

.. code-block:: python

    # -*- coding: utf-8 -*-

If you don't add this encoding, and you have an image with name for example 'tiburón.jpeg', you will get the following error trying to run your script:

.. code-block:: python

    SyntaxError: Non-ASCII character '***' in file test.py on line 6, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details

Running Tests
-------------

To run the tests and format the code, simply:

.. code-block:: bash

    tox
