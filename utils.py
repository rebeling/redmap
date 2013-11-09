#!/usr/bin/env python
# encoding: utf-8
import ConfigParser


class ConfigData:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("secret.cfg")
        this_credentials = ['key', 'user', 'pw', 'redmine_url', 'project']
        data = {x: config.get('Credentials',x) for x in this_credentials}
        for k, v in data.items():
            setattr(self, k, v)
