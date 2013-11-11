#!/usr/bin/env python
# encoding: utf-8
# import logging as log


def t_(input):
    # translate or map input to
    translate = {
        "Backlog": "backlog",
        "Neu": "new"
    }
    if input in translate:
        return translate[input].encode('utf-8')
    else:
        return input.encode('utf-8')