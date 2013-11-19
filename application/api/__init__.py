#!/usr/bin/env python
# encoding: utf-8
from processing import update
from flask import Flask
app = Flask(__name__)


@app.route("/content/all")
def deliver_content():
    with open('application/data/content.json', 'r') as f:
        return f.read()

@app.route("/update/order/<type_of>/<id>/<direction>")
def update_order(type_of, id, direction):
    result = update(type_of, id, direction)
    return result


if __name__ == "__main__":
    app.run()