module.exports = (grunt) ->

  # Project configuration.
  grunt.initConfig

    # compile your coffee files
    # https://github.com/gruntjs/grunt-contrib-coffee
    coffee:
      options:
        join: true
      app:
        files:
          'app/befe/static/js/myapp.js': [
                                  'app/befe/fe_src/coffee-js/app.coffee',
                                  'app/befe/fe_src/coffee-js/controller.coffee',
                                  'app/befe/fe_src/coffee-js/directives.coffee',
                                  'app/befe/fe_src/coffee-js/factory.coffee'
                                  'app/befe/fe_src/coffee-js/filter.coffee'],

    # compiles your stylus to css files
    # https://github.com/gruntjs/grunt-contrib-stylus
    stylus:
      compile:
        options:
          compress: true
        files:
          'app/befe/static/css/main.css': ['app/befe/fe_src/stylus-css/*.styl']

    # minifiy html files
    # https://github.com/gruntjs/grunt-contrib-htmlmin
    htmlmin:
      app:
        # # turn on for production
        # options:
        #   removeComments: true
        #   collapseWhitespace: true
        files:
          'app/befe/templates/index.html': 'app/befe/fe_src/index.templ.html'
          # 'webapp/partials/index.view.html': 'src/partials-html/index.view.templ.html'

    # start the watch dog and bark on save
    # https://github.com/gruntjs/grunt-contrib-watch
    watch:
      app:
        files: ['**/*.coffee', '**/*.templ.html', '**/*.styl']
        tasks: ['coffee', 'stylus', 'htmlmin']

    # add project release
    # release:



  # necessary plugins
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-stylus'
  grunt.loadNpmTasks 'grunt-contrib-htmlmin'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  # default task
  grunt.registerTask 'default', ['coffee', 'stylus', 'htmlmin']
