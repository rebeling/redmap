#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import logging.config
import logging as log
from app.webapp import app
from app.redmine.get_content import analize_project


def main():
    logging.config.fileConfig('cfg/logging.cfg')
    cl_args = sys.argv
    log.info("args: %s" % cl_args)

    if 'red' in cl_args:
        analize_project()

    if 'app' in cl_args:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
