import os

from flask import Flask, render_template
from dvr_scan.db import close_db, init_db_command
import dvr_scan.auth
import dvr_scan.monitor

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        template_folder='templates',
        instance_relative_config=True
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'dvr_scan.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template("index.html")


    init_app(app)
    app.register_blueprint(dvr_scan.auth.bp)
    app.register_blueprint(dvr_scan.monitor.bp)
    return app
