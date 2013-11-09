#!/usr/bin/env python
# encoding: utf-8
from redreq import get_project_data
from utils import ConfigData


def main(red):
    success, data = get_project_data(red)

    if success:
        restructure = {'total_count': data['total_count']}
        print "\n".join(data['issues'][0].keys())
        for issue in data['issues']:
            # Story, Task, Unterst...
            type_of = issue['tracker']['name']

            buffer = restructure.get(type_of, [])
            buffer.append(issue)
            restructure[type_of] = buffer
        print restructure

    else:
        print data

if __name__ == '__main__':
    main(ConfigData())

