import flask, yaml
from moon import *

@app.route('/~<name>', methods=['GET'])
def short_url(name, path = None):
    with open(SHORTURL_YAML, 'r') as fp:
        d = yaml.load(fp)
        print d
        if name in d:
            return flask.redirect(d[name])
        else:
            return flask.redirect('/')
    return '404'
