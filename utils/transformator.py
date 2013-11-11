#!/usr/bin/env python
# encoding: utf-8
from utils.translator import t_
# import logging as log


def restructure_data(data):

    # total_count: data['total_count']
    restructure = {}
    # print "\n".join(data['issues'][0].keys())
    for issue in data['issues']:
        # Story, Task, Unterst...
        type_of = issue['tracker']['name']
        buffer = restructure.get(type_of, [])
        buffer.append(issue)
        restructure[type_of] = buffer



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
        # print key.encode('utf-8')
        # print items

        if key.encode('utf-8')  == "Story":
            new_items[key] = []
            for item in items:
                new_items[key].append(restructure_item(key, item))

            # in order to sort the stories and put the backlogs at the end
            # we prefix 'sprint ' to 'backlog' and remove it after the sorting
            stories = new_items[key]
            for story in stories:
                if 'backlog' in story['fixed_version']:
                    story['fixed_version'] = 'sprint ' + story['fixed_version']
            stories = sorted(stories, key=lambda k: k['fixed_version'])
            for story in stories:
                if 'backlog' in story['fixed_version']:
                    story['fixed_version'] = story['fixed_version'][7:]

            new_items[key] = stories


        elif key.encode('utf-8')  == "Task":
            alltasks = {}
            for item in items:
                parentid = item['parent']['id']
                tasks = alltasks.get(parentid, [])
                tasks.append(restructure_item(key, item, parentid=parentid))
                alltasks[parentid] = tasks
            new_items[key] = alltasks

        elif key.encode('utf-8')  == "Unterstützung":
            new_items[key] = []
            for item in items:
                new_items[key].append(restructure_item(key, item))

    return new_items






def restructure_item(type_of, item, parentid=None):

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

    if type_of.encode('utf-8') == "Story":
        # print item
        pass

    elif type_of.encode('utf-8') == "Task":
        if parentid:
            new_item['parent'] = parentid

    elif type_of.encode('utf-8') == "Unterstützung":
        # print item
        pass

    return new_item

