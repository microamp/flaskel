# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

import flaskel
from flaskel.lib import test as lib_test


bp_test = Blueprint("test", __name__)


@bp_test.route("/")
def index():
    return jsonify(**{
        k: str(v) if not isinstance(v, str) else v
        for k, v in flaskel.app.config.iteritems()
    })


@bp_test.route("/add/<int:a>/<int:b>")
def add(a, b):
    return "{a} + {b} = {x}".format(a=a, b=b, x=lib_test.add(a=a, b=b))


@bp_test.route("/add2")
def add2():
    return "{a} + {b} = {x}".format(
        a=request.args["a"],
        b=request.args["b"],
        x=lib_test.add(a=int(request.args["a"]), b=int(request.args["b"])),
    )
