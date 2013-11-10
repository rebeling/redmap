#!/usr/bin/env python
# encoding: utf-8
from redreq import get_project_data
import json
from utils import ConfigData, t_


def main(red):
    success, data = get_project_data(red)

    if success:
        # total_count: data['total_count']
        restructure = {}
        print "\n".join(data['issues'][0].keys())
        for issue in data['issues']:
            # Story, Task, Unterst...
            type_of = issue['tracker']['name']

            buffer = restructure.get(type_of, [])
            buffer.append(issue)
            restructure[type_of] = buffer
        print restructure


        # 'Story': [{
        #     'subject':                 # title
        #     'description':             # description
        #     'created_on':              #
        #     'author':                  #
        #     'assigned_to.name':        #
        #     'fixed_version.name':      # Backlog, ...
        #     'due_date':                # to be ready
        #      ...
        # },
        # ]

        # 'Task' = {
        #     'storyId': {
        #         'taskId': {
        #             'subject':                 # title
        #             'description':             # description
        #             'created_on':              #
        #             'author':                  #
        #             'assigned_to.name':        #
        #             'fixed_version.name':      # Backlog, ...
        #             'due_date':                # to be ready
        #             ...
        #             'estimation':
        #             'realtime':
        #             'status':
        #             'blocked_by': [taskId]
        #


        new_items = {}
        for key, items in restructure.iteritems():
            print key.encode('utf-8')
            # print items

            if key == "Story":
                new_items[key] = []
                for item in items:
                    new_items[key].append(reworked_item(key, item))

            elif key == "Task":
                alltasks = {}
                for item in items:
                    parentid = item['parent']['id']
                    tasks = alltasks.get(parentid, [])
                    tasks.append(reworked_item(key, item))
                    alltasks[parentid] = tasks
                new_items[key] = alltasks

            elif key == "Unterstützung":
                print "todo!"


        print json.dumps(new_items, indent=4, sort_keys=True)

    else:
        print data



def reworked_item(type_of, item):

    new_item = {
        'subject': t_(item['subject']),
        'description': t_(item['subject']),
        'created_on': item['created_on'],
        'author': t_(item['author']['name']),
        'assigned_to': t_(item['assigned_to']['name']),
        'fixed_version': t_(item['fixed_version']['name']).lower(),
        'start_date': item['start_date'],
        'status': t_(item['status']['name']),
        # 'updated_on': item['updated_on'],
        # 'done_ratio': item['done_ratio']
        # 'due_date': item['due_date'],
    }

    # if type_of is "Story":
    # elif type_of is "Task":

    return new_item





if __name__ == '__main__':
    main(ConfigData())

