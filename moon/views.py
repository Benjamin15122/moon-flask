from moon import *
from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g
#from flask_flatpages import FlatPages
#from flask_frozen import Freezer
import sys, os, subprocess
import yaml

import codecs

from datetime import datetime, date
from datetime import time as dtime

from string import Template
import markdown

from gitlet import git_update_check
from citation import makeExtension as makeCitationExtension

class Pagination(object):
    ''' A plain object to facilitate add attr as it has __dict__

    '''
    pass

class Page(object):
    ''' A plain object to hold page information instead of using a dict

    '''
    pass

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


def get_date(e):
    ''' A helper method used to sort entries
        No crash but will result in a bad page, e.g., incorrect date
    '''
    return e.get('date', '')

def remove_dead_events(events):
    now = datetime.now();
    return filter(lambda e: now < to_datetime(get_date(e)), events)

@git_update_check(DEADLINES_YAML)
def load_deadlines():
    ''' Load all deadlines, see events/deadlines.yaml

    All deadlines have been sorted manually
    '''
    e = None
    with open(DEADLINES_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(PHD_EVENTS_YAML)
def load_phd_events():
    ''' Load all PhD seminar events, see events/phd.yaml

    All PhD seminar events have been sorted manually
    '''
    e = None
    with open(PHD_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(MASTER_EVENTS_YAML)
def load_master_events():
    ''' Load all Master seminar events, see events/master.yaml

    All Master seminar events have been sorted manually
    '''
    e = None
    with open(MASTER_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(PHOTO_YAML)
def load_photos():
    ''' Load all photos shown in gallery

    '''
    p = None
    with open(PHOTO_YAML, 'r') as f:
        p = yaml.load(f)

    return sorted(p, key=get_date, reverse=True) if p else {}

@git_update_check(NEWS_DIR)
def load_news():
    ''' Load all news and paginations

    Result:
        a tuple of which the first element is the list of news
        and the second element is the Pagination object.
    '''
    n = None

    if not os.path.exists(NEWS_YAML):
        update_news_yaml()

    with open(NEWS_YAML, 'r') as f:
        n = yaml.load(f)
        if not (n and len(n)):
            # TODO raise 404 or 500?
            abort(500)
        n = sorted(n, key=get_date, reverse=True)

    pg = Pagination()
    pg.first = n[0]['page_num']
    pg.last  = n[-1]['page_num']

    return n, pg


def pagination(news_pages):
    ''' Set all news with a page_num

    '''
    num_per_page = 10

    for index, page in enumerate(news_pages):
        page['page_num'] = index / num_per_page + 1 # page number starts from 1

def update_news_yaml():
    ''' Scan news folder and save all news into a single yaml file

    Arguments:
        path: the path of the news in relative to the NEWS_DIR
        title: title in the metadata
        date: date in the metadata
        summary: summary in the metadata
        img_title: a image title should be 90x90 or 150x150 or MMxMM
        img_path: path in relative to the static folder
    '''
    rootdir = NEWS_DIR
    news_pages = []
    for subdir, dirs, files in os.walk(rootdir):
        curdir = os.path.join(rootdir, subdir)
        for f in files:
            f = os.path.join(curdir, f)
            if f.endswith('.md'):
                page = get_markdown_page_or_none(f)
            elif f.endswith('.rst'):
                page = get_restructuredtext_page_or_404(f)
            else:
                continue

            if page is None:
                print("Get page " + str(f) + " failed")
                continue

            pagedict = {}
            pagedict['path'] = os.path.splitext(os.path.relpath(f, rootdir).replace('\\','/'))[0]
            pagedict['title'] = page.meta.get('title', 'Please add a title')
            pagedict['date'] = to_datetime(page.meta.get('date', ''))
            pagedict['summary'] = page.meta.get('summary', 'Please provide a news body')
            pagedict['img_title'] = page.meta.get('img_title')
            pagedict['img_path'] = page.meta.get('img_path')
            # TODO Support news draft
            pagedict['status'] = page.meta.get('status')

            news_pages.append(pagedict)

    news_pages = sorted(news_pages, key=get_date, reverse=True)

    pagination(news_pages)

    news_cache = yaml.safe_dump(news_pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    # news_cache is a utf-8 encoded str object
    # convert it into an unicode object
    with codecs.open(NEWS_YAML, 'w', 'utf-8') as f:
        f.write(news_cache.decode("utf-8"))

@git_update_check(PEOPLE_YAML)
def load_people():
    ''' Load all people
    '''
    p = None
    with open(PEOPLE_YAML) as f:
        p = yaml.load(f)

    return p if p else {}

@git_update_check(EVENTS_YAML)
def load_events():
    '''Load general events,

    Empty now so we need check whether e is None and returning a {} accordingly
    '''
    e = None
    with open(EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return sorted(e, key=get_date, reverse=True) if e else {}

###################

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
        g.md = markdown.Markdown(['markdown.extensions.extra',
            'markdown.extensions.meta',
            makeCitationExtension()])
        install_content_hook()

        # g.photos takes the responsibility to check cache
        g.p = g.photos()

def install_content_hook():
    # photos
    g.photos = load_photos()

    # events
    g.events = load_events()
    g.phd_events = load_phd_events()
    g.deadlines = load_deadlines()
    g.master_events = load_master_events()
    # news
    g.news = load_news()

    # members
    g.members = load_people()


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
    n, pg = g.news()
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
        return render_template('events.html', events=g.events(), deadlines=g.deadlines(), phd=g.phd_events())

    if path == 'deadlines':
        #load_deadlines()
        return render_template('deadlines.html', deadlines=g.deadlines())

    if path == 'phd':
        #load_phd_events()
        return render_template('phd.html', phd=g.phd_events())

    if path == 'master':
        #load_master_events()
        return render_template('master.html', master=g.master_events())

    page = get_page(EVENTS_DIR, path)

    template = page.meta.get('template', 'events-page.html')
    return render_template(template, page=page)

#####################

@app.route('/', methods=['GET'])
def index():
    # remove dead events on index page
    return render_template('index.html', news=g.news()[0], \
            events=g.events(), members=g.members(), \
            deadlines=remove_dead_events(g.deadlines()), \
            phd=remove_dead_events(g.phd_events()), \
            master=remove_dead_events(g.master_events()))

#####################

@app.route('/leadership/', methods=['GET'])
def leadership():
    return render_template('leadership.html')


@app.route('/people/', methods=['GET'])
def people():
    return render_template('people.html', people=g.members())

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


@app.route('/people/<name>/', methods=['GET'])
@app.route('/people/<name>/<path:path>', methods=['GET'])
def page(name, path=None):
    if path is None:
        path = 'index'

    #print("Incoming path: " + path)

    if path == 'cn/':
        path = 'cn/index'

    user_dir = safe_join(PAGES_DIR, name)

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
