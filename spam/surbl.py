#!/usr/bin/env python

from urlparse import urlparse
from socket import gethostbyname
from spam import DomainInexistentException
from os.path import join, abspath, dirname

class SurblChecker(object):
    """spam checker using surbl"""
    IS_SPAM = 1
    IS_NOT_SPAM = 2

    def __init__(self, 
                 two_level_file = open(join(abspath(dirname(__file__)) + "/two-level-tlds")),
                 three_level_file = open(join(abspath(dirname(__file__)) + "/three-level-tlds"))):
        self._load_datafiles(two_level_file, three_level_file)
    
    def _load_datafiles(self, two, three):
        self._two_list = list(two.readlines())
        self._three_list = list(three.readlines())

    def _binary_search(self, a, x, lo=0, hi=None):
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo+hi)//2
            midval = a[mid]
            if midval < x:
                lo = mid+1
            elif midval > x: 
                hi = mid
            else:
                return mid
        return -1

    def _query_surbl(self, name):
        try:
            return gethostbyname(name + ".multi.surbl.org")
        except Exception:
            return None

    def _extract_registered_name(self, domain):
        components = domain.split(".")
        name_to_check = None
        if len(components) > 2:
            pos = self._binary_search(self._three_list, components[-3] + "." + components[-2] + "." + components[-1] + "\n")
            if pos != -1 and len(components) > 3:
                name_to_check = components[-4] + "." + components[-3] + "." + components[-2] + "." + components[-1]
        if not name_to_check:
            pos = self._binary_search(self._two_list, components[-2] + "." + components[-1] + "\n")
            if pos != -1 and len(components) > 2:
                name_to_check = components[-3] + "." + components[-2] + "." + components[-1]
            else:
                name_to_check = components[-2] + "." + components[-1]
        return name_to_check

    def _decode_surbl(self, surbl_result):
        """decode surbl ip codes"""
        if surbl_result:
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
        
        name_to_check = self._extract_registered_name(domain)
        surbl_result = self._query_surbl(name_to_check)
        return self._decode_surbl(surbl_result)

    def is_spam(self, url):
        """shortcut for check_url == IS_SPAM"""
        return self.check_url(url) == self.IS_SPAM

    def is_not_spam(self, url):
        """shortcut for check_url == IS_NOT_SPAM"""
        return self.check_url(url) == self.IS_NOT_SPAM
