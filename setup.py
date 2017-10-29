#!/usr/bin/env python

'''This file controls the packaging and deployment of the time_intervals module.

Jon Nation
August 2017
'''

from setuptools import setup, find_packages

setup(
    name = 'time_intervals',
    version = '1.0',
    description = 'Operations on intervals',
    author = 'Sotiria Lampoudi',
    author_email = 'slampoud@gmail.com',
    packages = ['time_intervals'],
    package_data = {
        '': ['*.conf'],
    },
    tests_require = [
        "nose",
    ],
    test_suite = 'nose.collector',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ]

)
