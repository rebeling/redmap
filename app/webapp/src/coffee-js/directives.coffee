
 # ['$compile', 'myData', function($compile, myData){

app.directive 'sprintSelector', (DataExchange) ->
    restrict: 'E'
    replace: true

    link: (scope, elem, attr) ->
        scope.ttf_key = attr.key
        scope.ttf_value = attr.initialvalue
        scope.ttf_values = ['kw01', 'kw02', 'kw03', 'kw04', 'kw05', 'kw06', 'future']
        scope.item = attr.item
        scope.type_of = attr.itemtype

        scope.settype = (item, sprint, type_of) ->

            if type_of is 'task'
                storyid = item.parent
                taskid = item.id
            else
                storyid = item.id
                taskid = 'None'

            DataExchange._update_sprint(storyid, taskid, sprint, type_of).then(
                (response) ->
                    console.log "response:", response
                    scope.ttf_value = sprint
                (data) ->
                    console.log "data:", data
                )

    template: '<div class="btn-group">' +
                  '<button type="button" class="btn btn-xs dropdown-toggle" data-toggle="dropdown">' +
                    '{{ttf_value}} <span class="caret"></span>' +
                  '</button>' +
                '<ul class="dropdown-menu" role="menu">' +
                    '<li class="{{entity}}" ng-repeat="entity in ttf_values">' +
                        '<a ng-click="settype({{item}}, \'{{entity}}\', type_of)">{{entity}}</a>' +
                    '</li>' +
                '</ul>' +
              '</div>'



app.directive 'sorter', ->
    restrict: 'E'
    template: '<span class="sorter"><i class="icon-sort-down"></i>' +
              '<i class="icon-sort-up"></i></span>'


app.directive 'draggable', ->

	(scope, element) ->
        # this gives us the native JS object
        console.log "draggable element", element
        el = element[0]
        el.draggable = true
        el.addEventListener(
            'dragstart',
            (e) ->
                console.log "drag starts", e.dataTransfer
                e.dataTransfer.effectAllowed = 'move'

                console.log "this", this

                # newone = this.id
                # newone.classList.add("moving")

                e.dataTransfer.setData('Text', this.id)

                this.classList.add('drag')

        )
        el.addEventListener(
            'dragend',
            (e) ->
                console.log "dragend"
                this.classList.remove('drag')
        )


app.directive 'droppable', ->
    scope:
        # drop: '&' # parent
        onDrop: '=', # parent's method to call on drop event
    link: (scope, element) ->
        # again we need the native object
        console.log "droppable element", element
        el = element[0]

        el.addEventListener(
            'dragover',
            (e) ->
                console.log "dragover"
                e.dataTransfer.dropEffect = 'move'
                # allows us to drop
                if e.preventDefault
                    e.preventDefault()
                this.classList.add('over')
        )

        el.addEventListener(
            'dragenter',
            (e) ->
                console.log "dragenter"
                this.classList.add('over')
        )
        el.addEventListener(
            'dragleave',
            (e) ->
                console.log "dragleave"
                this.classList.remove('over')
        )

        el.addEventListener(
            'drop',
            (e) ->
                console.log "dropped"
                # Stops some browsers from redirecting.
                if e.stopPropagation
                    e.stopPropagation()
                this.classList.remove('over')

                # add item to dropzone
                item = document.getElementById(e.dataTransfer.getData('Text'))
                item2 = document.getElementById(e.dataTransfer) #.getData('Text'))
                this.appendChild(item)
                # call the drop passed drop function
                scope.onDrop(item,item2, e)
                scope.$apply('drop()')
        )







# <div ng-controller="PopoverDemoCtrl">
#   <div class="well">
#     <div>
#       <h4>Dynamic</h4>
#       <div>Dynamic Popover : <input type="text" ng-model="dynamicPopoverText"></div>
#       <div>Dynamic Popover Popup Text: <input type="text" ng-model="dynamicPopover"></div>
#       <div>Dynamic Popover Popup Title: <input type="text" ng-model="dynamicPopoverTitle"></div>
#       <div><button popover="{{dynamicPopover}}" popover-title="{{dynamicPopoverTitle}}" class="btn">{{dynamicPopoverText}}</button></div>
#     </div>
#     <div>
#       <h4>Positional</h4>
#       <button popover-placement="top" popover="On the Top!" class="btn">Top</button>
#       <button popover-placement="left" popover="On the Left!" class="btn">Left</button>
#       <button popover-placement="right" popover="On the Right!" class="btn">Right</button>
#       <button popover-placement="bottom" popover="On the Bottom!" class="btn">Bottom</button>
#     </div>
#     <div>
#       <h4>Triggers</h4>
#       <button popover="I appeared on mouse enter!" popover-trigger="mouseenter" class="btn">Mouseenter</button>
#       <input type="text" value="Click me!"
#         popover="I appeared on focus! Click away and I'll vanish..."
#         popover-trigger="focus" />
#     </div>
#     <div>
#       <h4>Other</h4>
#       <button Popover-animation="true" popover="I fade in and out!" class="btn">fading</button>
#       <button popover="I have a title!" popover-title="The title." class="btn">title</button>
#     </div>
#   </div>
# </div>






# pop over msg
app.directive 'popOverStory', () ->
    restrict: 'E'
    # replace: true
    # scope: {content: '=content'}
    link: (scope, elem, attr) ->

        # console.log scope, elem, attr
        # console.log
        # console.log content
        scope.type_of_popover = 'story'
        scope.position = 'right'
        scope.id = 'story.id'
        scope.subject = 'story.subject'
        scope.description = 'a description'

        # description is little bit complex

        # scope.description = '<dt>Estimated</dt>' +
        #     '<dd>{{story.estimations.t_total}} h ({{story.estimations.t_real}})</dd>' +
        #     '<dt>Author</dt>'
            # <dd>{{story.author}}</dd>
            # <dt>Assigned</dt>
            # <dd>{{story.assigned_to}}</dd>
            # <dt>Type</dt>
            # <dd>{{story.type}}</dd>



        # console.log "popOverStory attr:", attr

    template: '<a class="poping" ng-switch on="type_of_popover">' +
                '<span ng-switch-when="story" popover-placement="{{position}}" popover-title="{{subject}} {{id}}" popover="{{description}}" popover-trigger="mouseenter"> <i class="fa fa-info-circle"></i> </span>' +
                '<span ng-switch-default popover-placement="right" popover="boom" popover-trigger="mouseenter"><i class="fa fa-info"></i></span>' +
              '</a>'

        # scope.text = attr.text
        # scope.poping = 'yeh'
        # # if attr.title
        # if attr.link
        #     scope.poping = 'linkandtitle'
        #     scope.link = attr.link
        #     scope.title = attr.title

        # if attr.position
        #     scope.position = attr.position
        # else
        #     scope.position = 'top'

    # template: '<a class="poping" ng-switch on="poping">' +
    #             '<span ng-switch-when="linkandtitle" popover-placement="{{position}}" popover-title="{{title}}" popover="{{text}}" popover-trigger="mouseenter">{{link}}</span>' +
    #             '<span ng-switch-default popover-placement="{{position}}" popover="{{text}}" popover-trigger="mouseenter"><i class="icon-info-sign"></i></span>' +
    #           '</a>'


