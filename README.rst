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
