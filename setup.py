# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of dingy.
#

from setuptools import find_packages, setup


setup(
    name='dingy',
    version='0.1.0.dev0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==1.1.1',
        'redis==3.3.8'
    ]
)
