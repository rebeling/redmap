redmap
======

access the redmine data of a project


Configuration
----------------
The *secret.cfg* is ignored and contains your connection data, like this:

    [Credentials]
    redmine_url:x
    user:y
    pw:z
    key:a
    project:b


Used libraries
---------------
- Python 2.7
- ConfigParser - standard lib in 2
- Requests: HTTP for Humans - http://www.python-requests.org