#!/usr/bin/env python
# encoding: utf-8
import requests
import logging as log
from application.utils import red


def request_redmine_api(url):
    """
        would be nice to use pyredmine, but it actually can not find
        the project on server I am looking for ...requests does

    """
    # ?pyredmine - https://pypi.python.org/pypi/pyredmine/0.2.1
    # from redmine import Redmine
    # server = Redmine(red.redmine_url, key=red.key)
    r = requests.get(url, auth=(red.user, red.pw))
    if r.status_code == 200:
        log.info("success, url: %s" % url)
        return True, r.json()
    else:
        log.info("error %s, url: %s" % (r.status_code, url))
        return False, "no response, code:  %s" % r.status_code


def get_project_data():
    url = "%s/projects/%s/issues.json?limit=%s&status_id=*" % (
        red.url, red.project, red.limit)
    return request_redmine_api(url)


def get_issue_details(an_id):
    url = "%s/issues/%s.json" % (red.url, an_id)
    return request_redmine_api(url)
