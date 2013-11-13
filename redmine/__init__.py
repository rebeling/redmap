#!/usr/bin/env python
# encoding: utf-8

# some stuff needs to be translated and this is specific to
# redmine and the user settings
# todo: find a nicer way to solve this problem more general

translations = {
    "backlog": "backlog",
    "neu": "new",
    "erledigt": "done",
    "abgewiesen": "refused",
    "in bearbeitung": "in-progress",
    "gelöst": "qa !"
}

def t_(input, translations):
    # translate or map input to
    if input in translations:
        return translations[input].encode('utf-8')
    else:
        return input.encode('utf-8')