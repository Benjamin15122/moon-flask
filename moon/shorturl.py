import flask, yaml
from moon import *

@app.route('/~<name>', methods=['GET'])
@app.route('/~<name>/', methods=['GET'])
def short_url(name):
    mapping = flask.g.site.shorturl
    if name in mapping:
        return flask.redirect(mapping[name])
    else:
        flask.abort(404)

