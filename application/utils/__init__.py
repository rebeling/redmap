#!/usr/bin/env python
# encoding: utf-8
import datetime


def get_week_num_of(thisdate=None):
    if thisdate is None:
        thisdate = datetime.datetime.now()
    Year,WeekNum,DOW = thisdate.isocalendar()
    print Year,WeekNum,DOW
    return WeekNum

def write_content_to(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

def order_by_position(list_of_dicts):
    newlist = sorted(list_of_dicts, key=lambda k: k['position'])
    return newlist

if __name__ == '__main__':
    get_week_num_of()