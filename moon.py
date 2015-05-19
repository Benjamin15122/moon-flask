from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g
#from flask_flatpages import FlatPages
#from flask_frozen import Freezer
import sys, os, subprocess, time
import yaml

import codecs

from datetime import datetime

from string import Template
import markdown
from docutils.core import publish_string, publish_parts

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

#import ConfigParser

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

FLATPAGES_MARKDOWN_EXTENSIONS = []

MOON_GIT_URL = 'git@git.artemisprojects.org:moon.git'
MOON_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES_DIR = MOON_DIR + os.path.sep + 'pages'
NEWS_DIR = PAGES_DIR + os.path.sep + 'news'
EVENTS_DIR = PAGES_DIR + os.path.sep + 'events'

PEOPLE_YAML = PAGES_DIR + os.path.sep + 'people.yaml'
PHOTO_YAML  = PAGES_DIR + os.path.sep + 'photo.yaml'
NEWS_YAML   = NEWS_DIR + os.path.sep + 'news.yaml'
EVENTS_YAML = EVENTS_DIR + os.path.sep + 'events.yaml'

GITSUBMODULES = MOON_DIR + os.path.sep + '.gitsubmodules'

GIT_CMD = 'git'

GIT_PULL_MOON = [GIT_CMD, '-C', MOON_DIR, 'pull', 'origin', 'master']
GIT_INIT_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'init']
GIT_UPDATE_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'update']
GIT_PULL_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'foreach', 'git', 'pull', 'origin', 'master']

app = Flask(__name__)
app.config.from_object(__name__)

################

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives

def convert_bibtex(bibtex, hl):
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    try:
        bib_database = bibtexparser.loads(bibtex, parser=parser)
    except:
        return bibtex

    return convert_bibentries_to_html(bib_database.entries)

ip_temp = Template('<li><a name="$id"></a><b>$title</b>,$author,<em>$booktitle</em>,$pages,$month $year</li>')

def render_interproceedings(e):
    if 'month' not in e:
        e['month'] = ''
    return ip_temp.substitute(e)

def render_article(e):
    pass

def isEntry(e, t):
    return e.get('type') == t

def convert_bibentries_to_html(entries):
    html = []
    html.append('<ol>')
    for e in entries:
        if isEntry(e, 'inproceedings'):
            html.append(render_interproceedings(e))
        elif isEntry(e, 'article'):
            html.append(render_article(e))
        else:
            html.append(' '.join(e.values()))

    html.append('</ol>')

    return '\n'.join(html)

class BibtexDirective(rst.Directive):

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'hl': directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        b = convert_bibtex(text, self.options.get('hl', ''))
        n = nodes.raw(rawsource=self.block_text, text=b, format='html')
        return [n]

directives.register_directive('bibtex', BibtexDirective)

################

class Pagination(object):
    pass

class Page(object):
    pass

#################

def refresh_moon():
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

    return parse_date(st).strftime("%b %d, %Y")

@app.template_filter('to_time')
def to_time(st):
    if isinstance(st, datetime):
        return st.strftime("%H:%M")

    if isinstance(st, unicode):
        st = str(st)

    return parse_date(st).strftime("%H:%M")

app.jinja_env.filters['to_date'] = to_date
app.jinja_env.filters['to_time'] = to_time


def parse_date(d):
    dt = None
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except Exception as e:
        print("Not the %Y-%m-%d" + str(e))
        print(type(d))

    try:
        return datetime.strptime(d, "%Y-%m")
    except Exception as e:
        print(e)

    try:
        return datetime.strptime(d, "%Y-%m-%d %H:%M")
    except Exception as e:
        print(e)

    return datetime.now()

def get_date(e):
    return e.get('date', '')

def load_photos():
    p = {}
    with open(PHOTO_YAML, 'r') as f:
        p = yaml.load(f)
        p = sorted(p, key=get_date, reverse=True)

    return p

