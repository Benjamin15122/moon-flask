import flask, yaml
from moon import *

@app.route('/~<name>', methods=['GET'])
def short_url(name):
    # TODO: use new site model
    flask.abort(404)

