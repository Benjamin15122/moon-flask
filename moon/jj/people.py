
import flask, itertools
from flask import g, url_for

GROUP_LOGO = {
    'dse': '<img src="/static/img/logo-dse-small.png"/> ',
    'spar': '<img src="/static/img/logo-spar-small.png"/> ',
    'disalg': '<img src="/static/img/logo-disalg-small.png"/> ',
    'castle': '<img src="/static/img/logo-castle-small.png"/> ',
}

# People and people block (small)
PEOPLE_TEMPLATE_SM = u"""
<div class="col-lg-2 col-md-3 col-sm-4 col-xs-6">
<div class="pblock">
{% if url %} <a href="{{ url }}"> {% endif %}
<table><tr>
<td><img class="avatar" src="{{ avatar }}"/></td>
<td><span class="people-small">{{ name1 }}<br>{{ name2 }}</span></td>
</tr></table>
{% if url %} </a> {% endif %}
</div>
</div>
"""

BLOCK_TEMPLATE_SM = u"""
<div class="row people small people-small">
{% for block in peoples %}{{ block | safe }}{% endfor %}
</div>
"""

# People and people block (large)
PEOPLE_TEMPLATE_LG = u"""
<div class="col-lg-3 col-md-4 col-sm-6 col-xs-6">
<div class="pblock">
{% if url %} <a href="{{ url }}"> {% endif %}
<table><tr>
<td><img class="avatar" src="{{ avatar }}"/></td>
<td><span class="name">{{ name1 }}</span><br>
<span>{{ name2 | safe }}</span><br>
<span>{{ "" if not name3 else name3 | safe }}</span></td>
</tr></table>
{% if url %} </a> {% endif %}
</div>
</div>
"""

BLOCK_TEMPLATE_LG = u"""
<div class="row people small people-small">
{% for block in peoples %}{{ block | safe }}{% endfor %}
</div>
"""

def make_people_url(url):
    if url is None:
        return None

    if url.startswith('/'):
        return url

    if url.startswith('http://') or url.startswith('https://'):
        return url

    # the url is directory name
    return url_for('page', name=url)

def render_people(cond=None, category=None, large=False, group=None, center=None):
    if type(category) == str: category = [category]

    def render_one(p):
        avatar = p.get('avatar', '/static/img/avatar/default.jpg')
        mygroup = [i.strip() for i in p.get('group', '').split(',')]

        name = p['name'].split(' ')
        if len(name) == 2: (name1, name2) = ('', '')
        elif large:
            name1 = ' '.join(name)
            logo = ''.join([GROUP_LOGO[i] for i in mygroup if i in GROUP_LOGO])
            name2 = logo + p.get('title', str(p.get('from', '??')) + ' ' + u'\u2013')
        else:
            name1 = ' '.join(name[:-1])
            name2 = name[-1]
        
        name3=p.get("role")

        return flask.render_template_string(
            PEOPLE_TEMPLATE_LG if large else PEOPLE_TEMPLATE_SM,
            url = make_people_url(p.get('url', None)),
            name1 = name1, name2 = name2, name3 = name3,
            avatar = avatar)

    types = category if category else ['faculty', 'phd', 'graduates', 'alumni']
    peoples = sum([g.site.people[t] for t in types], [])

    def need_render(p):
        if center:
            if center not in p.get('center', ''): return False
        if group:
            if group not in p.get('group', ''): return False
        return True

    return flask.render_template_string(
        BLOCK_TEMPLATE_LG if large else BLOCK_TEMPLATE_SM,
        peoples = [render_one(p) for p in peoples if need_render(p)])

