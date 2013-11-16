#!/usr/bin/env python
# encoding: utf-8
import requests
import logging as log


def get_project_data(red):
    """ would be nice to use pyredmine, but it actually can not find
        the project on server I am looking for ...requests does
    """
    # ?pyredmine - https://pypi.python.org/pypi/pyredmine/0.2.1
    # from redmine import Redmine
    # server = Redmine(red.redmine_url, key=red.key)
    # print server.projects[red.project]
    url = "%s%s/issues.json?limit=%s&status_id=*" % (
        red.url, red.project, red.limit)
    r = requests.get(url, auth=(red.user, red.pw))
    if r.status_code == 200:
        log.info("success, url: %s" % url)
        return True, r.json()
    else:
        log.info("error %s, url: %s" % (r.status_code, url))
        return False, "no response, code:  %s" % r.status_code
