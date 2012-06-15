SPAM - URL spam testing library 
===============================

.. image:: https://secure.travis-ci.org/fmarani/spam.png

A library to verify whether an url has been classified as spam

Supports:

* SpamHaus zen 
  * SBL (e-mail spam)
  * XBL (infected PCs)
  * PBL (unsolicited smtp traffic)
* Surbl multi
  * Spamcop
  * sa-blacklist
  * Outblaze
  * Abusebutler
  * Phishtank
  * Zeus tracker
  * jwSpamSpy
  * Prolocation

For any further information, you can watch the tutorial here:
http://www.youtube.com/watch?v=anwy2MPT5RE

Install
-------

From PyPI (stable)::

    pip install spam-blocklists

From Github (unstable)::

    pip install git+git://github.com/fmarani/spam.git#egg=spam-blocklists

Use
---

Spamhaus::

    >>> from spam.spamhaus import SpamHausChecker
    >>> checker = SpamHausChecker()

    # google.com is a good domain
    >>> checker.is_spam("http://www.google.com/search?q=food")
    False

    # this domain does not exist
    >>> checker.is_spam("http://buyv1agra.com/")
    Traceback (most recent call last):
        ...
    DomainInexistentException

    # this is a scam
    >>> checker.is_spam("http://mihouyuan.com/login.htm")
    True

Surbl::

    >>> from spam.surbl import SurblChecker
    >>> checker = SurblChecker()

    # google.com test
    >>> checker.is_spam("http://www.google.com/search?q=food")
    False

    # spamhaus says it is spam, surbl does not
    >>> checker.is_spam("http://mihouyuan.com/login.htm")
    False

    # test endpoint for surbl
    >>> checker.is_spam("http://surbl-org-permanent-test-point.com/")
    True

Contribute
----------

Clone and install testing dependencies::

    pip install -r requirements.txt

Ensure tests pass::

    ./runtests.sh

