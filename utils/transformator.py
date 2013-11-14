#!/usr/bin/env python
# encoding: utf-8
from redmine import t_
import logging as log


def restructure_data(data):
    """
        input is a json structure of the complete project
        so is the output, but restructured

        # 'Story': [{
        #     'subject':                 # title
        #     'description':             # description
        #     'created_on':              #
        #     'author':                  #
        #     'assigned_to.name':        #
        #     'fixed_version.name':      # Backlog, ...
        #     'due_date':                # to be ready
        #      ...
        # },
        # ]

        # 'Task' = {
        #     'storyId': {
        #         'taskId': {
        #             'subject':                 # title
        #             'description':             # description
        #             'created_on':              #
        #             'author':                  #
        #             'assigned_to.name':        #
        #             'fixed_version.name':      # Backlog, ...
        #             'due_date':                # to be ready
        #             ...
        #             'estimation':
        #             'realtime':
        #             'status':
        #             'blocked_by': [taskId]
        #
    """

    # total_count: data['total_count']
    restructure = {}
    for issue in data['issues']:
        # translate type Story, Task, Unterst...
        # and create a dict of all with a list of its issues
        type_of = t_(issue['tracker']['name'].encode('utf-8').lower())
        buffer = restructure.get(type_of, [])
        buffer.append(issue)
        restructure[type_of] = buffer

    new_items = {}
    no_parent = {
        "task": False,
        "bug": False,
        "feature": False
    }

    for key, items in restructure.iteritems():


        if key == "story":
            new_items[key] = new_items.get('story', [])

            for item in items:
                newone = restructure_item(key, item)
                if newone:
                    new_items[key].append(newone)

            # # in order to sort the stories and put the backlogs at the end
            # # we prefix 'sprint ' to 'backlog' and remove it after the sorting
            if 'fixed_version' in new_items[key][0]:
                stories = new_items[key]
                for story in stories:
                    if 'fixed_version' not in story:
                        story['fixed_version'] = 'None'
                    if 'backlog' in story['fixed_version']:
                        story['fixed_version'] = 'sprint ' + story['fixed_version']
                stories = sorted(stories, key=lambda k: k['fixed_version'])
                for story in stories:
                    if 'backlog' in story['fixed_version']:
                        story['fixed_version'] = story['fixed_version'][7:]

                new_items[key] = stories




        elif key == "package":

            # new_items[key] = new_items.get('story', [])

            for item in items:
                print item
                newone = restructure_item(key, item)
            #     if newone:
            #         new_items[key].append(newone)

            # # # in order to sort the stories and put the backlogs at the end
            # # # we prefix 'sprint ' to 'backlog' and remove it after the sorting
            # if 'fixed_version' in new_items[key][0]:
            #     stories = new_items[key]
            #     for story in stories:
            #         if 'fixed_version' not in story:
            #             story['fixed_version'] = 'None'
            #         if 'backlog' in story['fixed_version']:
            #             story['fixed_version'] = 'sprint ' + story['fixed_version']
            #     stories = sorted(stories, key=lambda k: k['fixed_version'])
            #     for story in stories:
            #         if 'backlog' in story['fixed_version']:
            #             story['fixed_version'] = story['fixed_version'][7:]

            #     new_items[key] = stories





        elif key  == "task":

            alltasks = {}

            for item in items:

                if 'parent' in item:
                    parentid = item['parent']['id']
                    tasks = alltasks.get(parentid, [])
                    tasks.append(restructure_item("task", item, parentid=parentid))
                    alltasks[parentid] = tasks
                else:
                    no_parent['task'] = True
                    tasks_without_parent = alltasks.get('no_parent_task', [])
                    tasks_without_parent.append(restructure_item("task", item))
                    alltasks['no_parent_task'] = tasks_without_parent

            thetasks = new_items.get("task", {})
            for k,v in alltasks.iteritems():
                if k in thetasks:
                    for x in v:
                        thetasks[k].append(x)
                else:
                    thetasks[k] = v
            new_items["task"] = thetasks



        elif key == "support":
            for item in items:
                if 'parent' in item:
                    print 'support with parent'
                new_items["story"].append(restructure_item(key, item))


        elif key == "bug" or key == "feature":

            x = key
            if x == "bug":
                var = "bug"
            else:
                var = "feature"
            alltasks = {}
            for item in items:

                if 'parent' in item:
                    print 'yes, parent in item. take care'
                    # parentid = item['parent']['id']
                    # tasks = alltasks.get(parentid, [])
                    # tasks.append(restructure_item(key, item, parentid=parentid))
                    # alltasks[parentid] = tasks
                    pass
                    # deal with them
                else:
                    if var == "bug":
                        no_parent['bug'] = True
                    else:
                        no_parent['feature'] = True

                    tasks_without_parent = alltasks.get('no_parent_%s' % var, [])
                    tasks_without_parent.append(restructure_item(key, item))
                    alltasks['no_parent_%s' % var] = tasks_without_parent

            thetasks = new_items.get("task", {})
            for k,v in alltasks.iteritems():
                if k in thetasks:
                    for x in v:
                        thetasks[k].append(x)
                else:
                    thetasks[k] = v
            new_items["task"] = thetasks






        # done
        # Story: 8 open / 9
        # Task: 3 open / 10
        # Unterstützung: 1 open / 1
        # Fehler: 0 open / 2
        # Feature << dummy story for feature ohne Story

        # todo
        # Arbeitspaket << ?! ?!

        else:
            print "another key ", key
            print items
            print



    # # at the end append a story dummy for every rubbish at least to show
    # # may its just created on run
    if no_parent['bug']:
        new_items = add_a_dummy_story(new_items, id='no_parent_bug',
                                subject='All bugs without a story')

    if no_parent['task']:
        new_items = add_a_dummy_story(new_items, id='no_parent_task',
                                subject='All tasks without a story')

    if no_parent['feature']:
        new_items = add_a_dummy_story(new_items, id='no_parent_task',
                                subject='All tasks without a story')

    return new_items


