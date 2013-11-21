#!/usr/bin/env python
# encoding: utf-8
from processing import update
from flask import Flask
app = Flask(__name__)


@app.route("/content/all")
def deliver_content():
    with open('application/data/content.json', 'r') as f:
        return f.read()


@app.route("/update/order/<type_of>/<storyid>/<taskid>/<direction>")
def update_order(type_of, storyid, taskid, direction):
    updated_json = update(type_of, storyid, taskid, direction)
    return updated_json


if __name__ == "__main__":
    app.run()