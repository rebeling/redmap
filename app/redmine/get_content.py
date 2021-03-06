#!/usr/bin/env python
# encoding: utf-8
from app.redmine.red_requests import get_project_data
from app.redmine.transformer import restructure_data
from app.utils import write_content_to
from app.utils import timing
from app.utils import red
import json
import logging as log


@timing
def analize_project():
    """
        1. get/set all your connection data for redmine
        2. connect to your project and get the projects issues.json
        3. restructure the data in transformator
        4. save data as json
            todo:
            store data somehow ...pouchdb or redis would be awesome!
    """
    log.info('started')

    from app.redmine.red_requests import get_my_issues
    print get_my_issues()

    success, data_or_msg = get_project_data()
    if success:
        restructured = restructure_data(data_or_msg, red.project,
                                        '%s' % red.url + red.project)
        final_data = json.dumps(restructured, indent=4, sort_keys=True)
        write_content_to('app/data/content.json', final_data)
    else:
        log.info("failed %s" % data_or_msg)

    log.info('finished')
