import re

DOMAIN_PATTERN = re.compile(
            r'^(?:[a-z\d\-_]{1,62}\.){0,125}'
            r'(?:[a-z\d](?:\-(?=\-*[a-z\d])|[a-z]|\d){0,62}\.)'
            r'[a-z\d]{1,63}$'
        )

# The srcset width tolerance dictates the _maximum tolerated size_
# difference between an image's downloaded size and its rendered size.
# For example, setting this value to 10 means that an image will not
# render more than 10% larger or smaller than its native size.
SRCSET_WIDTH_TOLERANCE = 0.08

# The minimum srcset width tolerance.
SRCSET_MIN_WIDTH_TOLERANCE = 0.01

# The default srcset target ratios.
SRCSET_DPR_TARGET_RATIOS = range(1, 6)

SRCSET_MAX_SIZE = 8192

# Representation of an image with a width of zero. This value is used
# in validation contexts, i.e. "is the width of the passed or requested
# image greater than or equal to the 'zero width image'."
IMAGE_ZERO_WIDTH = 0

# The minimum width of a default generated image-width.
IMAGE_MIN_WIDTH = 100

# The maximum width of a default generated image-width.
IMAGE_MAX_WIDTH = 8192

# The default dpr qualities used when variable output quality is enabled.
DPR_QUALITIES = {1: 75, 2: 50, 3: 35, 4: 23, 5: 20}


SRCSET_TARGET_WIDTHS = [
    100, 116, 135, 156, 181, 210, 244, 283,
    328, 380, 441, 512, 594, 689, 799, 927,
    1075, 1247, 1446, 1678, 1946, 2257, 2619,
    3038, 3524, 4087, 4741, 5500, 6380, 7401, 8192]
