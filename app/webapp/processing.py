#!/usr/bin/env python
# encoding: utf-8
import json
from app.utils import order_by_key
import logging as log


def access_content(task='r', content=None):

    with open('app/data/content.json', task) as f:

        if task == 'r':
            content = json.loads(f.read())
        elif task == 'w':
            f.write(json.dumps(content, indent=4, sort_keys=True))
        return content


def update(type_of, storyid, taskid, direction):
    """
    update the order
    get the actual position and change, then update the neighboor

    """
    content = access_content(task='r')

    if type_of == 'story':
        for item in content['story']:

            if item['id'] == storyid:
                log.debug("change position for id %s" % taskid)
                old_position = item['position']
                if direction == 'left':
                    newposition = old_position - 1
                else:
                    newposition = old_position + 1
                item['position'] = newposition
                log.debug("update positions - old: %s new: %s" % (old_position, newposition))
                break

        for item in content['story']:
            if item['position'] == newposition and item['id'] != storyid:
                item['position'] = old_position

        content['story'] = order_by_key(content['story'], 'position')
        access_content(task='w', content=content)

    else:

        for item in content['task'][storyid]:
            if item['id'] == taskid:
                log.debug("change position for id %s" % taskid)

                old_position = item['position']
                if direction == 'up':
                    newposition = old_position - 1
                else:
                    newposition = old_position + 1
                item['position'] = newposition
                log.debug("update positions - old: %s new: %s" % (old_position, newposition))
                break

        for item in content['task'][storyid]:
            if item['position'] == newposition and item['id'] != taskid:
                log.debug("also update position for id %s" % item['id'])
                item['position'] = old_position

        content['task'][storyid] = order_by_key(content['task'][storyid], 'position')
        access_content(task='w', content=content)

    return json.dumps(content)





def update_sprint(storyid, taskid, sprint, type_of):
    """
    update the target sprint for this task
    if storyid is not None update the story for the sprint

    """
    content = access_content(task='r')

    if type_of == 'story':
        for item in content['story']:
            if item['id'] == storyid:
                log.debug("change sprint target for id %s" % storyid)
                item['sprint'] = sprint
                break
    else:
        for item in content['task'][storyid]:
            if item['id'] == taskid:
                log.debug("change sprint target for id %s" % taskid)
                item['sprint'] = sprint
                break

    access_content(task='w', content=content)
    return json.dumps(content)
