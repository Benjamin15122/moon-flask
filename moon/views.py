from moon import *
from models import Page, Site

from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g, render_template_string
#from flask_flatpages import FlatPages
#from flask_frozen import Freezer
import sys, os, subprocess
import yaml

import codecs

from datetime import datetime, date
from datetime import time as dtime

from string import Template
import markdown

from citation import makeExtension as makeCitationExtension
from citation import Citations, render_bib_entry

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


@app.template_filter('to_date')
def to_date(st):
    if isinstance(st, datetime):
        return st.strftime("%b %d, %Y")

    if isinstance(st, unicode):
        st = str(st)

    return to_datetime(st).strftime("%b %d, %Y")

@app.template_filter('to_time')
def to_time(st):
    if isinstance(st, datetime):
        return st.strftime("%H:%M")

    if isinstance(st, unicode):
        st = str(st)

    return to_datetime(st).strftime("%H:%M")

app.jinja_env.filters['to_date'] = to_date
app.jinja_env.filters['to_time'] = to_time


def to_datetime(d):
    '''
        convert everything to datetime
    '''
    if isinstance(d, date):
        return datetime.combine(d, dtime(0, 0))

    if isinstance(d, datetime):
        return d

    if d is None:
        return datetime.now();

    if d == '':
        return datetime.now();

    dt = None
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except Exception as e:
        print("Not the %Y-%m-%d " + str(e)) # 2012-02-01
        print(type(d))

    try:
        return datetime.strptime(d, "%Y-%m")
    except Exception as e:
        print("Not the %Y-%m " + str(e)) # 2012-02
        print(type(d))

    try:
        return datetime.strptime(d, "%Y-%m-%d %H:%M")
    except Exception as e:
        print("Not the %Y-%m-%d %H:%M" + str(e)) # 2012-02-01 19:00
        print(type(d))

    return datetime.now()



def remove_dead_events(events):
    now = datetime.now();
    return filter(lambda e: now < to_datetime(e.get('date', '')), events)


def create_markdown():
    md = markdown.Markdown(['markdown.extensions.extra',
            'markdown.extensions.meta',
            makeCitationExtension()])

    md.inlinePatterns.add('jinja block pattern', JinjaBlockPattern(JINJA_BLOCK_RE, md), ">backtick") # after backtick

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

def get_page(page_dir, path):
    page_path = None

    # 1) Test markdown
    try:
        md_path = safe_join(page_dir, path + '.md')
        if os.path.exists(md_path):
            page_path = md_path
    except Exception as e:
        print(e)
        print("Cannot find md path for " + path)

    if page_path:
        return get_markdown_page_or_404(page_path)

    # 2) Test reStructuredText
    try:
        rst_path = safe_join(page_dir, path + '.rst')
        if os.path.exists(rst_path):
            page_path = rst_path
    except Exception as e:
        print(e)
        print("Cannot find rst path for " + path)


    if page_path:
        return get_restructuredtext_page_or_404(page_path)

    # 3) Test yaml
    try:
        yaml_path = safe_join(page_dir, path + '.yaml')
        if os.path.exists(yaml_path):
            page_path = rst_path
    except Exception as e:
        print(e)
        print("Cannot find rst path for " + path)


    # 4) Test html
    # TODO Extract the body
    abort(404)

def get_restructuredtext_page_or_404(page_path):
    ''' Deprecated

    '''
    page = Page()

    with open(page_path, 'r') as f:
        parts = publish_parts(f.read().decode('utf-8'), writer_name='html')

        page.html = parts['html_body']
        page.meta = {} # test
        page.meta['title'] = parts['title']
        return page

    abort(404)

def get_markdown_page_or_none(page_path):
    try:
        return get_markdown_page(page_path)
    except Exception as e:
        print(e)
        return None

def get_markdown_page(page_path):
    page = Page()
    with open(page_path, 'r') as f:
        #if not hasattr(g, 'md'):
        #    g.md = markdown.Markdown(['markdown.extensions.extra', 'markdown.extensions.meta'])

        page.html = g.md.convert(f.read().decode('utf-8'))
        page.meta = g.md.Meta # flask-pages naming covention
        for key, value in page.meta.iteritems():
            page.meta[key] = ''.join(value) # meta is a list
        return page

    abort(404)

def get_markdown_page_or_404(page_path):
    try:
        return get_markdown_page(page_path)
    except Exception as e:
        print(e)
        abort(404)

    abort(404)


##########################

@app.context_processor
def bib_processor():

    def render_bib_file(path=None, keys=None, hl=''):
        if not path:
            return g.site.paper.render_all(hl)

        if request.endpoint == 'page':
            name = request.view_args['name']

            user_dir = get_user_dir(name)
            print(user_dir)
            bibfile = safe_join(user_dir, path)
        else:
            bibfile = safe_join(MOON_DIR, path)

        print(bibfile)

        try:
            c = Citations(bibfile)

            if not keys:
                return c.render_all(hl)
            elif isinstance(keys, str):
                return c.render_entry(keys, hl)
            else:
                return c.render_entries(keys, hl)

        except:
            pass

        return "<em>No such bib file " + path + "</em>"

    return dict(render_bib_file=render_bib_file, render_bib_entry=render_bib_entry)


##############################################

from markdown.inlinepatterns import Pattern
from markdown.util import etree

import re

JINJA_BLOCK_RE = r'({{[^{}]*}})'


class JinjaBlockPattern(Pattern):

    def __init__(self, pattern, md):
        Pattern.__init__(self, pattern, md)

    def handleMatch(self, m):
        jinja_block = m.group(2)

        try:
            # render returns a unicode object, encode it into a utf-8 string
            html = render_template_string(m.group(2)).encode('utf-8')
        except:
            return etree.fromstring('<em>' + m.group(2) + '</em>')

        try:
            return etree.fromstring(html)
        except:
            pass

        try:
            return etree.fromstring('<jinja>' + html + '</jinja>')
        except:
            pass