def add_a_dummy_story(new_items, id, subject):
    no_parent_dummy = {
        'id': id,
        'subject': subject,
        'description': '',
        'created_on': '',
        'author': {'name': 'AutoGenerated'},
        'assigned_to': {'name': ''},
        'status': {'name': 'different'},
    }
    stories = new_items.get('story', [])
    the_dummy = restructure_item('story', no_parent_dummy)
    stories.append(the_dummy)
    new_items['story'] = stories
    return new_items




def restructure_item(type_of, item, parentid=None):

    try:
        new_item = {
            'id': item['id'],
            'subject': t_(item['subject'].encode('utf-8')),
            'description': t_(item['description'].encode('utf-8')),
            'created_on': item['created_on'],
            'author': t_(item['author']['name'].encode('utf-8')),
            'assigned_to': t_(item['assigned_to']['name'].encode('utf-8')),
            'status': t_(item['status']['name'].lower().encode('utf-8')),
            # 'updated_on': item['updated_on'],
            # 'done_ratio': item['done_ratio']
            # 'due_date': item['due_date'],
        }

        try:
            new_item['fixed_version'] = t_(item['fixed_version']['name'].lower().encode('utf-8'))
        except:
            log.info("no such field")

        for field in ['start_date']:
            try:
                new_item[field] = item[field]
            except:
                log.info("no such field %s" % field)






        if type_of.encode('utf-8') == "Story":
            # print item
            new_item['type'] = 'story'
            pass

        elif type_of.encode('utf-8') == "Task":
            if parentid:
                new_item['parent'] = parentid
            new_item['type'] = 'task'

        elif type_of.encode('utf-8') == "Unterstützung":
            # print item
            new_item['type'] = 'support'

            # ...?!
            pass





        return new_item
    except Exception, e:
        print e
        return None

