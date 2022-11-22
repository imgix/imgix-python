<!-- ix-docs-ignore -->
![imgix logo](https://assets.imgix.net/sdk-imgix-logo.svg)

`imgix-python` is a client library for generating image URLs with [imgix](https://www.imgix.com/).

[![Version](https://img.shields.io/pypi/v/imgix.svg)](https://pypi.org/project/imgix/)
[![Build Status](https://travis-ci.com/imgix/imgix-python.svg?branch=main)](https://travis-ci.com/imgix/imgix-python)
![Downloads](https://img.shields.io/pypi/dm/imgix)
![Python Versions](https://img.shields.io/pypi/pyversions/imgix)
[![License](https://img.shields.io/github/license/imgix/imgix-python)](https://github.com/imgix/imgix-python/blob/main/LICENSE)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fimgix%2Fimgix-python.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fimgix%2Fimgix-python?ref=badge_shield)

---
<!-- /ix-docs-ignore -->

- [Installation](#installation)
- [Usage](#usage)
- [Signed URLs](#signed-urls)
- [Disabled Path Encoding](#disabled-path-encoding)
- [Srcset Generation](#srcset-generation)
    * [Fixed-Width Images](#fixed-width-images)
        + [Variable Quality](#variable-quality)
    * [Fluid-Width Images](#fluid-width-images)
        + [Custom Widths](#custom-widths)
        + [Width Ranges](#width-ranges)
        + [Width Tolerance](#width-tolerance)
        + [Explore Target Widths](#explore-target-widths)
    * [Usage with UTF-8](#usage-with-utf-8)
- [The `ixlib` Parameter](#the-ixlib-parameter)
- [Testing](#testing)
- [License](#license)

## Installation

``` bash
pip install imgix
```

## Usage

To begin creating imgix URLs, import the imgix library and create a URL builder. The URL builder can be reused to create URLs for any images on the domains it is provided.

``` python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder("demo.imgix.net")
>>> ub.create_url("bridge.png", {'w': 100, 'h': 100})
'https://demo.imgix.net/bridge.png?h=100&w=100'

```

_HTTPS_ support is enabled by default. _HTTP_ can be toggled on by setting `use_https` to `False`:

``` python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder("demo.imgix.net", use_https=False)
>>> ub.create_url("/bridge.png", {'w': 100, 'h': 100})
'http://demo.imgix.net/bridge.png?h=100&w=100'

```

## Signed URLs

To produce a signed URL, you must enable secure URLs on your source and then provide your signature key to the URL builder.

``` python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder("demo.imgix.net", sign_key="test1234")
>>> ub.create_url("/bridge.png", {'w': 100, 'h': 100})
'https://demo.imgix.net/bridge.png?h=100&w=100&s=bb8f3a2ab832e35997456823272103a4'

```

## Disabled Path Encoding

Path encoding is enabled by default. It can be toggled off by setting `disable_path_encoding` to `True` in the optional `options` paramater in `create_url()` and `create_srcset()` functions:

```python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder("sdk-test.imgix.net")
>>> ub.create_url(" <>[]{}|^%.jpg", params={'w': 100, 'h': 100}, options={'disable_path_encoding': True})
'https://sdk-test.imgix.net/ <>[]{}|^%.jpg?h=100&w=100'
```

Normally this would output a source URL like `https://demo.imgix.net/%20%3C%3E%5B%5D%7B%7D%7C%5E%25.jpg?h=100&2=100`, but since path encoding is disabled, it will output a source URL like `https://sdk-test.imgix.net/ <>[]{}|^%.jpg?h=100&w=100`.

```python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder("sdk-test.imgix.net")
>>> ub.create_srcset("image<>[]{} 123.png", widths=[100], options={'disable_path_encoding': True})
'https://sdk-test.imgix.net/image<>[]{} 123.png?w=100 100w'
```
Normally this would output a source URL like `https://sdk-test.imgix.net/image%3C%3E%5B%5D%7B%7D%20123.png?&w=100 100w`, but since path encoding is disabled, it will output a source URL like `https://sdk-test.imgix.net//image<>[]{} 123.png?w=100 100w`.

## Srcset Generation

The imgix-python package allows for generation of custom srcset attributes, which can be invoked through the `create_srcset` method. By default, the generated srcset will allow for responsive size switching by building a list of image-width mappings.

``` python
import os
from imgix import UrlBuilder

# Keep Your Secrets Safe!
SECRET = os.getenv("IX_SIGN_KEY")
ub = UrlBuilder("demos.imgix.net", sign_key=SECRET)
srcset = ub.create_srcset("image.png")
```

The above will produce the following srcset attribute value which can then be served to the client: 

``` html
https://demos.imgix.net/image.png?w=100&s=e415797545a77a9d2842dedcfe539c9a 100w,
https://demos.imgix.net/image.png?w=116&s=b2da46f5c23ef13d5da30f0a4545f33f 116w,
https://demos.imgix.net/image.png?w=135&s=b61422dead929f893c04b8ff839bb088 135w,
                                        ...
https://demos.imgix.net/image.png?w=7401&s=ad671301ed4663c3ce6e84cb646acb96 7401w,
https://demos.imgix.net/image.png?w=8192&s=a0fed46e2bbcc70ded13dc629aee5398 8192w
```

### Fixed-Width Images

In cases where enough information is provided about an image's dimensions, `create_srcset` will instead build a srcset that will allow for an image to be served at different resolutions. The parameters taken into consideration when determining if an image is fixed-width are `w`, `h`, and `ar`.

By invoking `create_srcset` with either a width **or** the height and aspect ratio (along with `fit=crop`, typically) provided, a different srcset will be generated for a fixed-width image instead.

``` python
from imgix import UrlBuilder
>>> ub = UrlBuilder("demos.imgix.net", sign_key="my-token")
>>> srcset = ub.create_srcset("image.png", {'h':800, 'ar':'3:2', 'fit':'crop'})

```

Will produce the following attribute value:

``` html
https://demos.imgix.net/image.png?ar=3%3A2&dpr=1&fit=crop&h=800&s=6cf5c443d1eb98bc3d96ea569fcef088 1x,
https://demos.imgix.net/image.png?ar=3%3A2&dpr=2&fit=crop&h=800&s=d60a61a5f34545922bd8dff4e53a0555 2x,
https://demos.imgix.net/image.png?ar=3%3A2&dpr=3&fit=crop&h=800&s=590f96aa426f8589eb7e449ebbeb66e7 3x,
https://demos.imgix.net/image.png?ar=3%3A2&dpr=4&fit=crop&h=800&s=c89c2fd3148957647e86cfc32ba20517 4x,
https://demos.imgix.net/image.png?ar=3%3A2&dpr=5&fit=crop&h=800&s=3d73af69d78d49eef0f81b4b5d718a2c 5x
```

By default, this library generates a `srcset` with pixel density values of `1` through `5`.
These target ratios can be controlled by using the `devicePixelRatios` parameters.

```python
from imgix import UrlBuilder
client = UrlBuilder("demo.imgix.net")
client.create_srcset(
  "image.jpg",
  { "w": 100 },
  {
    "device_pixel_ratios": [ 1, 2, 3 ]
  }
)
```
Will produce the following attribute value:
```html
https://demo.imgix.net/image.jpg?dpr=1&ixlib=python-3.2.1&q=75&w=100 1x,
https://demo.imgix.net/image.jpg?dpr=2&ixlib=python-3.2.1&q=50&w=100 2x,
https://demo.imgix.net/image.jpg?dpr=3&ixlib=python-3.2.1&q=35&w=100 3x'
```

For more information to better understand srcset, we highly recommend
[Eric Portis' "Srcset and sizes" article](https://ericportis.com/posts/2014/srcset-sizes/) which goes into depth about the subject.

#### Variable Quality

This library will automatically append a variable `q` parameter mapped to each `dpr` parameter when generating a [fixed-width image](#fixed-width-images) srcset. This technique is commonly used to compensate for the increased file size of high-DPR images.

Since high-DPR images are displayed at a higher pixel density on devices, image quality can be lowered to reduce overall file size––without sacrificing perceived visual quality. For more information and examples of this technique in action, see [this blog post](https://blog.imgix.com/2016/03/30/dpr-quality).

This behavior will respect any overriding `q` value passed in as a parameter. Additionally, it can be disabled altogether by passing `disable_variable_quality = true` to `create_srcset`.

This behavior specifically occurs when a [fixed-width image](#fixed-width-images) is rendered, for example:

```python
# Note that `params={"w": 100}` allows `create_srcset` to _infer_ the creation
# of a DPR based srcset attribute for fixed-width images.
ub = imgix.UrlBuilder('demo.imgix.net')
# Set `disable_variable_quality` to True to disable variable quality.
srcset = ub.create_srcset('image.jpg', params={"w": 100}, disable_variable_quality=False)
```

The above will generate a srcset with the following `q` to `dpr` query `params`:

```html
https://demo.imgix.net/image.jpg?w=100&dpr=1&q=75 1x,
https://demo.imgix.net/image.jpg?w=100&dpr=2&q=50 2x,
https://demo.imgix.net/image.jpg?w=100&dpr=3&q=35 3x,
https://demo.imgix.net/image.jpg?w=100&dpr=4&q=23 4x,
https://demo.imgix.net/image.jpg?w=100&dpr=5&q=20 5x
```

By default, this library will automatically append a variable `q` parameter mapped to each `dpr` parameter when generating a [fixed-width image](#fixed-width-images) srcset.

To customize variable qualities, you can pass a `variable_qualities` dictionary in the `options` while creating srcset as below:
```python
from imgix import UrlBuilder
client = UrlBuilder("demo.imgix.net")
client.create_srcset("image.jpg", {"w": 100}, {"variable_qualities": {1: 45, 2: 30, 3: 20, 4: 15, 5: 10}})
```
The above script will produce the following output:
```bash
https://demo.imgix.net/image.jpg?dpr=1&q=45&w=100 1x
https://demo.imgix.net/image.jpg?dpr=2&q=30&w=100 2x
https://demo.imgix.net/image.jpg?dpr=3&q=20&w=100 3x
https://demo.imgix.net/image.jpg?dpr=4&&q=15&w=100 4x
https://demo.imgix.net/image.jpg?dpr=5&q=10&w=100 5x
``` 

You can also pass `variable_qualities` along with the `device_pixel_ratios` option as below:
```python
from imgix import UrlBuilder
client = UrlBuilder("demo.imgix.net")
client.create_srcset(
  "image.jpg",
  { "w": 100 },
  {
    "device_pixel_ratios": [ 1, 2, 3 ],
    "variable_qualities": { 1: 45, 2: 30, 3: 20 }
  }
)
```
The above script will produce the following output:
```html
https://testing.imgix.net/image.jpg?dpr=1&q=45&w=100 1x,
https://testing.imgix.net/image.jpg?dpr=2&q=30&w=100 2x,
https://testing.imgix.net/image.jpg?dpr=3&q=20&w=100 3x
```

### Fluid-Width Images

#### Custom Widths

In situations where specific widths are desired when generating `srcset` pairs, a user can specify them by passing an array of positive integers as `widths`:

``` python
>>> from imgix import UrlBuilder
>>> builder = UrlBuilder('demo.imgix.net')
>>> builder.create_srcset('image.jpg', widths=[144, 240, 320, 446, 640])
'https://demo.imgix.net/image.jpg?w=144 144w,\nhttps://demo.imgix.net/image.jpg?w=240 240w,\nhttps://demo.imgix.net/image.jpg?w=320 320w,\nhttps://demo.imgix.net/image.jpg?w=446 446w,\nhttps://demo.imgix.net/image.jpg?w=640 640w'

```

```html
https://demo.imgix.net/image.jpg?w=144 144w,
https://demo.imgix.net/image.jpg?w=240 240w,
https://demo.imgix.net/image.jpg?w=320 320w,
https://demo.imgix.net/image.jpg?w=446 446w,
https://demo.imgix.net/image.jpg?w=640 640w
```

**Note**: in situations where a `srcset` is being rendered as a [fixed-width](#fixed-width-images) srcset, any custom `widths` passed in will be ignored.

Additionally, if both `widths` and a width `tol`erance are passed to the `create_srcset` method, the custom widths list will take precedence.

#### Width Ranges

In certain circumstances, you may want to limit the minimum or maximum value of the non-fixed `srcset` generated by the `create_srcset` method. To do this, you can specify the widths at which a srcset should `start` and `stop`:

```python
>>> from imgix import UrlBuilder
>>> ub = UrlBuilder('demo.imgix.net')
>>> ub.create_srcset('image.jpg', start=500, stop=2000)
'https://demo.imgix.net/image.jpg?w=500 500w,\nhttps://demo.imgix.net/image.jpg?w=580 580w,\nhttps://demo.imgix.net/image.jpg?w=673 673w,\nhttps://demo.imgix.net/image.jpg?w=780 780w,\nhttps://demo.imgix.net/image.jpg?w=905 905w,\nhttps://demo.imgix.net/image.jpg?w=1050 1050w,\nhttps://demo.imgix.net/image.jpg?w=1218 1218w,\nhttps://demo.imgix.net/image.jpg?w=1413 1413w,\nhttps://demo.imgix.net/image.jpg?w=1639 1639w,\nhttps://demo.imgix.net/image.jpg?w=1901 1901w,\nhttps://demo.imgix.net/image.jpg?w=2000 2000w'

```

Formatted version of the above srcset attribute:

``` html
https://demo.imgix.net/image.jpg?w=500 500w,
https://demo.imgix.net/image.jpg?w=580 580w,
https://demo.imgix.net/image.jpg?w=673 673w,
https://demo.imgix.net/image.jpg?w=780 780w,
https://demo.imgix.net/image.jpg?w=905 905w,
https://demo.imgix.net/image.jpg?w=1050 1050w,
https://demo.imgix.net/image.jpg?w=1218 1218w,
https://demo.imgix.net/image.jpg?w=1413 1413w,
https://demo.imgix.net/image.jpg?w=1639 1639w,
https://demo.imgix.net/image.jpg?w=1901 1901w,
https://demo.imgix.net/image.jpg?w=2000 2000w'
```

#### Width Tolerance

The `srcset` width `tol`erance dictates the maximum `tol`erated difference between an image's downloaded size and its rendered size.

For example, setting this value to `0.10` means that an image will not render more than 10% larger or smaller than its native size. In practice, the image URLs generated for a width-based srcset attribute will grow by twice this rate.

A lower tolerance means images will render closer to their native size (thereby increasing perceived image quality), but a large srcset list will be generated and consequently users may experience lower rates of cache-hit for pre-rendered images on your site.

By default, srcset width `tol`erance is set to 0.08 (8 percent), which we consider to be the ideal rate for maximizing cache hits without sacrificing visual quality. Users can specify their own width tolerance by providing a positive scalar value as width `tol`erance:

```python
>>> import imgix
>>> ub = imgix.UrlBuilder('demo.imgix.net')
>>> srcset = ub.create_srcset('image.jpg', start=100, stop=384, tol=0.20)

```

In this case, the `width_tolerance` is set to 20 percent, which will be reflected in the difference between subsequent widths in a srcset pair:

```html
https://demo.imgix.net/image.jpg?w=100 100w,
https://demo.imgix.net/image.jpg?w=140 140w,
https://demo.imgix.net/image.jpg?w=196 196w,
https://demo.imgix.net/image.jpg?w=274 274w,
https://demo.imgix.net/image.jpg?w=384 384w
```

#### Explore Target Widths

The `target_widths` function is used internally to generate lists of target widths to be used in calls to `create_srcset`.

It is a way to generate, play with, and explore different target widths separately from srcset attributes. One way of generating a srcset attribute is:

```python
srcset = ub.create_srcset('image.jpg', start=300, stop=3000, tol=0.13)
```

The above is convenient if `start`, `stop`, and `tol`erance are known in advance. Another approach is to use `target_widths` to determine which combination of values for `start`, `stop`, and `tol`erance work best.

```python
>>> from imgix import UrlBuilder, target_widths
>>> # Create
>>> widths = target_widths(300, 3000, 0.13)
>>> widths
[300, 378, 476, 600, 756, 953, 1200, 1513, 1906, 2401, 3000]
>>> # Explore
>>> sm, md, lg = widths[:3], widths[3:7], widths[7:]
>>> widths = [w for w in widths[1::2]]
>>> widths
[378, 600, 953, 1513, 2401]
>>> # Serve
>>> ub = UrlBuilder('demo.imgix.net')
>>> srcset = ub.create_srcset('image.png', widths=widths)
>>> srcset
'https://demo.imgix.net/image.png?w=378 378w,\nhttps://demo.imgix.net/image.png?w=600 600w,\nhttps://demo.imgix.net/image.png?w=953 953w,\nhttps://demo.imgix.net/image.png?w=1513 1513w,\nhttps://demo.imgix.net/image.png?w=2401 2401w'

```

### Usage with UTF-8

For usage with non-ASCII characters, please be sure that your project's source files specify UTF-8 encoding:

``` python
# -*- coding: utf-8 -*-
```

If you don't add this encoding, and you have an image with the name 'tiburón.jpeg', for example, you will get the following error trying to run your script:

``` python
SyntaxError: Non-ASCII character '***' in file test.py on line 6, but no encoding declared; see http://www.python.org/peps/pep-0263.html for details
```

## The `ixlib` Parameter

For security and diagnostic purposes, we sign all requests with the language and version of library used to generate the URL.

This can be disabled by setting `include_library_param` to `False` like so:

``` python
UrlBuilder('demo.imgix.net', include_library_param=False)
```

## Testing

Run the following to execute the project's tests and code linter:

``` bash
tox
```

If you have cloned this repo or downloaded it locally, you can also run `python -m doctest -v README.md` to test the examples in this readme.

## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fimgix%2Fimgix-python.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fimgix%2Fimgix-python?ref=badge_large)
