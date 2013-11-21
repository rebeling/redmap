#!/usr/bin/env python
# encoding: utf-8
from application.redmine.redreq import get_project_data
from application.utils.transformator import restructure_data
from application.utils import write_content_to
import json
import logging as log


def process_project(red):
    """
        1. get/set all your connection data for redmine
        2. connect to your project and get the projects issues.json
        3. restructure the data in transformator
        4. save data as json
            todo:
            store data somehow ...pouchdb or redis would be awesome!
    """
    log.info('started')

    success, data_or_msg = get_project_data()
    if success:
        restructured = restructure_data(data_or_msg, red.project,
                                        '%s' % red.url + red.project)
        final_data = json.dumps(restructured, indent=4, sort_keys=True)
        write_content_to('application/data/content.json', final_data)
    else:
        log.info("failed %s" % data_or_msg)

    log.info('finished')
