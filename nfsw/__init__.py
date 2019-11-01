# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of nfsw.
#

import os

from flask import Flask, render_template

def create_app(test_config=None):
    # create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'nfsw.sqlite')
    )

    if test_config is None:
        # load instance's config if it exists.
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_object(test_config)


    try:
        os.makedirs(app.instance_path)
    except:
        pass


    # register database commands.
    from nfsw import db

    db.init_app(app)


    # register auth blueprint
    from nfsw import auth

    app.register_blueprint(auth.bp)

    # register io blueprint
    from nfsw import io

    app.register_blueprint(io.bp)
    app.add_url_rule('/io', endpoint='io')

    # register epilogue blueprint
    from nfsw import epilogue

    app.register_blueprint(epilogue.bp)
    app.add_url_rule('/epilogue', endpoint='epilogue')

    @app.route('/', endpoint='index')
    @auth.anon_only
    def nfsw():
        return render_template('nfsw.html')


    return app

