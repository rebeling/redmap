#!/usr/bin/env python
# encoding: utf-8
from application.redmine.red_translation import red_t_
from application.redmine.red_requests import get_issue_details
from application.redmine.red_item import create_item # Story, Task
from application.utils import order_by_key
import logging as log
import json
from application.utils import timing
import time


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


@timing
def restructure_data(data, project, project_url):
    """
    input is a json structure of the complete project
    so is the output, but restructured
    1. organize issues by type
    2. process for every type the issues list
    3. ..

    """
    t1 = time.time()

    print "» %.2f sec" % (time.time() - t1)

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

    # get data from last time to update position and status
    updater = {}
    try:
        with open('application/data/content.json', 'r') as f:
            buffer = json.loads(f.read())
            updater['story'] = {
                x['id']:{'postion': x['position'], 'status': x['status']}
                for x in buffer['story']}

            updater['task'] = {}
            for key, tasks in buffer['task'].iteritems():
                updater['task'][key] = {
                    x['id']:{'postion': x['position'], 'status': x['status']}
                    for x in tasks}

    except Exception, e:
        log.debug("failed to update with latest data: %s" % e)


    print "» %.2f sec" % (time.time() - t1)

    # create no_parent for all the orphans
    no_parent = {x: False
        for x in ['task', 'package', 'support', 'bug', 'feature']}

    print "» %.2f sec" % (time.time() - t1)

    for key, items in restructure.iteritems():

        if key == "story":

            print "story » %.2f sec" % (time.time() - t1)

            for i, item in enumerate(items):

                success, details = get_issue_details(item['id'])
                details['type'] = 'story'
                details['position'] = i + 1
                item.update(details)

                s = create_item(item)
                # s = Story(item)

                if updater and 'story' in updater:
                    # update with data from last time
                    this = updater['story'].get(item['id'], None)
                    if this:
                        s['position'] = this['position']
                        s['status'] = this['status']

                processed_items["story"].append(s)

        elif key == "support" or key == "task":

            print "task » %.2f sec" % (time.time() - t1)

            for item in items:

                success, details = get_issue_details(item['id'])
                details['type'] = 'task'
                item.update(details)

                t = create_item(item)

                parent_id = t['parent']
                if parent_id == None:
                    parent_id = 'no_parent_%s' % key
                    no_parent[key] = True

                no_position_yet = True
                if updater and 'task' in updater:
                    if parent_id in updater['task']:
                        this = updater['task'][parent_id].get(item['id'], None)
                        if this:
                            t['position'] = this['position']
                            t['status'] = this['status']
                            no_position_yet = False

                if no_position_yet:
                    p = len(processed_items["task"].get(parent_id, [])) + 1
                    t['position'] = p

                tasks_4_storyX = processed_items["task"].get(parent_id, [])
                tasks_4_storyX.append(t)
                processed_items["task"][parent_id] = tasks_4_storyX

        else:

            print "» %.2f sec" % (time.time() - t1)

            log.info("another key: %s" % key)

    print "» %.2f sec" % (time.time() - t1)

    processed_items = story_dummies_for_orphans(processed_items, no_parent)

    processed_items = items_order(processed_items)

    return processed_items


@timing
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

    for key, value in no_parent.iteritems():
        if value:
            no_parent_item = {
                'id': dummies[key]['id'],
                'subject': dummies[key]['subject'],
                'status': {'name': 'unknown'},
                'type': 'story'
            }
            s = create_item(no_parent_item)
            items['story'].append(s)

    return items


@timing
def items_order(items):
    """
    order the items by position. easy for stories, but loopy for tasks

    """
    items['story'] = order_by_key(items['story'], 'position')

    # tasks
    for key, to_be_ordered in items['task'].iteritems():
        try:
            items['task'][key] = order_by_key(to_be_ordered, 'position')
        except Exception, e:
            log.error('not able to order the items %s' % e)

    return items
















# def estimation_and_progress(tasks):

#     estimations = {
#         't_total': 0,
#         't_real': 0,
#         't_over': 0,
#         'c_done': 0,
#         'c_inprogress': 0,
#         'c_total': 0
#     }

#     for key, value in tasks:

#         estimations['t_total'] += value['est']
#         estimations['c_total'] += 1

#         if value['status'] == 'done':
#             estimations['c_done'] += 1
#             estimations['t_real'] += value['real']
#             x = value['est'] - value['real']
#             if x < 0:
#                 estimations['t_over'] += x * -1

#         if value['status'] == 'inprogress':
#             estimations['c_inprogress'] += 1
#             estimations['t_real'] += value['real']

#     return estimations





# def calculate_progress(estimated, realworked, status):
#         if status == 'done' or realworked >= estimated:
#             return 100
#         elif realworked < estimated:
#             return (realworked * 100)/estimated
#         else:
#             return 0

# def check_blocking(blockedby):
#     if len(blockedby) > 0:
#         return True
#     else:
#         return False


# # storyObj = (story, related_tasks) ->

# #     task_ids = []
# #     if related_tasks
# #         for i,task in related_tasks
# #             task_ids.push task.id

# #     the_story = angular.copy(story)

# #     the_story['tasks'] = related_tasks
# #     the_story['task_ids'] = task_ids
# #     the_story['estimations'] = estimation_and_progress(related_tasks)

# #     the_story
