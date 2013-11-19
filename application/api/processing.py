#!/usr/bin/env python
# encoding: utf-8
import json
from application.utils import order_by_position
import logging as log


def access_content(task='r', content=None):

    with open('application/data/content.json', task) as f:

        if task == 'r':
            content = json.loads(f.read())
        elif task == 'w':
            f.write(json.dumps(content, indent=4, sort_keys=True))
        return content


def update(type_of, the_id, direction):
    content = access_content(task='r')

    log.debug('hello')

    # return "%s %s %s" % (type_of, the_id, direction)
    # return str(type(the_id))

    if type_of == 'story':
        for item in content['story']:
            if item['id'] == int(the_id):
                # update the order
                # get the actual position and change, then update the neighboor to
                old_position = item['position']
                if direction == 'left':
                    newposition = old_position - 1
                else:
                    newposition = old_position + 1
                item['position'] = newposition
                break
        for item in content['story']:
            if item['position'] == newposition and item['id'] != int(the_id):
                item['position'] = old_position

    content['story'] = order_by_position(content['story'])
    access_content(task='w', content=content)

    return "Done."
