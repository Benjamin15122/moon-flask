from moon import *
#from models import Site, get_page

from models.site import Site
from models.bundle import Bundle
from models.page import get_page, get_user_dir

from flask import Flask, render_template, redirect, send_from_directory, g, request


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
        decorate_g()

@app.teardown_request
def teardown_request(exception):
    pass

@app.route('/', methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@app.route('/people/<name>/', methods=['GET'])
@app.route('/people/<name>/<path:path>', methods=['GET'])
def page(name=None, path=None):
    if path is None:
        path = 'index'

    #print("Incoming path: " + path)
    if path.endswith('/'):
        path = path + 'index'

    if name:
        user_dir = get_user_dir(name)
        # Personal static folder
        if path.startswith('static/'):
            return send_from_directory(user_dir, path)
        page = get_page(user_dir, path)
    else:
        page = get_page(PAGES_DIR, path)

    # support redirect
    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect(rd)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)

import flask, models

# TODO: redirect
# '/spar/people/wxy/sogr.html': '/spar/peoples/xywu/sogr.html',

@app.route('/spar/', methods=['GET'])
@app.route('/spar/<path:path>', methods=['GET'])
def spar(path = None):
    path = request.path
    if path.endswith('/'): path += 'index.html'
    tokens = path.split('/')

    dir = '/'.join(tokens[:-1])
    fname = tokens[-1]

    if path.endswith('.html'):
        base = PAGES_DIR + dir + '/' + fname[:-5]
        if os.path.exists(base + '.md'):
            page = models.page.get_markdown_page(base + '.md')
        else:
            page = models.page.get_markdown_page(base + '.html')
        return render_template('page.html', page = page)

    return flask.send_file(PAGES_DIR + os.path.sep + path)

