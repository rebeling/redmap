#!/usr/bin/env python
# encoding: utf-8
import json
from application.utils import order_by_key
import logging as log


def access_content(task='r', content=None):

    with open('application/data/content.json', task) as f:

        if task == 'r':
            content = json.loads(f.read())
        elif task == 'w':
            f.write(json.dumps(content, indent=4, sort_keys=True))
        return content


def update(type_of, storyid, taskid, direction):
    content = access_content(task='r')

    if type_of == 'story':
        for item in content['story']:
            try:
                storyid = int(storyid)
            except Exception, e:
                pass
            if item['id'] == storyid:
                # update the order
                # get the actual position and change, then update the neighboor
                old_position = item['position']
                if direction == 'left':
                    newposition = old_position - 1
                else:
                    newposition = old_position + 1
                item['position'] = newposition
                break
        for item in content['story']:
            if item['position'] == newposition and item['id'] != storyid:
                item['position'] = old_position

        content['story'] = order_by_key(content['story'], 'position')
        access_content(task='w', content=content)

    else:
        for item in content['task'][storyid]:
            if item['id'] == int(taskid):
                # update the order
                # get the actual position and change, then update the neighboor to
                old_position = item['position']
                if direction == 'up':
                    newposition = old_position - 1
                else:
                    newposition = old_position + 1
                item['position'] = newposition
                break

        for item in content['task'][storyid]:
            if item['position'] == newposition and item['id'] != int(taskid):
                item['position'] = old_position

        content['task'][storyid] = order_by_key(content['task'][storyid], 'position')
        access_content(task='w', content=content)

    return json.dumps(content)
