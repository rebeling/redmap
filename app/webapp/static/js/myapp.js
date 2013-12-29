(function() {
  'use strict';
  /* Declare app level module which depends on filters, and services*/

  var app, app_name;

  app_name = "schmite";

  app = angular.module(app_name, ['ui.bootstrap']);

  app.controller('ScrummapCtrl', function($scope, $window, DataExchange) {
    var set_the_stories_obj, storyObj, _blockedbysth, _calc_progress, _estimations;
    console.log('ScrummapCtrl');
    $scope.editmode = false;
    $scope.redmine_data = function() {
      $scope.showloader = true;
      return DataExchange.get_updated_data_from_redmine().then(function(response) {
        console.log(response);
        $scope.showloader = false;
        return $window.location.reload();
      }, function(data) {
        return console.log('error');
      });
    };
    set_the_stories_obj = function(response_data) {
      var a_story, i, related_tasks, _i, _len, _ref, _results;
      $scope.stories = [];
      _ref = response_data.story;
      _results = [];
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
        a_story = _ref[i];
        related_tasks = response_data.task[a_story.id];
        _results.push($scope.stories.push(storyObj(a_story, related_tasks)));
      }
      return _results;
    };
    $scope.story_order = function(type, storyid, direction) {
      return DataExchange._reorder_story_item('story', storyid, storyid, direction).then(function(response) {
        console.log('update');
        $scope.showloader = false;
        return set_the_stories_obj(response.data);
      }, function(data) {
        return console.log('error');
      });
    };
    $scope.task_order = function(storyid, taskid, direction) {
      return DataExchange._reorder_task_item('task', storyid, taskid, direction).then(function(response) {
        console.log('update');
        $scope.showloader = false;
        return set_the_stories_obj(response.data);
      }, function(data) {
        return console.log('error');
      });
    };
    _estimations = function(thistasks) {
      var estimations, key, value, x;
      estimations = {
        't_total': 0,
        't_real': 0,
        't_over': 0,
        'c_done': 0,
        'c_inprogress': 0,
        'c_total': 0
      };
      for (key in thistasks) {
        value = thistasks[key];
        estimations.t_total += value.est;
        estimations.c_total += 1;
        if (value.status === 'done') {
          estimations.c_done += 1;
          estimations.t_real += value.real;
          x = value.est - value.real;
          if (x < 0) {
            estimations.t_over += x * -1;
          }
        }
        if (value.status === 'inprogress') {
          estimations.c_inprogress += 1;
          estimations.t_real += value.real;
        }
      }
      return estimations;
    };
    _calc_progress = function(est, real, status) {
      if (real === 0) {
        return 0;
      } else if (status === 'done' || real > est || real === est) {
        return 100;
      } else if (real < est) {
        return (real * 100) / est;
      } else {
        return 0;
      }
    };
    _blockedbysth = function(blockedby) {
      if (blockedby.length > 0) {
        return true;
      } else {
        return false;
      }
    };
    storyObj = function(story, related_tasks) {
      var i, task, task_ids, the_story, _i, _len;
      task_ids = [];
      if (related_tasks) {
        for (task = _i = 0, _len = related_tasks.length; _i < _len; task = ++_i) {
          i = related_tasks[task];
          task_ids.push(task.id);
        }
      }
      the_story = angular.copy(story);
      the_story['tasks'] = related_tasks;
      the_story['task_ids'] = task_ids;
      the_story['estimations'] = _estimations(related_tasks);
      return the_story;
    };
    $scope.showloader = true;
    return DataExchange.get_items().then(function(response) {
      $scope.showloader = false;
      return set_the_stories_obj(response.data);
    }, function(data) {
      $scope.showloader = false;
      return $scope.alert = {
        type: 'warning',
        msg: 'Der Status der Anfrage ist ' + data.status + '.'
      };
    });
  });

  app.controller('PopoverDemoCtrl', function($scope) {
    $scope.dynamicPopover = "Hello, World!";
    $scope.dynamicPopoverText = "dynamic";
    return $scope.dynamicPopoverTitle = "Title";
  });

  app.controller('IndexCtrl', function($scope) {
    console.log('IndexCtrl');
    $scope.menupoint = 'map';
    return $scope.onDropEvent = function(droppeditem, item2, me) {
      var dropzone;
      console.log("droppeditem:", droppeditem.id, droppeditem.dataset, droppeditem, item2);
      console.log("me.target.id:", me.target.id, me, me.target.field);
      console.log("this:", this);
      console.log("me.srcElement.attributes.field:", me.srcElement.attributes.field);
      console.log(me.srcElement.attributes.field.value);
      console.log(me.srcElement.attributes.user.value);
      $scope.drag_and_dropped = droppeditem.id;
      $scope.target_id = me.target.id;
      $scope.dropped_field = me.srcElement.attributes.field.value;
      $scope.user = me.srcElement.attributes.user.value;
      $scope.qa_user = droppeditem.dataset;
      if ($scope.dropped_field === "f3" && droppeditem.dataset.qa) {
        if ($scope.user !== droppeditem.dataset.qa) {
          console.log;
          console.log("from", $scope.user, "to", droppeditem.dataset.qa);
          console.log("move to dropzone id ", "f3-" + droppeditem.dataset.qa);
          dropzone = document.getElementById("f3-" + droppeditem.dataset.qa);
          dropzone.appendChild(droppeditem);
          return console.log(dropzone);
        }
      }
    };
  });

  app.directive('sprintSelector', function() {
    return {
      restrict: 'E',
      replace: true,
      link: function(scope, elem, attr) {
        scope.ttf_key = attr.key;
        scope.ttf_value = attr.initialvalue;
        scope.ttf_values = [1, 2, 3, 4, 5, 6];
        if (scope.ttf_values.indexOf(scope.ttf_value === -1)) {
          return scope.ttf_values.unshift(scope.ttf_value);
        }
      },
      template: '<div class="btn-group">' + '<button type="button" class="btn btn-default btn-xs dropdown-toggle" data-toggle="dropdown">' + 'sprint {{ttf_value}} <span class="caret"></span>' + '</button>' + '<ul class="dropdown-menu" role="menu">' + '<li class="{{entity}}" ng-repeat="entity in ttf_values">' + '<a ng-click="settype(\'{{entity}}\')">sprint {{entity}}</a>' + '</li>' + '</ul>' + '</div>'
    };
  });

  app.directive('sorter', function() {
    return {
      restrict: 'E',
      template: '<span class="sorter"><i class="icon-sort-down"></i>' + '<i class="icon-sort-up"></i></span>'
    };
  });

  app.directive('draggable', function() {
    return function(scope, element) {
      var el;
      console.log("draggable element", element);
      el = element[0];
      el.draggable = true;
      el.addEventListener('dragstart', function(e) {
        console.log("drag starts", e.dataTransfer);
        e.dataTransfer.effectAllowed = 'move';
        console.log("this", this);
        e.dataTransfer.setData('Text', this.id);
        return this.classList.add('drag');
      });
      return el.addEventListener('dragend', function(e) {
        console.log("dragend");
        return this.classList.remove('drag');
      });
    };
  });

  app.directive('droppable', function() {
    return {
      scope: {
        onDrop: '='
      },
      link: function(scope, element) {
        var el;
        console.log("droppable element", element);
        el = element[0];
        el.addEventListener('dragover', function(e) {
          console.log("dragover");
          e.dataTransfer.dropEffect = 'move';
          if (e.preventDefault) {
            e.preventDefault();
          }
          return this.classList.add('over');
        });
        el.addEventListener('dragenter', function(e) {
          console.log("dragenter");
          return this.classList.add('over');
        });
        el.addEventListener('dragleave', function(e) {
          console.log("dragleave");
          return this.classList.remove('over');
        });
        return el.addEventListener('drop', function(e) {
          var item, item2;
          console.log("dropped");
          if (e.stopPropagation) {
            e.stopPropagation();
          }
          this.classList.remove('over');
          item = document.getElementById(e.dataTransfer.getData('Text'));
          item2 = document.getElementById(e.dataTransfer);
          this.appendChild(item);
          scope.onDrop(item, item2, e);
          return scope.$apply('drop()');
        });
      }
    };
  });

  app.directive('popOverStory', function() {
    return {
      restrict: 'E',
      link: function(scope, elem, attr) {
        scope.type_of_popover = 'story';
        scope.position = 'right';
        scope.id = 'story.id';
        scope.subject = 'story.subject';
        return scope.description = 'a description';
      },
      template: '<a class="poping" ng-switch on="type_of_popover">' + '<span ng-switch-when="story" popover-placement="{{position}}" popover-title="{{subject}} {{id}}" popover="{{description}}" popover-trigger="mouseenter"> <i class="fa fa-info-circle"></i> </span>' + '<span ng-switch-default popover-placement="right" popover="boom" popover-trigger="mouseenter"><i class="fa fa-info"></i></span>' + '</a>'
    };
  });

  app.factory('DataExchange', function($http, $rootScope) {
    return {
      get_updated_data_from_redmine: function() {
        return $http.get('http://localhost:5000/content/update_from_redmine_data').success(function(data, status, headers, config) {}).error(function(data, status, headers, config) {});
      },
      _reorder_story_item: function(type, storyid, storyid2, direction) {
        var params;
        params = [type, storyid, storyid2, direction].join('/');
        return $http.get('http://localhost:5000/update/order/' + params).success(function(data, status, headers, config) {}).error(function(data, status, headers, config) {});
      },
      _reorder_task_item: function(type, storyid, taskid, direction) {
        var params;
        params = [type, storyid, taskid, direction].join('/');
        return $http.get('http://localhost:5000/update/order/' + params).success(function(data, status, headers, config) {}).error(function(data, status, headers, config) {});
      },
      get_items: function() {
        return $http.get('http://localhost:5000/content/all').success(function(data, status, headers, config) {}).error(function(data, status, headers, config) {});
      }
    };
  });

  app.filter('twolines', function() {
    return function(subject) {
      if (subject.length > 40) {
        return subject.slice(0, 40) + ' ...';
      } else {
        return subject;
      }
    };
  });

}).call(this);
