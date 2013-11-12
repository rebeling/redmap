#!/usr/bin/env python
# encoding: utf-8
import ConfigParser
# import logging as log


class ConfigData:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("cfg/secret.cfg")
        items = config.items('Credentials')
        items += config.items('Settings')
        for k, v in items:
            setattr(self, k, v)
