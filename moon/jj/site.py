from moon.models.page import load_blog_yaml
from flask import request, abort

from flask import get_template_attribute

import traceback

def render_blogs():
    endpoint = request.endpoint

    if endpoint != 'page':
        abort(404)

    name = request.view_args.get('name')

    # ?p=#
    try:
        p = int(request.args.get('p', 1))
    except:
        p = 1

    blogs = load_blog_yaml(name)
    blogs.current = p

    render = get_template_attribute('page_render.html', 'render_posts')

    try:
        return render(blogs)
    except Exception as e:
        traceback.print_exc(e)
        abort(500)

    abort(404)


def render_awards():
    return _render_macro('awards_render.html', 'render_awards')


def render_short_news(news):
    return _render_macro('page_render.html', 'render_short_news', news)

def render_all_news():
    return _render_macro('page_render.html', 'render_all_news')

def render_events():
    return _render_macro('events_render.html', 'render_events')


def render_phd_events():
    return _render_macro('events_render.html', 'render_phd_events')

def render_master_events():
    return _render_macro('events_render.html', 'render_master_events')

def _render_macro(template, macro, *args):
    try:
        render = get_template_attribute(template, macro)
        return render(*args)
    except Exception as e:
        traceback.print_exc(e)
        abort(500)

    abort(404)
