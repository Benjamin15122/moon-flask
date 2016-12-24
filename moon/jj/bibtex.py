from moon.models.bibtex import Citations, render_bib_entry
from moon.models.page import get_user_dir
from flask import request, g, safe_join
import traceback

from moon import PAGES_DIR, MOON_DIR

import time, os

def render_bib_file(path=None, keys=None, hl='', group_by_year=False):
    if not path:
        return g.site.paper.render_all(hl, group_by_year)

    if request.endpoint == 'page':
        base_dir = request.path[1:] # remove leading '/'
        if not base_dir.endswith('/'):
            base_dir = os.path.dirname(base_dir) # get dir
        bibfile = safe_join(PAGES_DIR, base_dir + '/' + path)
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
    except Exception:
        traceback.print_exc()
        return "<em>render path=%s, keys=%s, hl=%s, group_by_year=%s failed! </em>" % (path, keys, hl, group_by_year)

    return "<em>No such bib file " + path + "</em>"
