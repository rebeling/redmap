#!/usr/bin/env python
# encoding: utf-8
import requests
import logging as log
from app.utils import red


def request_redmine_api(url):
    """
    get data from redmine api
    """
    r = requests.get(url) #, auth=(red.user, red.pw))
    if r.status_code == 200:
        return True, r.json()
    else:
        log.info("error %s, url: %s" % (r.status_code, url))
        return False, "no response, code:  %s" % r.status_code


def get_my_issues():
    url = "%s/issues.xml?assigned_to_id=26&key=%s" % (
        red.url, red.key)
    print url
    return request_redmine_api(url)


def get_project_data():
    url = "%s/projects/%s/issues.json?limit=%s&status_id=*&key=%s" % (
        red.url, red.project, red.limit, red.key)
    print url
    return request_redmine_api(url)


def get_issue_details(an_id):
    url = "%s/issues/%s.json?key=%s" % (red.url, an_id, red.key)
    success, details = request_redmine_api(url)
    if success:
        details = {k: details.get(k, None) for k in ['done_ratio', 'spent_hours']}
    else:
        details = {}
    return success, details

