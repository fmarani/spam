#!/usr/bin/env python

from urlparse import urlparse
from socket import gethostbyname

from spam import DomainInexistentException

class SpamHausChecker(object):
    """spam checker using spamhaus"""
    IS_SPAM = 1
    IS_NOT_SPAM = 2

    def _query_spamhaus(self, spamhaus_zone):
        try:
            return gethostbyname(spamhaus_zone)
        except Exception:
            return None

    def _resolve(self, domain):
        try:
            return gethostbyname(domain)
        except Exception:
            return None

    def _build_spamhaus_zone(self, ip):
        ip_segments = ip.split(".")
        ip_segments.reverse()
        return ".".join(ip_segments) + ".zen.spamhaus.org"

    def _decode_spamhaus(self, spamhaus_result):
        if spamhaus_result:
            return self.IS_SPAM
        else:
            return self.IS_NOT_SPAM

    def check_url(self, url):
        """check an url"""
        domain = urlparse(url).netloc
        return self.check_domain(domain)

    def check_domain(self, domain):
        """check a domain"""
        domain = domain[domain.find('@')+1:] # remove user info
        if domain.count(":") > 0:
            domain = domain[:domain.find(':')] # remove port info
        ip = self._resolve(domain)
        if not ip:
            raise DomainInexistentException
        spamhaus_zone = self._build_spamhaus_zone(ip)
        spamhaus_result = self._query_spamhaus(spamhaus_zone)
        return self._decode_spamhaus(spamhaus_result)

    def is_spam(self, url):
        """shortcut for check_url == IS_SPAM"""
        return self.check_url(url) == self.IS_SPAM

    def is_not_spam(self, url):
        """shortcut for check_url == IS_NOT_SPAM"""
        return self.check_url(url) == self.IS_NOT_SPAM
