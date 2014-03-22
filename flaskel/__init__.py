#-*- coding: utf-8 -*-

import os
import logging.config

from flask import Flask

__version__ = "0.1"

CONFIG_PATHS = ("/path/to/settings.py",
                "flaskel/settings.py",
                "settings.py",)

app = Flask(__name__)


def config():
    class DefaultConfig(object):
        DEBUG = True

    for path in CONFIG_PATHS:
        if os.path.exists(path):
            config = DefaultConfig()
            config.__file__ = os.path.join(os.getcwd(), path)
            execfile(path, config.__dict__)
            return config
    else:
        raise Exception("No settings file found")


def _before_request():
    pass


def _teardown_request(e):
    pass


def create_app():
    global app

    # app config
    app.config.from_object(config())

    # before/after request
    app.before_request(_before_request)
    app.teardown_request(_teardown_request)

    # logging config
    logging_config = os.environ.get("LOGGING_CONFIG",
                                    app.config.get("LOGGING_CONFIG"))
    if logging_config:
        logging.config.fileConfig(logging_config)

    # blueprints
    import api.test
    app.register_blueprint(api.test.bp_test)

    return app
