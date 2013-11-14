redmap
======

transforms the data of a redmine project to a more general structure


Configuration
----------------
The *cfg/secret.cfg* is ignored and contains your connection data, like this:

    [Credentials]
    redmine_url:x
    user:y
    pw:z
    key:a

    [Settings]
    project:b
    limit=c
    filepath:d


Requirement Rules
-------------------
...


Used libraries
---------------
- Python 2.7
- ConfigParser - standard lib in 2
- Requests: HTTP for Humans - http://www.python-requests.org