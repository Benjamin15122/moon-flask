from flask import Flask, render_template, redirect, send_from_directory
from flask_flatpages import FlatPages
from flask_frozen import Freezer
import sys, os
import yaml

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

FLATPAGES_MARKDOWN_EXTENSIONS = []

MOON_DIR = os.path.dirname(os.path.abspath(__file__))

PAGES_DIR = MOON_DIR + os.path.sep + "pages"
PEOPLE_YAML = PAGES_DIR + os.path.sep + "people.yaml"


app = Flask(__name__)
app.config.from_object(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/people.html')
def people():
    with open(PEOPLE_YAML) as f:
        people = yaml.load(f)

    return render_template('people.html', people=people)

@app.route('/research.html')
def research():
    return render_template('research.html')

@app.route('/people/<name>/')
@app.route('/people/<name>/<path:path>')
def page(name, path=None):
    if path is None:
        path = 'index'
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
        app.run(port=8000)
