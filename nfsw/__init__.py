import os

from flask import Flask

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


    @app.route('/hello')
    def hello():
        return 'Hello World :('


    # register database commands.
    from nfsw import db

    db.init_app(app)


    # register auth blueprint
    from nfsw import auth

    app.register_blueprint(auth.bp)

    return app

