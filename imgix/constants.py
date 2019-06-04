import re

DOMAIN_PATTERN = re.compile(
            r'^(?:[a-z\d\-_]{1,62}\.){0,125}'
            r'(?:[a-z\d](?:\-(?=\-*[a-z\d])|[a-z]|\d){0,62}\.)'
            r'[a-z\d]{1,63}$'
        )
