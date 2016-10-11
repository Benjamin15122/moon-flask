from moon import *
#from models import Site, get_page

from models.site import Site
from models.bundle import Bundle
from models.page import get_page, get_user_dir, Pagination

from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g, render_template_string
import sys, os, subprocess

from datetime import datetime, timedelta
from utils import to_date, to_time, to_datetime


from moon.md import create_markdown


def remove_dead_events(events):
    yesterday = datetime.now() + timedelta(days=-1)
    return filter(lambda e: yesterday < to_datetime(e.get('date', '')), events)


##################

def decorate_g():
    g.site = Site()
    g.bundle = Bundle()

@app.errorhandler(404)
def page_not_found(e):
    '''Custom 404 page

    '''
    if not hasattr(g, 'site'):
        decorate_g()
    return render_template('404.html'), 404

@app.before_request
def before_request():
    ''' Callback before each request

    TODO: in fact all load should be done here
    '''
    # We should use request.endpoint == 'static'
    # However, not all static files are fetched from global static directory
    # Currently, we check whether there is a `/static/' in the path
    if '/static/' not in request.path:
        g.md = create_markdown()
        decorate_g()

@app.teardown_request
def teardown_request(exception):
    pass

#####################

@app.route('/news/', methods=['GET'])
@app.route('/news/<int:page_num>', methods=['GET'])
def news(page_num=None):
    if page_num is None:
        page_num = 1

    #load_news()
    n = g.site.news
    pg = Pagination(n)
    pg.current = page_num
    return render_template('news.html', news=n, pg=pg)

@app.route('/news/<path>', methods=['GET'])
def short_news(path=None):
    page = get_page(NEWS_DIR, path)
    template = page.meta.get('template')
    if not template:
        print("notepage")
        abort(404)

    t = page.meta.get('type')

    if t is None:
        abort(404)
    elif t == 'paper':
        items = g.site.paper_news
    elif t == 'award':
        items = g.site.award_news
    elif t == 'scholarship':
        items = g.site.scholarship_news
    else:
        abort(404)
    return render_template(template, title=page.meta.get('title'), items=items)

@app.route('/news/page/<path:path>', methods=['GET'])
def news_page(path):
    page = get_page(NEWS_DIR, path)

    template = page.meta.get('template', 'news-page.html')
    return render_template(template, page=page)


#####################

@app.route('/events/', methods=['GET'])
@app.route('/events/<path:path>/', methods=['GET'])
def events(path=None):
    if path is None:
        #load_events()
        #load_phd_events()
        #load_deadlines()
        return render_template('events.html', events=g.site.events, deadlines=g.site.deadlines, phd=g.site.phd_events)

    if path == 'deadlines':
        #load_deadlines()
        return render_template('deadlines.html', deadlines=g.site.deadlines)

    if path == 'phd':
        #load_phd_events()
        return render_template('phd.html', phd=g.site.phd_events)

    if path == 'master':
        #load_master_events()
        return render_template('master.html', master=g.site.master_events)

    page = get_page(EVENTS_DIR, path)

    template = page.meta.get('template', 'events-page.html')
    return render_template(template, page=page)

#####################

@app.route('/', methods=['GET'])
def index():
    # remove dead events on index page
    return render_template('index.html', news=g.site.news, \
            events=g.site.events, members=g.site.people, \
            deadlines=remove_dead_events(g.site.deadlines), \
            phd=remove_dead_events(g.site.phd_events), \
            master=remove_dead_events(g.site.master_events))

#####################

@app.route('/about/', methods=['GET'])
def about():
    page = get_page(PAGES_DIR, 'about')
    template = page.meta.get('template', 'people-page.html')
    return render_template(template, page=page)

@app.route('/people/', methods=['GET'])
def people():
    return render_template('people.html', people=g.site.people)

@app.route('/awards/', methods=['GET'])
def awards():
    return render_template('awards.html')

@app.route('/contact/', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/research/', methods=['GET'])
def research():
    return render_template('research.html')

@app.route('/dse/', methods=['GET'])
@app.route('/dse/<path:path>', methods=['GET'])
def dse(path=None):
    if path is None:
        page = get_page(DSE_DIR, 'index')
    else:
        page = get_page(DSE_DIR, path)
    template = page.meta.get('template', 'dse-page.html')
    return render_template(template, page=page)

@app.route('/<path:path>', methods=['GET'])
def general_page(path):
    if path.endswith('/'):
        page = get_page(PAGES_DIR, path + 'index')
    else:
        page = get_page(PAGES_DIR, path)

    template = page.meta.get('template', 'general-page.html')
    return render_template(template, page=page)

@app.route('/people/<name>/', methods=['GET'])
@app.route('/people/<name>/<path:path>', methods=['GET'])
def page(name, path=None):
    if path is None:
        path = 'index'

    #print("Incoming path: " + path)
    if path.endswith('/'):
        path = path + 'index'

    user_dir = get_user_dir(name)

    # Personal static folder
    if path.startswith('static/'):
        return send_from_directory(user_dir, path)

    page = get_page(user_dir, path)

    # support redirect
    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect(rd)

    template = page.meta.get('template', 'people-page.html')
    return render_template(template, page=page)




