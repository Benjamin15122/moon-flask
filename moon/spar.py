import os, flask
from moon import *

@app.route('/spar/', methods = ['GET'])
@app.route('/spar/<path:path>', methods = ['GET'])
def spar_homapge(path = '/'):
    try:
        if path.endswith('/'):
            path += 'index.html'
        if path.split('.')[-1] in ['html']: # HTML may be raw file or a markdown
            md_path = SPAR_DIR + os.path.sep + '.'.join(path.split('.')[:-1] + ['md'])
            if os.path.isfile(md_path):
                with open(md_path, 'r') as fp:
                    content = flask.g.md.convert(fp.read())
                return flask.render_template('spar.html', content = content)
        return flask.send_from_directory(SPAR_DIR, path)
    except Exception, e:
        return str(e)
