# -*- coding:utf-8

import flask, itertools
from flask import g

# People and people block (small)
PEOPLE_TEMPLATE_SM = """
<div class="col-lg-2 col-md-3 col-sm-6">
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

BLOCK_TEMPLATE_SM = """
<div class="row people small people-small">
{% for block in peoples %}{{ block | safe }}{% endfor %}
</div>
"""

# People and people block (large)
PEOPLE_TEMPLATE_LG = """
<div class="col-lg-3 col-md-6 col-sm-12">
<div class="pblock">
{% if url %} <a href="{{ url }}"> {% endif %}
<table><tr>
<td><img class="avatar" src="{{ avatar }}"/></td>
<td><span class="name">{{ name1 }}</span><br>
<span>{{ name2 }}</span></td>
</tr></table>
{% if url %} </a> {% endif %}
</div>
</div>
"""

BLOCK_TEMPLATE_LG = """
<div class="row people small people-small">
{% for block in peoples %}{{ block | safe }}{% endfor %}
</div>
"""

def render_people(cond = None, category = None, large = False, group = None):
    if type(category) == str: category = [category]

    def render_one(p):
        avatar = p.get('avatar', '/static/img/avatar/default.jpg')
        name = p['name'].split(' ')
        if len(name) == 2: (name1, name2) = ('', '')
        elif large:
            (name1, name2) = (' '.join(name), p.get('title', str(p.get('from', '??')) + ' –'))
        else:
            (name1, name2) = (' '.join(name[:-1]), name[-1])

        return flask.render_template_string(
            PEOPLE_TEMPLATE_LG if large else PEOPLE_TEMPLATE_SM,
            url = p.get('url', None),
            name1 = name1, name2 = name2,
            avatar = avatar)

    types = category if category else ['faculty', 'phd', 'graduates', 'alumni']
    peoples = sum([g.site.people[t] for t in types], [])

    def need_render(p):
        return not group or group in p.get('group', '')

    return flask.render_template_string(
        BLOCK_TEMPLATE_LG if large else BLOCK_TEMPLATE_SM,
        peoples = [render_one(p) for p in peoples if need_render(p)])

