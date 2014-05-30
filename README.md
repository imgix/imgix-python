imgix-python
============

A Python client library for generating URLs with imgix.

Basic Usage
-----------

To begin creating imgix URLs programmatically, simply import the imgix library
and create a URL builder. The URL builder can be reused to create URLs for any
images on the domains it is provided.

    import imgix

	builder = imgix.UrlBuilder("demos.imgix.net")
	print builder.create_url("/bridge.png", w=100, h=100)

	# Prints out: http://demos.imgix.net/bridge.png?h=100&w=100

For HTTPS support, simply specify the HTTPS flag like so:

    import imgix

	builder = imgix.UrlBuilder("demos.imgix.net", use_https=True)
	print builder.create_url("/bridge.png", w=100, h=100)

	# Prints out: https://demos.imgix.net/bridge.png?h=100&w=100


Signed URLs
-----------

To produce a signed URL, you must enable secure URLs on your source and then
provide your signature key to the URL builder.

    import imgix

	builder = imgix.UrlBuilder("demos.imgix.net", sign_key="test1234")
	print builder.create_url("/bridge.png", w=100, h=100)

	# Prints out: http://demos.imgix.net/bridge.png?h=100&w=100
