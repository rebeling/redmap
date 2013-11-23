#!/usr/bin/env python
# encoding: utf-8

# import unittest
from application.redmine.red_translation import red_t_
import logging as log


def create_item(arg):

    # 'created_on',
    keys = ['id', 'type', 'subject', 'description', 'author', 'status',
            'position', 'sprint', 'fixed_version', 'assigned_to',
            'estimated_hours', 'parent']

    item = {}
    for k in keys:
        v = arg.get(k, None)
        if v:
            if type(v) is dict:
                if k == 'parent':
                    v = v.get('id', None)
                else:
                    v = v.get('name', None)
        try:
            if v and k in ['status']:
                v = str(red_t_(v.encode('utf-8').lower()))
            if v and k in ['id', 'parent']:
                v = str(v)
        except Exception, e:
            log.debug("e %s" % e)
        item[k] = v

    return item



# class Base(object):
#     """
#     StoryAndTask super class
#     """
#     __slots__ = ('item')
#     def __init__(self, arg, details=None):

#         # 'created_on',
#         keys = ['id', 'type', 'subject', 'description', 'author', 'status',
#                 'position', 'sprint', 'fixed_version', 'assigned_to',
#                 'estimated_hours', 'parent']

#         item = {}
#         for k in keys:
#             v = arg.get(k, None)
#             if v:
#                 if type(v) is dict:
#                     if k == 'parent':
#                         v = v.get('id', None)
#                     else:
#                         v = v.get('name', None)
#             try:
#                 if v and k in ['status']:
#                     v = str(red_t_(v.encode('utf-8').lower()))
#                 if v and k in ['id', 'parent']:
#                     v = str(v)
#             except Exception, e:
#                 log.debug("e %s" % e)
#             item[k] = v

#         # self.__dict__.update(item)
#         self.item = item


# class Story(Base):
#     def __init__(self, arg):
#         super(Story, self).__init__(arg)


# class Task(Base):
#     def __init__(self, arg):
#         super(Task, self).__init__(arg)
#         # self.__dict__.update(arg)


# class Tests(unittest.TestCase):
#     def setUp(self):
#         pass

# if __name__ == '__main__':
#     # unittest.main()
#     s = Story({'id': '123'})
