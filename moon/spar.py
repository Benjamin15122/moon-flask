import os, flask, markdown
from moon import *

from citation import makeJinjaBlockPattern

@app.route('/spar/', methods = ['GET'])
@app.route('/spar/<path:path>', methods = ['GET'])
def spar_homepage(path = '/'):
    try:
        if path.endswith('/'):
            path += 'index.html'
        if path.split('.')[-1] in ['html']: # HTML may be raw file or a markdown
            md_path = SPAR_DIR + os.path.sep + '.'.join(path.split('.')[:-1] + ['md'])
            if os.path.isfile(md_path):
                with open(md_path, 'r') as fp:
                    md = markdown.Markdown(extensions = 
                        ['markdown.extensions.extra',
                         'markdown.extensions.meta',
                         'markdown.extensions.toc',]
                    )

                    makeJinjaBlockPattern(md)

                    content = md.convert(fp.read().decode('utf-8'))
                    meta = md.Meta
                    title = ''.join( meta.get('title', ['']) )
                return flask.render_template('spar.html', content = content, title = title)
        return flask.send_from_directory(SPAR_DIR, path)
    except Exception, e:
        return str(e)
