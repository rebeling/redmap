#!/usr/bin/env python
# encoding: utf-8


# some stuff needs to be translated/transformed and this is specific to
# redmine and the user settings: languages, type of elements etc.
# todo: find a nicer way to solve this problem more general
translations = {
    "backlog": "backlog",
    "neu": "new",
    "erledigt": "done",
    "abgewiesen": "refused",
    "in bearbeitung": "in-progress",
    "gelöst": "qa !",
    "arbeitspaket": "package",
    "fehler": "bug",
    "unterstützung": "support"
}

def red_t_(input):
    if input in translations:
        return translations[input]
    else:
        return input

