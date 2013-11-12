#!/usr/bin/env python
# encoding: utf-8
import ConfigParser
# import logging as log


class ConfigData:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("cfg/secret.cfg")
        for k, v in config.items('Credentials'):
            setattr(self, k, v)
