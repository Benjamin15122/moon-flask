from flask import g

def render_people(group = None):
    def display_people(p):
        d = []
        d.append('<div class="col-lg-2 col-md-3 col-sm-6">')
        d.append('<div class="pblock">')

        if 'url' in p: d.append('<a href="%s">' % p['url'])

        d.append('<table><tr>')
        avatar = p.get('avatar', '/static/img/avatar/default.jpg')
        name = p['name'].split(' ')
        if len(name) == 2: name = ' '.join(name)
        else: name = ' '.join(name[:-1]) + '<br>' + name[-1]
            
        d.append('<td><img class="avatar" src="%s"/></td>' % avatar)
        d.append('<td><span class="spar-name">%s</span></td>' % name)

        d.append('</tr></table>')

        if 'url' in p: d.append('</a>')
        d.append('</div>')
        d.append('</div>')
        return '\n'.join(d)

    ret = []
    ret.append('''<div class="spar-people"><div class="row people" >''')
    for (key, name) in zip(
        ['faculty', 'phd', 'graduates', 'alumni'],
        ['Mentors', 'Ph.D. students', 'M.Sc. students', 'Alumni/ae'],
    ):
        ret.append("\n<h3>%s</h3>\n" % name)
        ret.append('<div class="row small k-equal-height">')
        for p in g.site.people[key]:
            groups = [i.strip() for i in p.get('group', '').split(',')]
            if group and group in groups:
                ret.append(display_people(p))
        ret.append('</div>')

    ret.append('</div></div>')

    peoples = '\n'.join(ret)
    return peoples

