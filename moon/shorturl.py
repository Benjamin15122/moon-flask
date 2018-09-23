import flask, yaml
from moon import *
import views

@app.route('/~<name>', methods=['GET'], defaults={'path': None})
@app.route('/~<name>/', methods=['GET'], defaults={'path': None})
@app.route('/~<name>/<path:path>', methods=['GET'])
def short_url(name, path):
    mapping = flask.g.site.shorturl
    if name in mapping:
        dest = mapping[name]
        if dest.startswith('people/'):
            uname = dest.split('/')[1]
            return views.page(name=uname, path=path)
        else:
            return flask.redirect(dest)
    else:
        flask.abort(404)

