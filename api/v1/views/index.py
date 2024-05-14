#!/usr/bin/python3
from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def status_code():
    status_code = {
            "status": "OK"
            }
    return jsonify(status_code), 200
