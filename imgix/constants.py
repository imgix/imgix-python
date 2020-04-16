import re

DOMAIN_PATTERN = re.compile(
            r'^(?:[a-z\d\-_]{1,62}\.){0,125}'
            r'(?:[a-z\d](?:\-(?=\-*[a-z\d])|[a-z]|\d){0,62}\.)'
            r'[a-z\d]{1,63}$'
        )

# The srcset width tolerance dictates the _maximum tolerated size_
# difference between an image's downloaded size and its rendered size.
# For example, setting this value to 0.1 means that an image will not
# render more than 10% larger or smaller than its native size.
SRCSET_WIDTH_TOLERANCE = 8

# The minimum srcset width tolerance.
SRCSET_MIN_WIDTH_TOLERANCE = 1

SRCSET_MAX_SIZE = 8192

# Representation of an image with a width of zero. This value is used
# in validation contexts, i.e. "is the width of the passed or requested
# image greater than or equal to the 'zero width image'."
IMAGE_ZERO_WIDTH = 0

# The minimum width of a default generated image-width.
IMAGE_MIN_WIDTH = 100

# The maximum width of a default generate image-width.
IMAGE_MAX_WIDTH = 8192


def _target_widths():
    resolutions = []
    prev = 100

    def ensure_even(n):
        return 2 * round(n/2.0)

    while prev <= SRCSET_MAX_SIZE:
        resolutions.append(int(ensure_even(prev)))
        prev *= 1 + (SRCSET_WIDTH_TOLERANCE / 100.0) * 2

    resolutions.append(SRCSET_MAX_SIZE)
    return resolutions


SRCSET_TARGET_WIDTHS = _target_widths()
