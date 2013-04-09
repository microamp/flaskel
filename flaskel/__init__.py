# -*- coding: utf-8 -*-

import os
import logging.config

from flask import Flask


class DefaultConfig(object):
    DEBUG = True
    SCRIPT_NAME = "/flaskel"


def from_pyfile(config_file):
    config = DefaultConfig()
    config.__file__ = os.path.join(os.getcwd(), config_file)
    try:
        execfile(config_file, config.__dict__)
    except IOError as e:
        raise e
    return config


def _before_request():
    pass


def _teardown_request(exception):
    pass


# flask app
app = Flask(__name__)

# app config
config_file = os.environ.get("CONFIG", "flaskel/settings.py")
config = from_pyfile(config_file=config_file)
app.config.from_object(config)

# before/after request
app.before_request(_before_request)
app.teardown_request(_teardown_request)

# logging config
logging_config = os.environ.get(
    "LOGGING_CONFIG",
    app.config.get("LOGGING_CONFIG")
)
if logging_config:
    logging.config.fileConfig(logging_config)

# blueprints
import views.test
app.register_blueprint(views.test.bp_test)
