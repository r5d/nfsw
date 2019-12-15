# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of nfsw.
#

from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    ldesc = f.read()


setup(
    name='nfsw',
    version='0.1.1',
    license='ISC',
    author='rsiddharth',
    author_email='s@ricketyspace.net',
    description='A quirky text based adverture',
    long_description=ldesc,
    long_description_content_type='text/markdown',
    url='https://ricketyspace.net/nfsw',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Topic :: Games/Entertainment',
    ],
    platforms='OpenBSD',
    zip_safe=False,
    install_requires=[
        'flask==1.1.1',
        'redis==3.3.8',
        'uwsgi==2.0.18'
    ]
)
