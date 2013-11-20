#!/usr/bin/env python
# encoding: utf-8
from application.redmine import red_t_
from application.utils import order_by_position
import logging as log
import json


def organize_issues_by_type(data):
    restructure = {}
    for issue in data['issues']:
        # translate type Story, Task, Unterst...
        # and create a dict of all with a list of its issues
        type_of = red_t_(issue['tracker']['name'].encode('utf-8').lower())
        buffer = restructure.get(type_of, [])
        buffer.append(issue)
        restructure[type_of] = buffer
    return restructure


def process(item, alltasks, key, no_parent):
    if 'parent' in item:
        parentid = item['parent']['id']
        tasks = alltasks.get(parentid, [])
        tasks.append(restructure_item("task", item, parentid=parentid))
        alltasks[parentid] = tasks
    else:
        no_parent[key] = True
        tasks_without_parent = alltasks.get('no_parent_%s' % key, [])
        tasks_without_parent.append(restructure_item("task", item))
        alltasks['no_parent_%s' % key] = tasks_without_parent
    return alltasks, no_parent


def extend_thetasks(alltasks, processed_items):
    thetasks = processed_items.get("task", {})
    for k,v in alltasks.iteritems():
        if k in thetasks:
            for x in v:
                thetasks[k].append(x)
        else:
            thetasks[k] = v
    return thetasks


def restructure_data(data, project, project_url):
    """
        input is a json structure of the complete project
        so is the output, but restructured
        1. organize issues by type
        2. process for every type the issues list
        3. ..
    """
    processed_items = {
        'story': [],
        'task': {},
        'info': {
            'total_count': data['total_count'],
            'project': project,
            'project_url': project_url
        }
    }

    restructure = organize_issues_by_type(data)

    no_parent = {
        "task": False,
        "package": False,
        "support": False,
        "bug": False,
        "feature": False
    }

    for key, items in restructure.iteritems():

        if key == "story":
            for i, item in enumerate(items):
                newone = restructure_item(key, item, position=i)
                if newone:
                    processed_items[key].append(newone)

        elif key == "support" or key == "task":

            buffer = {}
            for item in items:
                buffer, no_parent = process(item, buffer, key, no_parent)
            processed_items["task"] = extend_thetasks(buffer, processed_items)

        elif key == "bug" or key == "feature":

            buffer = {}
            for item in items:

                if 'parent' in item:
                    print 'yes, parent in item. take care'
                    pass
                else:
                    no_parent[key] = True
                    buffer, no_parent = process(item, buffer, key, no_parent)

            processed_items["task"] = extend_thetasks(buffer, processed_items)



        else:
            log.info("another key: %s" % key)


    # # at the end append a story dummy for every rubbish at least to show
    # # identify false positives in the project
    dummies = {
        'support': {'id': 'no_parent_support',
                    'subject': 'All support without a story'},
        'bug': {    'id': 'no_parent_bug',
                    'subject': 'All bugs without a story'},
        'task': {   'id': 'no_parent_task',
                    'subject': 'All tasks without a story'},
        'feature': {'id': 'no_parent_task',
                    'subject': 'All tasks without a story'}
    }

    dummy_pos = len(processed_items['story'])
    for key, value in no_parent.iteritems():
        if value:
            dummy_pos += 1
            buffer = add_a_dummy_story(dummies, key, position=dummy_pos)
            processed_items['story'].append(buffer)


    for key in processed_items['story']:
        try:
            for i,task in enumerate(processed_items['task'][key['id']]):
                task['position'] = i
        except:
            pass

    try:
        with open('application/data/content.json', 'r') as f:
            old_processed_items = json.loads(f.read())

            # update by old content
            for item in old_processed_items['story']:
                for new_item in processed_items['story']:
                    if item['id'] == new_item['id']:
                        new_item['position'] = item['position']
                        new_item['sprint'] = item['sprint']
    except:
        pass

    # order at the end
    processed_items['story'] = order_by_position(processed_items['story'])

    for key in processed_items['story']:
        try:
            processed_items['task'][key['id']] = order_by_position(processed_items['task'][key['id']])
        except:
            pass

    return processed_items



def add_a_dummy_story(dummies, key, position=0):
    no_parent_dummy = {
        'id': dummies[key]['id'],
        'subject': dummies[key]['subject'],
        'description': '',
        'created_on': '',
        'author': {'name': 'AutoGenerated'},
        'assigned_to': {'name': ''},
        'status': {'name': 'unknown'},
    }
    return restructure_item('story', no_parent_dummy, position=position)


def restructure_item(type_of, item, parentid=None, position=0):

    new_item = {
        'id': item['id'],
        'subject': red_t_(item['subject'].encode('utf-8')),
        'description': red_t_(item['description'].encode('utf-8')),
        'created_on': item['created_on'],
        'author': red_t_(item['author']['name'].encode('utf-8')),
        'status': red_t_(item['status']['name'].lower().encode('utf-8')),
        'type': type_of,
        'position': position,
        'sprint': 'initial'
    }

    for x in ['fixed_version', 'assigned_to']:
        try:
            new_item[x] = red_t_(item[x]['name'].lower().encode('utf-8'))
        except:
            log.info("no such field %s" % x)

    for field in ['start_date', 'estimated_hours']:
        try:
            new_item[field] = item[field]
        except:
            log.info("no such field %s" % field)

    return new_item
