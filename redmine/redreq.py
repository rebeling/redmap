#!/usr/bin/env python
# encoding: utf-8
import requests
# import logging as log


def get_project_data(red):
    """ would be nice to use pyredmine, but it actually can not find
        the project on server I am looking for ...requests does
    """
    # ?pyredmine - https://pypi.python.org/pypi/pyredmine/0.2.1
    # from redmine import Redmine
    # server = Redmine(red.redmine_url, key=red.key)
    # print server.projects[red.project]
    url = "%s/projects/%s/issues.json" % (red.redmine_url, red.project)
    r = requests.get(url, auth=(red.user, red.pw))
    if r.status_code == 200:
        return True, r.json()
    else:
        return False, "no response, code:  %s" % r.status_code
