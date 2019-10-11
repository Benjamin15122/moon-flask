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

@app.errorhandler(500)
def page_not_found(e):
    '''Custom 500 page

    '''
    if not hasattr(g, 'site'):
        decorate_g()
    return render_template('500.html', description=e.description), 500



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

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return redirect('/static/img/favicon.png')

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

