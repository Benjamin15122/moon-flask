from moon import *
from models import Site, get_page

from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g, render_template_string
#from flask_flatpages import FlatPages
#from flask_frozen import Freezer
import sys, os, subprocess

from datetime import datetime
from utils import to_date, to_time, to_datetime



import markdown

from citation import makeExtension as makeCitationExtension
from citation import Citations, render_bib_entry, makeJinjaBlockPattern

#################

def refresh_moon():
    ''' Refresh the code repository

    '''
    ret_code = subprocess.call(GIT_PULL_MOON)
    print('execute "%s" with ret %d' % (' '.join(GIT_PULL_MOON), ret_code))

    ret_code = subprocess.call(GIT_INIT_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_INIT_SUBMODULES), ret_code))

    ret_code = subprocess.call(GIT_UPDATE_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_UPDATE_SUBMODULES), ret_code))

    ret_code = subprocess.call(GIT_PULL_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_PULL_SUBMODULES), ret_code))

    os.remove(NEWS_YAML)

##################


@app.route('/gitlabwebhooks', methods=['POST'])
def gitlab_webhooks():
    ''' Gitlab webhooks

    '''
    data = request.get_json()

    try:
        refresh_moon()
    except Exception:
        abort(500)

    return make_response("", 200)


###################



def remove_dead_events(events):
    now = datetime.now();
    return filter(lambda e: now < to_datetime(e.get('date', '')), events)


def create_markdown():
    md = markdown.Markdown(['markdown.extensions.extra',
            'markdown.extensions.meta',
            makeCitationExtension()])

    #md.inlinePatterns.add('jinja block pattern', JinjaBlockPattern(JINJA_BLOCK_RE, md), ">backtick") # after backtick

    makeJinjaBlockPattern(md)

    return md

##################

@app.errorhandler(404)
def page_not_found(e):
    '''Custom 404 page

    '''
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
        g.site = Site()

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
    n, pg = g.site.news
    pg.current = page_num

    return render_template('news.html', news=n, pg=pg)

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
    return render_template('index.html', news=g.site.news[0], \
            events=g.site.events, members=g.site.people, \
            deadlines=remove_dead_events(g.site.deadlines), \
            phd=remove_dead_events(g.site.phd_events), \
            master=remove_dead_events(g.site.master_events))

#####################

@app.route('/leadership/', methods=['GET'])
def leadership():
    return render_template('leadership.html')


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
def dse():
    page = get_page(DSE_DIR, 'index')
    template = page.meta.get('template', 'people-page.html')
    return render_template(template, page=page)

def get_user_dir(name):
    user_dir = safe_join(PAGES_DIR, name)

    # pages in the 'share' folder can be either
    # accessed by /people/share/haosun/ or /people/haosun/
    if not os.path.exists(user_dir):
        user_dir = safe_join(PAGES_SHARE_DIR, name)

    return user_dir

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


##########################

@app.context_processor
def bib_processor():

    def render_bib_file(path=None, keys=None, hl=''):
        if not path:
            return g.site.paper.render_all(hl)

        if request.endpoint == 'page':
            name = request.view_args['name']

            user_dir = get_user_dir(name)
            bibfile = safe_join(user_dir, path)
        else:
            bibfile = safe_join(MOON_DIR, path)


        try:
            c = Citations(bibfile)

            if not keys:
                return c.render_all(hl)
            elif isinstance(keys, str):
                return c.render_entry(keys, hl)
            else:
                return c.render_entries(keys, hl)
        except Exception as e:
            return "<em>render path=%s, keys=%s, hl=%s failed! </em>" % (path, keys, hl)

        return "<em>No such bib file " + path + "</em>"

    return dict(render_bib_file=render_bib_file, render_bib_entry=render_bib_entry)


##############################################

