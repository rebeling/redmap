app.controller 'ScrummapCtrl', ($scope, $window, DataExchange) ->
    console.log 'ScrummapCtrl'

    $scope.editmode = false

    $scope.sprinttog = null
    $scope.setsprinttog = (sprint) ->
        $scope.sprinttog = sprint

    $scope.checkclass = (vali) ->
        if $scope.sprinttog isnt null && $scope.sprinttog is vali
            'sprintclass'
        else if $scope.sprinttog isnt null && $scope.sprinttog isnt vali
            'sprintclassoff'
        else
            'schnup'

# /content/update_from_redmine_data

    $scope.redmine_data = () ->
        $scope.showloader = true
        DataExchange
            .get_updated_data_from_redmine()
            .then(
                (response) ->
                    console.log response
                    $scope.showloader = false
                    $window.location.reload()
                (data) ->
                    console.log 'error'
            )



    set_the_stories_obj = (response_data) ->
        $scope.stories = []
        for a_story,i in response_data.story
            related_tasks = response_data.task[a_story.id]
            $scope.stories.push storyObj(a_story, related_tasks)


    $scope.story_order = (type, storyid, direction) ->
        DataExchange
            ._reorder_story_item('story', storyid, storyid, direction)
            .then(
                (response) ->
                    console.log 'update'
                    $scope.showloader = false
                    set_the_stories_obj(response.data)
                (data) ->
                    console.log 'error'
            )

    $scope.task_order = (storyid, taskid, direction) ->
        DataExchange
            ._reorder_task_item('task', storyid, taskid, direction)
            .then(
                (response) ->
                    console.log 'update'
                    $scope.showloader = false
                    set_the_stories_obj(response.data)
                (data) ->
                    console.log 'error'
            )


    # $scope.highlight = (items, onoff) ->
    #     for item in items
    #         element = document.getElementById(item)
    #         if onoff is 0
    #             element.classList.add('highlight')
    #         else
    #             element.classList.remove('highlight')

    _estimations = (thistasks) ->
        # console.log "this", thistasks
        estimations =
            't_total': 0
            't_real': 0
            't_over': 0
            'c_done': 0
            'c_inprogress': 0
            'c_total': 0

        for key, value of thistasks
            # console.log key, value

            estimations.t_total += value.est
            estimations.c_total += 1

            if value.status is 'done'
                estimations.c_done += 1
                estimations.t_real += value.real
                x = value.est - value.real
                if x < 0
                    estimations.t_over += x * -1

            if value.status is 'inprogress'
                estimations.c_inprogress += 1
                estimations.t_real += value.real

        estimations


    _calc_progress = (est, real, status) ->

        if real is 0
            0
        else if status is 'done' or real > est or real is est
            100
        else if real < est

            # console.log real, est, (real * 100)/est
            # 100 - (((real - est) * 10) * -1)
            (real * 100)/est

        else
            0

    _blockedbysth = (blockedby) ->
        if blockedby.length > 0
            true
        else
            false

    storyObj = (story, related_tasks) ->

        task_ids = []
        if related_tasks
            for i,task in related_tasks
                task_ids.push task.id

        the_story = angular.copy(story)
        the_story['tasks'] = related_tasks
        the_story['task_ids'] = task_ids
        the_story['estimations'] = _estimations(related_tasks)
        the_story


    $scope.showloader = true
    DataExchange.get_items().then(
        (response) ->
            $scope.showloader = false
            set_the_stories_obj(response.data)
        (data) ->
            # console.log "ERROR", data.status
            $scope.showloader = false
            $scope.alert =
                type: 'warning'
                msg: 'Der Status der Anfrage ist ' + data.status + '.'
        )



app.controller 'PopoverDemoCtrl', ($scope) ->
    # console.log 'PopoverDemoCtrl'
    $scope.dynamicPopover = "Hello, World!";
    $scope.dynamicPopoverText = "dynamic";
    $scope.dynamicPopoverTitle = "Title";



app.controller 'IndexCtrl', ($scope) ->
    console.log 'IndexCtrl'

    $scope.menupoint = 'map'

    # $scope.handleDrop = (dropzone) ->

    #     console.log 'Item has been dropped into:', dropzone, this

    $scope.onDropEvent = (droppeditem,item2, me) ->


        console.log "droppeditem:", droppeditem.id, droppeditem.dataset, droppeditem, item2
        console.log "me.target.id:", me.target.id, me, me.target.field
        console.log "this:", this

        console.log "me.srcElement.attributes.field:", me.srcElement.attributes.field
        console.log me.srcElement.attributes.field.value
        console.log me.srcElement.attributes.user.value

        $scope.drag_and_dropped = droppeditem.id
        $scope.target_id = me.target.id


        $scope.dropped_field = me.srcElement.attributes.field.value
        $scope.user = me.srcElement.attributes.user.value
        $scope.qa_user = droppeditem.dataset


        if $scope.dropped_field is "f3" and droppeditem.dataset.qa
            if $scope.user isnt droppeditem.dataset.qa
                console.log
                console.log "from", $scope.user, "to", droppeditem.dataset.qa
                console.log "move to dropzone id ", "f3-"+droppeditem.dataset.qa


                dropzone = document.getElementById("f3-"+droppeditem.dataset.qa)
                dropzone.appendChild(droppeditem)

                console.log dropzone
