from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response, safe_join, Markup, abort, g
#from flask_flatpages import FlatPages
#from flask_frozen import Freezer
import sys, os, subprocess
import yaml

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
PEOPLE_YAML = PAGES_DIR + os.path.sep + 'people.yaml'
PEOPLE_BIO = 'people_bio'

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
    bib_database = bibtexparser.loads(bibtex, parser=parser)
    print(bib_database.entries)

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
        print(getattr(e, 'type', '') == 'inproceedings')
        print(getattr(e, 'type', ''))
        print(e['type'])
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
        print(b)
        return [n]


directives.register_directive('bibtex', BibtexDirective)

################


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

##################


@app.route('/gitlabwebhooks', methods=['POST'])
def gitlab_webhooks():
    data = request.get_json()

    #TODO no 'object type' in current gitlab request
    #try:
    #    if data['object_type'] != 'push':
    #        print('gitlab webhooks: object type is ' + data['object_type'])
    #        abort(500)
    #except Exception:
    #    print('gitlab webhooks: json is ' + str(data))
    #    abort(404)

    try:
        refresh_moon()
    except Exception:
        abort(500)

    return make_response("", 200)

    #repo_url = data['repository']['url']

    #if repo_url == MOON_GIT_URL:
    #    refresh_moon()

    #config = ConfigParser.ConfigParser()

    #with open(GITSUBMODULES) as f:
    #    config.readfp(open("rb"))

    #for sec in config.sections():
    #    if config.get(sec, 'url') == repo_url:
    #        refresh_moon()

###################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.before_request
def before_request():
    md = getattr(g, 'md', None)
    if md is None:
        g.md = markdown.Markdown(['markdown.extensions.extra', 'markdown.extensions.meta'])

@app.teardown_request
def teardown_request(exception):
    pass


#####################

@app.route('/news/', methods=['GET'])
@app.route('/news/<path:path>', methods=['GET'])
def news(path=None):
    return render_template('news.html')

#####################

@app.route('/events/', methods=['GET'])
@app.route('/events/<path:path>', methods=['GET'])
def events(path=None):
    return render_template('events.html')

#####################

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#####################

@app.route('/people/', methods=['GET'])
def people():
    with open(PEOPLE_YAML) as f:
        people = yaml.load(f)
    return render_template('people.html', people=people)

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

    page = get_user_page(user_dir, path)

    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect(rd)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)

def get_user_page(user_dir, path):
    print(path)
    page_path = None

    # 1) Test markdown
    try:
        md_path = safe_join(user_dir, path + '.md')
        if os.path.exists(md_path):
            page_path = md_path
    except Exception as e:
        print(e)
        print("Cannot find md path for " + path)

    if page_path:
        return get_markdown_page_or_404(page_path)

    # 2) Test reStructuredText
    try:
        rst_path = safe_join(user_dir, path + '.rst')
        if os.path.exists(rst_path):
            page_path = rst_path
    except Exception as e:
        print(e)
        print("Cannot find rst path for " + path)

    print(page_path)

    if page_path:
        return get_restructuredtext_page_or_404(page_path)

    # 3) Test yaml
    try:
        yaml_path = safe_join(user_dir, path + '.yaml')
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
        page.html = publish_parts(f.read(), writer_name='html')['html_body']
        page.meta = {} # test
        return page

    abort(404)



def get_markdown_page_or_404(page_path):
    page = Page()
    with open(page_path, 'r') as f:
        try:
            page.html = g.md.convert(f.read())
            page.meta = g.md.Meta # flask-pages naming covention
            return page
        except:
            abort(404)

    abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
