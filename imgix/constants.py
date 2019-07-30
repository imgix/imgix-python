import re

DOMAIN_PATTERN = re.compile(
            r'^(?:[a-z\d\-_]{1,62}\.){0,125}'
            r'(?:[a-z\d](?:\-(?=\-*[a-z\d])|[a-z]|\d){0,62}\.)'
            r'[a-z\d]{1,63}$'
        )


def target_widths():
    resolutions = []
    prev = 100
    INCREMENT_PERCENTAGE = 8
    MAX_SIZE = 8192

    def ensureEven(n):
        return 2 * round(n/2)

    while prev <= MAX_SIZE:
        resolutions.append(ensureEven(prev))
        prev *= 1 + (INCREMENT_PERCENTAGE / 100) * 2

    resolutions.append(MAX_SIZE)
    return resolutions
