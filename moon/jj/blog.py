from moon.models.site import Blogs
from moon.models.page import Pagination
from flask import request, abort

from flask import get_template_attribute

import traceback

def render_blogs():
    endpoint = request.endpoint

    if endpoint != 'page':
        abort(404)

    name = request.view_args.get('name')

    # ?p=#
    p = request.args.get('p', 1)

    blogs = Blogs(name, p)

    render = get_template_attribute('post_render.html', 'render_posts')

    try:
        return render(blogs)
    except Exception as e:
        traceback.print_exc(e)
        abort(500)

    abort(404)

