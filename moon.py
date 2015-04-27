from flask import Flask, render_template, redirect, send_from_directory, request, abort, make_response
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import sys, os, subprocess
import yaml

#import ConfigParser

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

FLATPAGES_MARKDOWN_EXTENSIONS = []

MOON_GIT_URL = 'git@git.artemisprojects.org:moon.git'
MOON_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES_DIR = MOON_DIR + os.path.sep + 'pages'
PEOPLE_YAML = PAGES_DIR + os.path.sep + 'people.yaml'

GITSUBMODULES = MOON_DIR + os.path.sep + '.gitsubmodules'

GIT_CMD = 'git'

GIT_PULL_MOON = [GIT_CMD, '-C', MOON_DIR, 'pull', 'origin', 'master']
GIT_INIT_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'init']
GIT_UPDATE_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'update']
GIT_PULL_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'foreach', 'git', 'pull', 'origin', 'master']

app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

def refresh_moon():
    ret_code = subprocess.call(GIT_PULL_MOON)
    print('execute "%s" with ret %d' % (' '.join(GIT_PULL_MOON), ret_code))

    ret_code = subprocess.call(GIT_INIT_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_INIT_SUBMODULES), ret_code))

    ret_code = subprocess.call(GIT_UPDATE_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_UPDATE_SUBMODULES), ret_code))

    ret_code = subprocess.call(GIT_PULL_SUBMODULES)
    print('execute "%s" with ret %d' % (' '.join(GIT_PULL_SUBMODULES), ret_code))



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

        

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

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

    page_path = name + '/' + path


    if path.startswith('static/'):
        return send_from_directory('pages/' + name, path)

    page = flatpages.get_or_404(page_path)

    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect(rd)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(host='0.0.0.0', port=8000)
