import flask, itertools
from flask import g

PEOPLE_TEMPLATE = """
<div class="col-lg-2 col-md-3 col-sm-6">
<div class="pblock">
    {% if url %} <a href="{{ url }}"> {% endif %}
    <table><tr>
        <td><img class="avatar" src="{{ avatar }}"/></td>
        <td><span class="spar-name">{{ name | safe }}</span></td>
    </tr></table>
    {% if url %} </a> {% endif %}
</div>
</div>
"""

BLOCK_TEMPLATE = """
<div class="spar-people">
<div class="row people">
<div class="row small">
{% for block in peoples %}{{ block | safe }}{% endfor %}
</div>
</div>
</div>
"""

def render_people(cond = None, category = None, group = None):
    if type(category) == str: category = [category]

    def render_one(p):
        avatar = p.get('avatar', '/static/img/avatar/default.jpg')
        if 'name' not in p: return ''
        name = p['name'].split(' ')
        if len(name) == 2: name = ' '.join(name)
        else: name = ' '.join(name[:-1]) + '<br>' + name[-1]

        return flask.render_template_string(PEOPLE_TEMPLATE,
            url = p.get('url', None),
            name = name,
            avatar = avatar)

    types = category if category else ['faculty', 'phd', 'graduates', 'alumni']
    peoples = sum([g.site.people[i] for i in types], [])

    def need_render(p):
        return not group or group in p.get('group', '')

    return flask.render_template_string(BLOCK_TEMPLATE,
        peoples = [render_one(p) for p in peoples if need_render(p)])

