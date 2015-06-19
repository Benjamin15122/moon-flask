import flask
from moon import app

@app.route('/spar/', methods = ['GET'])
@app.route('/spar/<path:path>', methods = ['GET'])
def spar_homapge(path = ''):
    return flask.render_template('spar.html')
