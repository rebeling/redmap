#!/usr/bin/env python
# encoding: utf-8


def t_(input):
    # translate or map input to
    translate = {
        "Backlog": "backlog",
        "Neu": "new"
    }
    if input in translate:
        return translate[input]
    else:
        return input