#!/usr/bin/env python
# encoding: utf-8
import os
from flask import Flask
from flask import render_template, send_from_directory
from flask import make_response

app = Flask(__name__)

# app.config.from_object('app.settings')
# app.url_map.strict_slashes = False


# frontend routes
# special file handlers and error handlers

@app.route('/')
def index(**kwargs):
    # # files will be cached
    # return send_file('templates/index.html')
    # developement - file will not b cached
    return make_response(open('app/befe/templates/index.html').read())


@app.route('/favicon.ico')
def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                                           'img/favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# api routes

@app.route("/content/all")
def deliver_content():
    with open('app/data/content.json', 'r') as f:
        return f.read()

@app.route("/content/update_from_redmine_data")
def get_redmine_content():
    from app.redmine.get_content import analize_project
    analize_project()
    return 'success:200'

@app.route("/update/order/<type_of>/<storyid>/<taskid>/<direction>")
def update_order(type_of, storyid, taskid, direction):
    from app.befe.processing import update
    updated_json = update(type_of, storyid, taskid, direction)
    return updated_json


if __name__ == "__main__":
    app.run()