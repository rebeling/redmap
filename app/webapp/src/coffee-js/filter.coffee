

app.filter 'twolines', () ->
    (subject) ->
        # console.log subject.length
        if subject.length > 40
            subject.slice(0,40) + ' ...'
        else
            subject
