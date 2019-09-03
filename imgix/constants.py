import re

DOMAIN_PATTERN = re.compile(
            r'^(?:[a-z\d\-_]{1,62}\.){0,125}'
            r'(?:[a-z\d](?:\-(?=\-*[a-z\d])|[a-z]|\d){0,62}\.)'
            r'[a-z\d]{1,63}$'
        )
SRCSET_INCREMENT_PERCENTAGE = 8
SRCSET_MAX_SIZE = 8192


def _target_widths():
    resolutions = []
    prev = 100

    def ensure_even(n):
        return 2 * round(n/2.0)

    while prev <= SRCSET_MAX_SIZE:
        resolutions.append(int(ensure_even(prev)))
        prev *= 1 + (SRCSET_INCREMENT_PERCENTAGE / 100.0) * 2

    resolutions.append(SRCSET_MAX_SIZE)
    return resolutions


SRCSET_TARGET_WIDTHS = _target_widths()
