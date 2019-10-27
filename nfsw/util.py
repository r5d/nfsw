# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of dingy.
#

import os

from flask import current_app

def read_junk(key):
    r = os.path.join('junk', key)

    with current_app.open_resource(r) as f:
        return f.read().decode()
