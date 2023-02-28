def activitylist(chosen):
    print '<table><tr><th>Column1</th><th>Column2</th>...</tr>'
    for row in choser:
        print '<tr>'
        for col in row:
            print '<td>%s</td>' % col
            print '</tr>'
            print '</table>'
