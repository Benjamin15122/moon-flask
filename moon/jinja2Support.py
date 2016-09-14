from moon import app
from citation import Citations, render_bib_entry
from views import get_user_dir
from flask import request, g, safe_join


import time
def render_bib_file(path=None, keys=None, hl='', group_by_year=False):
    if not path:
        return g.site.paper.render_all(hl, group_by_year)

    if request.endpoint == 'page':
        name = request.view_args['name']

        user_dir = get_user_dir(name)
        bibfile = safe_join(user_dir, path)
    else:
        bibfile = safe_join(MOON_DIR, path)


    try:
        c = Citations(bibfile)

        if not keys:
            return c.render_all(hl, group_by_year)
        elif isinstance(keys, str):
            return c.render_entry(keys, hl)
        else:
            return c.render_entries(keys, hl, group_by_year)
    except Exception as e:
        return "<em>render path=%s, keys=%s, hl=%s, group_by_year=%s failed! </em>" % (path, keys, hl, group_by_year)

    return "<em>No such bib file " + path + "</em>"



app.jinja_env.globals.update(render_bib_entry=render_bib_entry)
app.jinja_env.globals.update(render_bib_file=render_bib_file)
