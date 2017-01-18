from moon import *
from .models.site import Site
from .models.bundle import Bundle
from .models.page import get_page, get_user_dir, get_markdown_page

from flask import Flask, render_template, redirect, send_file, send_from_directory, g, request, abort, url_for, safe_join

import os

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

# TODO: handle redirect
# '/spar/people/wxy/sogr.html': '/spar/peoples/xywu/sogr.html',

def spar():
    fullpath = request.path

    # TODO: this code barely works, but should not be like this.
    if fullpath == '/': fullpath = '/index'
    elif fullpath.endswith('/'): fullpath += 'index.html'
    tokens = fullpath.split('/')
    dir = os.path.sep.join(tokens[:-1])
    fname = tokens[-1]

    base = PAGES_DIR + os.path.sep + fullpath

    if fullpath.endswith('.html'):
        base = PAGES_DIR + dir + os.path.sep + fname[:-5]
        if os.path.exists(base + '.md'):
            content = get_markdown_page(base + '.md')
        else:
            content = get_markdown_page(base + '.html')
        return render_template('page.html', page = content)
    elif os.path.exists(base):
        return send_file(PAGES_DIR + os.path.sep + fullpath)

def check_static(folder, path):
    try:
        localpath = safe_join(folder, path)
        if os.path.exists(localpath):
            if os.path.isfile(localpath):
                return localpath
    except:
        # not handle here
        return None
    else:
        return None

@app.route('/', methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
@app.route('/people/<name>/', methods=['GET'])
@app.route('/people/<name>/<path:path>', methods=['GET'])
def page(name = None, path = None):
    if path is None:
        path = 'index'
    #elif name is None and path.startswith('spar/'):
    #    return spar()
    elif path.endswith('/'):
        path += 'index'

    if name:
        root_dir = get_user_dir(name)
    else:
        root_dir = PAGES_DIR

    localpath = check_static(root_dir, path)
    if localpath:
        return send_file(localpath)

    page = get_page(root_dir, path)

    # support redirect
    rd = page.meta.get('redirect')
    if rd is not None:
        return redirect_url(rd)

    template = page.meta.get('template', 'page.html')
    return render_template(template, page = page)

def redirect_url(url):
    if url is None:
        abort(404)

    if isinstance(url, unicode):
        url = url.encode('utf8')

    # absolute path with domain
    if url.startswith('http://') or url.startswith('https://'):
        return redirect(url)

    # absolute path without domain
    if url.startswith('/'):
        return redirect(url_for('page', path=url[1:]))

    # relative path (w.r.t. request.path)
    base_path = os.path.dirname(request.path)
    return redirect_url(base_path + '/' + url)

