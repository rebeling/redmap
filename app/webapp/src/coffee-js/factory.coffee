app.factory 'DataExchange', ($http, $rootScope) ->


    get_updated_data_from_redmine: () ->

        $http.get('http://localhost:5000/content/update_from_redmine_data')
            .success(
                (data, status, headers, config) ->
                    # console.log "success:", data, status, headers, config
            )
            .error(
                (data, status, headers, config) ->
                    # console.log "error:", data, status, headers, config
            )





    _reorder_story_item: (type, storyid, storyid2, direction) ->

        params = [type, storyid, storyid2, direction].join('/')
        $http.get('http://localhost:5000/update/order/' + params)
            .success(
                (data, status, headers, config) ->
                    # console.log "success:", data, status, headers, config
            )
            .error(
                (data, status, headers, config) ->
                    # console.log "error:", data, status, headers, config
            )


    _reorder_task_item: (type, storyid, taskid, direction) ->

        params = [type, storyid, taskid, direction].join('/')
        $http.get('http://localhost:5000/update/order/' + params)
            .success(
                (data, status, headers, config) ->
                    # console.log "success:", data, status, headers, config
            )
            .error(
                (data, status, headers, config) ->
                    # console.log "error:", data, status, headers, config
            )


    get_items: () ->

        $http.get('http://localhost:5000/content/all')
            .success(
                (data, status, headers, config) ->
                    # console.log "success:", data, status, headers, config
            )
            .error(
                (data, status, headers, config) ->
                    # console.log "error:", data, status, headers, config
            )