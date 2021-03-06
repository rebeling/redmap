#!/usr/bin/env python
# encoding: utf-8
import datetime
from app.utils.config_parser import ConfigData
import logging as log
import time


red = ConfigData()


def timing(f):
    def wrap(*args):
        t1 = time.time()
        ret = f(*args)
        t2 = time.time()
        print "» %.2f sec" % (t2 - t1), f.func_name
        return ret
    return wrap


def get_week_num_of(thisdate=None):
    if thisdate is None:
        thisdate = datetime.datetime.now()
    Year,WeekNum,DOW = thisdate.isocalendar()
    print Year,WeekNum,DOW
    return WeekNum


def write_content_to(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)

def order_by_key(list_of_dicts, key2order):
    try:
        newlist = sorted(list_of_dicts, key=lambda k: k[key2order])
    except Exception, e:
        log.error("no way %s" % e)

    return newlist


if __name__ == '__main__':
    get_week_num_of()