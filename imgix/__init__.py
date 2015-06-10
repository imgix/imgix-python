import hashlib
import urllib
import urlparse
import zlib
import requests
import json

SHARD_STRATEGY_CRC = "crc"
SHARD_STRATEGY_CYCLE = "cycle"

SIGNATURE_MODE_QUERY = "query"
SIGNATURE_MODE_PATH = "path"  # Unsupported at the moment


class UrlBuilder(object):

    def __init__(self, domains, use_https=False, sign_key=None,
                 sign_mode=SIGNATURE_MODE_QUERY,
                 shard_strategy=SHARD_STRATEGY_CRC):
        if not isinstance(domains, list):
            domains = [domains]
        self._domains = domains
        self._sign_key = sign_key
        self._sign_mode = sign_mode
        self._use_https = use_https
        self._shard_strategy = shard_strategy
        self._shard_next_index = 0

    def create_url(self, path, **parameters):
        if self._shard_strategy == SHARD_STRATEGY_CRC:
            crc = zlib.crc32(path) & 0xffffffff
            index = crc % len(self._domains)  # Deterministically choose domain
            domain = self._domains[index]

        elif self._shard_strategy == SHARD_STRATEGY_CYCLE:
            domain = self._domains[self._shard_next_index]
            self._shard_next_index = (
                self._shard_next_index + 1) % len(self._domains)

        else:
            domain = self._domains[0]

        scheme = "https" if self._use_https else "http"
        url_obj = UrlHelper(domain, path, scheme,
                            sign_key=self._sign_key, sign_mode=self._sign_mode,
                            **parameters)
        return str(url_obj)

    def create_shortened_url_using_bitlyAPI(self, url_obj, key=None):
        bitly = BitlyHelper(url_obj, key)
        shortenedUrl = bitly.create_shortened_url()
        if key != None:
            return shortenedUrl


class UrlHelper(object):

    @classmethod
    def from_url(cls, url):
        pass

    def __init__(self, domain, path, scheme="http",
                 sign_key=None, sign_mode=SIGNATURE_MODE_QUERY, **parameters):
        self._scheme = scheme
        self._host = domain
        self._path = path
        self._sign_key = sign_key
        if sign_mode != SIGNATURE_MODE_QUERY:
            raise Exception("Path signatures are not supported yet.")
        self._sign_mode = sign_mode
        self._parameters = {}
        for key, value in parameters.iteritems():
            self.set_parameter(key, value)

    def set_parameter(self, key, value):
        if not value:
            self.delete_parameter(key)
            return

        self._parameters[key] = value

    def delete_parameter(self, key):
        if key in self._parameters:
            del self._parameters[key]

    def __str__(self):
        query_pairs = []

        for key in sorted(self._parameters.keys()):
            query_pairs.append((str(key), str(self._parameters[key])))

        path = self._path

        if path.startswith("http"):
            path = urllib.quote(self._path, safe="")

        if not path.startswith("/"):
            path = "/" + path  # Fix web proxy style URLs

        query = urllib.urlencode(query_pairs)
        if self._sign_key:
            delim = "" if query == "" else "?"
            signing_value = self._sign_key + path + delim + query
            signature = hashlib.md5(signing_value).hexdigest()

            if query:
                query += "&s=" + signature
            else:
                query = "s=" + signature

        return urlparse.urlunparse([
            self._scheme,
            self._host,
            path,
            "",
            query,
            "",
        ])

class BitlyHelper:
    def __init__(self, url, key):
        self._url = url
        if key == None:
            print "We need yout bitly key to get the shortened url"
        self._key = key

    def create_shortened_url(self):
        if self._key != None:
            API_KEY = self._key
            uri = self._url
            params = {'access_token':API_KEY, 'uri':uri}
            endpoint = 'https://api-ssl.bitly.com/v3/shorten'
            r = requests.get(endpoint, params=params)
            response = json.loads(r.text.decode('utf-8'))
            return response['data']['url']
