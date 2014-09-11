"""Unit tests for the python imgix library"""
# pylint: disable=C0111,W0312, R0904, C0301
import unittest
import imgix
from urlparse import urlparse

def get_host_from_url(url):
	dummy = urlparse(url)
	return dummy.netloc


class UrlBuilderTests(unittest.TestCase):

	def test_basic_usage(self):
		builder = imgix.UrlBuilder("demos.imgix.net")
		url = builder.create_url("/bridge.png", w=100, h=100)
		self.assertEquals(url, "http://demos.imgix.net/bridge.png?h=100&w=100")

	def test_basic_usage_with_https(self):
		builder = imgix.UrlBuilder("demos.imgix.net", use_https=True)
		url = builder.create_url("/bridge.png", w=100, h=100)
		self.assertEquals(url, "https://demos.imgix.net/bridge.png?h=100&w=100")

	def test_basic_usage_with_signing(self):
		builder = imgix.UrlBuilder("demos.imgix.net", sign_key="test1234")
		url = builder.create_url("/bridge.png", w=100, h=100)
		expected = "http://demos.imgix.net/bridge.png?h=100&w=100&s=bb8f3a2ab832e35997456823272103a4"
		self.assertEquals(url, expected)

	def test_basic_usage_with_shard_crc(self):
		domains = ["demos-1.imgix.net", "demos-2.imgix.net", "demos-3.imgix.net"]
		builder = imgix.UrlBuilder(domains)

		img1_domain = get_host_from_url(builder.create_url("/bridge.png", w=100, h=100))
		img2_domain = get_host_from_url(builder.create_url("/flower.png", w=100, h=100))

		for dummy in range(0, 20):
			img1_domain_test = get_host_from_url(builder.create_url("/bridge.png", w=100, h=100))
			img2_domain_test = get_host_from_url(builder.create_url("/flower.png", w=100, h=100))
			self.assertEquals(img1_domain, img1_domain_test)
			self.assertEquals(img2_domain, img2_domain_test)

	def test_basic_usage_with_shard_cycle(self):
		domains = ["demos-1.imgix.net", "demos-2.imgix.net", "demos-3.imgix.net"]
		builder = imgix.UrlBuilder(domains, shard_strategy=imgix.SHARD_STRATEGY_CYCLE)

		used = []

		for dummy in domains:
			url = builder.create_url("/bridge.png", w=100, h=100)
			cur_domain = get_host_from_url(url)
			self.assertFalse(cur_domain in used)
			used.append(cur_domain)





