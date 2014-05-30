import hashlib
import urllib
import urlparse
import zlib

SIGNATURE_MODE_QUERY = "query"
SIGNATURE_MODE_PATH = "path" # Unsupported at the moment

class UrlBuilder(object):
	def __init__(self, domains, use_https=False, sign_key=None, sign_mode=SIGNATURE_MODE_QUERY):
		if not isinstance(domains, list):
			domains = [domains]
		self._domains = domains
		self._sign_key = sign_key
		self._sign_mode = sign_mode
		self._use_https = use_https

	def create_url(self, path, **parameters):
		crc = zlib.crc32(path) & 0xffffffff
		index = crc % len(self._domains) # Deterministically choose a domain
		scheme = "https" if self._use_https else "http"
		url_obj = UrlHelper(self._domains[index], path, scheme, sign_key=self._sign_key, sign_mode=self._sign_mode, **parameters) 
		return str(url_obj)
		

class UrlHelper(object):
	@classmethod
	def from_url(cls, url):
		pass

		
	def __init__(self, domain, path, scheme="http", sign_key=None, sign_mode=SIGNATURE_MODE_QUERY, **parameters):
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
		if self._parameters.has_key(key):
			del self._parameters[key]


	def __str__(self):
		query_pairs = []
		for key in sorted(self._parameters.keys()):
			query_pairs.append((str(key), str(self._parameters[key])))

		path = urllib.quote(self._path)
		query = urllib.urlencode(query_pairs)
		if self._sign_key:
			delim = "" if query == "" else "?"
			signature = hashlib.md5(path + delim + query).hexdigest()
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
