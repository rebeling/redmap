

app.filter 'twolines', () ->
    (subject) ->
        # console.log subject.length
        if subject.length > 40
            subject.slice(0,40) + ' ...'
        else
            subject


app.filter 'initialen', () ->
    (name) ->
        # console.log subject.length
        initialen = ''
        for x in name.split(' ')
            initialen += x[0]
        initialen

