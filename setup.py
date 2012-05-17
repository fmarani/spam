#!/usr/bin/env python

from setuptools import setup

setup(name='spam-blocklists',
        version='0.9',
        url='https://github.com/fmarani/spam',
        description="Spam related services interface",
        long_description=open('README.rst').read(),
        author="Federico Marani",
        author_email="flagzeta@gmail.com",
        packages=['spam'],
        requires=[],    
        classifiers = [
            "Intended Audience :: Developers",
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries',
            ]
        )
