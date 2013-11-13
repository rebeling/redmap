#!/usr/bin/env python
# encoding: utf-8
from redmine import t_
import logging as log


def restructure_data(data):

    # total_count: data['total_count']
    restructure = {}
    for issue in data['issues']:
        # Story, Task, Unterst...
        type_of = issue['tracker']['name']
        buffer = restructure.get(type_of, [])
        buffer.append(issue)
        restructure[type_of] = buffer



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





    new_items = {}
    no_parent_task = False
    no_parent_error = False
    no_parent_feature = False


    for key, items in restructure.iteritems():
        # print key.encode('utf-8')
        # print items
        # print "\n".join(items[0].keys())


        if key.encode('utf-8') == "Story" or key.encode('utf-8') == "Arbeitspaket":
            new_items[key] = new_items.get('Story', [])

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





        elif key.encode('utf-8')  == "Task":

            alltasks = {}

            for item in items:

                if 'parent' in item:
                    parentid = item['parent']['id']
                    tasks = alltasks.get(parentid, [])
                    tasks.append(restructure_item("Task", item, parentid=parentid))
                    alltasks[parentid] = tasks
                else:
                    no_parent_task = True
                    tasks_without_parent = alltasks.get('no_parent_task', [])
                    tasks_without_parent.append(restructure_item("Task", item))
                    alltasks['no_parent_task'] = tasks_without_parent



            thetasks = new_items.get("Task", {})
            for k,v in alltasks.iteritems():
                if k in thetasks:
                    for x in v:
                        thetasks[k].append(x)
                else:
                    thetasks[k] = v
            new_items["Task"] = thetasks



        elif key.encode('utf-8')  == "Unterstützung":

            for item in items:
                if 'parent' in item:
                    print 'support with parent'

                new_items["Story"].append(restructure_item(key, item))



        elif key.encode('utf-8')  == "Fehler" or key.encode('utf-8')  == "Feature":

            x = key.encode('utf-8')
            if x == "Fehler":
                var = "error"
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
                    if var == "error":
                        no_parent_error = True
                    else:
                        no_parent_feature = True

                    tasks_without_parent = alltasks.get('no_parent_%s' % var, [])
                    tasks_without_parent.append(restructure_item(key, item))
                    alltasks['no_parent_%s' % var] = tasks_without_parent

            thetasks = new_items.get("Task", {})
            for k,v in alltasks.iteritems():
                if k in thetasks:
                    for x in v:
                        thetasks[k].append(x)
                else:
                    thetasks[k] = v
            new_items["Task"] = thetasks






        # done
        # Story: 8 open / 9
        # Task: 3 open / 10
        # Unterstützung: 1 open / 1
        # Fehler: 0 open / 2
        # Feature << dummy story for feature ohne Story

        # todo
        # Arbeitspaket << ?! ?!

        else:
            print "another key ", key.encode('utf-8')
            print items
            print







    # # at the end append a story dummy for every rubbish at least to show
    # # may its just created on run
    if no_parent_error:
        no_parent_dummy = {
            'id': 'no_parent_error',
            'subject': 'All errors without a story',
            'description': '',
            'created_on': '',
            'author': {'name': 'AutoGenerated'},
            'assigned_to': {'name': ''},
            'status': {'name': 'different'},
        }
        stories = new_items.get('Story', [])
        the_dummy = restructure_item('Story', no_parent_dummy)
        stories.append(the_dummy)
        new_items['Story'] = stories

    if no_parent_task:
        no_parent_dummy = {
            'id': 'no_parent_task',
            'subject': 'All tasks without a story',
            'description': '',
            'created_on': '',
            'author': {'name': 'AutoGenerated'},
            'assigned_to': {'name': ''},
            'status': {'name': 'different'},
        }
        stories = new_items.get('Story', [])
        the_dummy = restructure_item('Story', no_parent_dummy)
        stories.append(the_dummy)
        new_items['Story'] = stories

    if no_parent_feature:
        no_parent_dummy = {
            'id': 'no_parent_feature',
            'subject': 'All features without a story',
            'description': '',
            'created_on': '',
            'author': {'name': 'AutoGenerated'},
            'assigned_to': {'name': ''},
            'status': {'name': 'different'},
        }
        stories = new_items.get('Story', [])
        the_dummy = restructure_item('Story', no_parent_dummy)
        stories.append(the_dummy)
        new_items['Story'] = stories

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

...?!
            pass





        return new_item
    except Exception, e:
        print e
        return None

