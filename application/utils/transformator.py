#!/usr/bin/env python
# encoding: utf-8
from application.redmine.translation import red_t_
from application.redmine.redreq import get_issue_details
from application.utils import order_by_key
import logging as log
import json
from application.utils import red


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

    # create no_parent for all the orphans
    no_parent = {x: False
        for x in ['task', 'package', 'support', 'bug', 'feature']}

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


    processed_items = story_dummies_for_orphans(processed_items, no_parent)

    for key in processed_items['story']:
        # process the tasks again and numerate them
        try:
            for i,task in enumerate(processed_items['task'][key['id']]):
                task['position'] = i
        except:
            pass

    processed_items = check_latest(processed_items)
    processed_items = items_order(processed_items)

    return processed_items


def story_dummies_for_orphans(items, no_parent):
    """
        at the end append a story dummy for every rubbish at least to show
        identify false positives in the project

    """
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

    dummy_pos = len(items['story'])
    for key, value in no_parent.iteritems():
        if value:
            dummy_pos += 1
            buffer = add_a_dummy_story(dummies, key, position=dummy_pos)
            items['story'].append(buffer)
    return items


def check_latest(processed_items):
    """
        update the new with the content from latest

    """
    try:
        with open('application/data/content.json', 'r') as f:
            old_processed_items = json.loads(f.read())
            for item in old_processed_items['story']:
                for new_item in processed_items['story']:
                    if item['id'] == new_item['id']:
                        new_item['position'] = item['position']
                        new_item['sprint'] = item['sprint']
    except Exception, e:
        log.debug("failed to update with latest data: %s" % e)

    try:
        with open('application/data/content.json', 'r') as f:
            old_processed_items = json.loads(f.read())
            for key, value in old_processed_items['task'].iteritems():
                for old_item in value:
                    try:
                        key = int(key)
                    except:
                        pass
                    if key in processed_items['task']:
                        for new_item in processed_items['task'][key]:
                            if old_item['id'] == new_item['id']:
                                new_item['position'] = old_item['position']
                                new_item['sprint'] = old_item['sprint']
                    else:
                        log.debug("key not in there %s %s " % (key, type(key)) )
                        for x in processed_items['task'].keys():
                            log.debug("key %s %s" % (x, type(x)))
    except Exception, e:
        log.debug("failed to update with latest data: %s" % e)




    return processed_items


def items_order(items):
    """
        order the items by position. easy for stories, but loopy for tasks

    """
    items['story'] = order_by_key(items['story'], 'position')

    for key, to_be_ordered in items['task'].iteritems():
        log.debug("order for %s" % key)
        try:
            items['task'][key] = order_by_key(to_be_ordered, 'position')
        except Exception, e:
            log.error('not able to order the items %s' % e)

    return items




















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
    return restructure_item('story', no_parent_dummy, position=position, dummy=1)


def restructure_item(type_of, item, parentid=None, position=0, dummy=None):

    # get more details
    done_ratio = 0
    spent_hours = 0
    if dummy == None:
        success, data = get_issue_details(item['id'], red)
        if success:
            done_ratio = data['issue'].get('done_ratio', 0)
            spent_hours = data['issue'].get('spent_hours', 0)
        else:
            log.debug("get issue error: %s" % data)


    # init the new item
    new_item = {
        'id': item['id'],
        'subject': red_t_(item['subject'].encode('utf-8')),
        'description': red_t_(item['description'].encode('utf-8')),
        'created_on': item['created_on'],
        'author': red_t_(item['author']['name'].encode('utf-8')),
        'status': red_t_(item['status']['name'].lower().encode('utf-8')),
        'type': type_of,
        'position': position,
        'sprint': 'initial',
        'done_ratio': done_ratio,
        'spent_hours': spent_hours
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











def estimation_and_progress(tasks):

    estimations = {
        't_total': 0,
        't_real': 0,
        't_over': 0,
        'c_done': 0,
        'c_inprogress': 0,
        'c_total': 0
    }

    for key, value in tasks:

        estimations['t_total'] += value['est']
        estimations['c_total'] += 1

        if value['status'] == 'done':
            estimations['c_done'] += 1
            estimations['t_real'] += value['real']
            x = value['est'] - value['real']
            if x < 0:
                estimations['t_over'] += x * -1

        if value['status'] == 'inprogress':
            estimations['c_inprogress'] += 1
            estimations['t_real'] += value['real']

    return estimations





def calculate_progress(estimated, realworked, status):
        if status == 'done' or realworked >= estimated:
            return 100
        elif realworked < estimated:
            return (realworked * 100)/estimated
        else:
            return 0

def check_blocking(blockedby):
    if len(blockedby) > 0:
        return True
    else:
        return False


# storyObj = (story, related_tasks) ->

#     task_ids = []
#     if related_tasks
#         for i,task in related_tasks
#             task_ids.push task.id

#     the_story = angular.copy(story)

#     the_story['tasks'] = related_tasks
#     the_story['task_ids'] = task_ids
#     the_story['estimations'] = estimation_and_progress(related_tasks)

#     the_story
