def load_news():
    n = {}

    if not os.path.exists(NEWS_YAML):
        update_news_yaml()

    with open(NEWS_YAML, 'r') as f:
        n = yaml.load(f)
        n = sorted(n, key=get_date, reverse=True)

    pg = Pagination()
    pg.first = n[0]['page_num']
    pg.last  = n[-1]['page_num']

    return n, pg

def pagination(news_pages):

    num_per_page = 10

    for index, page in enumerate(news_pages):
        page['page_num'] = index / num_per_page + 1 # page number starts from 1

def update_news_yaml():
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
            pagedict['date'] = parse_date(page.meta.get('date', ''))
            pagedict['summary'] = page.meta.get('summary', 'Please provide a news body')
            pagedict['img_title'] = page.meta.get('img_title')
            pagedict['img_path'] = page.meta.get('img_path')
            # TODO Support news draft
            pagedict['status'] = page.meta.get('status')

            news_pages.append(pagedict)

    news_pages = sorted(news_pages, key=get_date, reverse=True)

    pagination(news_pages)

    news_cache = yaml.safe_dump(news_pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    with codecs.open(NEWS_YAML, 'w', 'utf-8') as f:
        f.write(news_cache)

def load_people():
    with open(PEOPLE_YAML) as f:
        return yaml.load(f)


def load_events():
    e = {}
    with open(EVENTS_YAML, 'r') as f:
        e = yaml.load(f)
        e = sorted(e, key=get_date, reverse=True)

    return e

###################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    md = getattr(g, 'md', None)
    if md is None:
        g.md = markdown.Markdown(['markdown.extensions.extra', 'markdown.extensions.meta'])

    g.p = load_photos()


@app.teardown_request
def teardown_request(exception):
    pass


#####################

@app.route('/news/', methods=['GET'])
@app.route('/news/<int:page_num>', methods=['GET'])
def news(page_num=None):
    if page_num is None:
        page_num = 1

    n, pg = load_news()
    pg.current = page_num

    return render_template('news.html', news=n, pg=pg)

@app.route('/news/page/<path:path>', methods=['GET'])
def news_page(path):
    page = get_page(NEWS_DIR, path)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)


#####################

@app.route('/events/', methods=['GET'])
@app.route('/events/<path:path>', methods=['GET'])
def events(path=None):
    if path is None:
        return render_template('events.html')

    page = get_page(EVENTS_DIR, path)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)

#####################

@app.route('/', methods=['GET'])
def index():

    n,pg = load_news()
    e = load_events()
    m = load_people()

    return render_template('index.html', news=n, events=e, members=m)

#####################

@app.route('/people/', methods=['GET'])
def people():
    with open(PEOPLE_YAML) as f:
        people = yaml.load(f)
    return render_template('people.html', people=people)

@app.route('/awards/', methods=['GET'])
def awards():
    return render_template('awards.html')

@app.route('/contact/', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/research/', methods=['GET'])
def research():
    return render_template('research.html')

@app.route('/people/<name>/', methods=['GET'])
@app.route('/people/<name>/<path:path>', methods=['GET'])
def page(name, path=None):
    if path is None:
        path = 'index'

    print("Incoming path: " + path)

    if path == 'cn/':
        path = 'cn/index'

    user_dir = safe_join(PAGES_DIR, name)

    if path.startswith('static/'):
        return send_from_directory(user_dir, path)

    page = get_page(user_dir, path)

    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect(rd)

    template = page.meta.get('template', 'page.html')
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
    page = Page()

    with open(page_path, 'r') as f:
        parts = publish_parts(f.read(), writer_name='html')

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
        if not hasattr(g, 'md'):
            g.md = markdown.Markdown(['markdown.extensions.extra', 'markdown.extensions.meta'])

        page.html = g.md.convert(f.read())
        page.meta = g.md.Meta # flask-pages naming covention
        for key, value in page.meta.iteritems():
            page.meta[key] = ''.join(value)
        return page

    abort(404)

def get_markdown_page_or_404(page_path):
    try:
        return get_markdown_page(page_path)
    except Exception as e:
        print(e)
        abort(404)

    abort(404)

reload(sys)
sys.setdefaultencoding('utf-8') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
