redmap
======

transforms the data of a redmine project to a more general structure


Todo
-----
- get spent_hours and transfer all calculations from frontend
    to the backend ...no need to do this in frontend
- get done ratio of task
- write install instructions


Configuration
----------------
The *cfg/secret.cfg* is ignored and contains your connection data, like this:

    [Credentials]
    url:x
    user:y
    pw:z
    key:a

    [Settings]
    project:b
    limit=c
    filepath:d


Rules and Definitions
----------------------
Using artificial structures and self defined stuff in your pm-tool makes you
need to change this code heavily. But if you go with the following its pretty
easy:

- Story
- Task / Feature / Bug


Data Storage
---------------------
At the moment, the data s stored as json in files. In future it would be nice
to use a datastorage - wish it will be pouchdb - to augment the datastructure.
Due to the lack of functionality at your current tool, you can extend the data
somehow and needs to be updated ...if needed and so on.


Used libraries
---------------
- Python 2.7
- ConfigParser - standard lib in 2
- Requests: HTTP for Humans - http://www.python-requests.org
- Flask - http://flask.pocoo.org/
- Angularjs
- Grunt


Installations
---------------
Uses coffee, angularjs, stylus and compiles via Grunt:
this needs to be installed locally or global

    npm install
    npm install grunt-contrib-coffee --save-dev
    npm install grunt-contrib-stylus --save-dev
    npm install grunt-contrib-htmlmin --save-dev
    npm install grunt-contrib-watch --save-dev


To build, run `grunt`.

To watch, run `grunt watch`.


...more instructions will follow