imgix-python
============

A Python client library for generating URLs with imgix.

Basic Usage
-----------

    import imgix

	builder = imgix.Builder("demo.imgix.net")
	print builder.create_url("/bridge.png", w=100, h=100, fit=crop)

	# Prints out: http://demo.imgix.net/bridge.png?fit=crop&h=100&w=100


