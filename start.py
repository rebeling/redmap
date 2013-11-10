#!/usr/bin/env python
# encoding: utf-8
from utils.config_parser import ConfigData
from redmine.redreq import get_project_data
from utils.transformator import restructure_data
import json


def main():
    """
        1. get/set all your connection data for redmine
        2. connect to your project and get the projects issues.json
        3. restructure the data in transformator
        todo:
        4. store data somehow ...pouchdb or redis would be awesome!
    """
    red = ConfigData()

    success, data_or_msg = get_project_data(red)

    if success:
        restructured = restructure_data(data_or_msg)
        final_data = json.dumps(restructured, indent=4, sort_keys=True)
        with open("data/%s_data.json" % red.project, 'w') as f:
            f.write(final_data)

    else:
        print data_or_msg


if __name__ == '__main__':
    main()
