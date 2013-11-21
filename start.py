#!/usr/bin/env python
# encoding: utf-8
from application.utils import red
import logging.config
import logging as log
import sys


def main():
    logging.config.fileConfig('cfg/logging.cfg')
    cl_args = sys.argv
    log.info("args: %s" % cl_args)

    if 'red' in cl_args:
        from application.redmine import process_project
        process_project(red)

    if 'api' in cl_args:
        from application.api import app
        app.run(debug=True)


if __name__ == '__main__':
    main()
