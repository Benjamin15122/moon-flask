import os, flask, markdown
from moon import *

from citation import makeJinjaBlockPattern

from arithmatex import ArithmatexExtension

@app.route('/spar/', methods = ['GET'])
@app.route('/spar/<path:path>', methods = ['GET'])
def spar(path = '/'):
    try:
        if path == 'kwiki':
            path += '/index.html'
        if path.endswith('/'):
            path += 'index.html'
        if path.split('.')[-1] in ['html']: # HTML may be raw file or a markdown
            md_path = SPAR_DIR + os.path.sep + '.'.join(path.split('.')[:-1] + ['md'])
            if os.path.isfile(md_path):
                kwiki = path.startswith('kwiki/')
                template = 'wiki.html' if kwiki else 'spar.html'

                with open(md_path, 'r') as fp:
                    extensions = ['markdown.extensions.extra',
                         'markdown.extensions.meta',
                         'markdown.extensions.toc',]

                    if kwiki:
                        extensions.append(ArithmatexExtension())

                    md = markdown.Markdown(extensions = extensions)

                    makeJinjaBlockPattern(md)

                    content = md.convert(fp.read().decode('utf-8'))

                    meta = md.Meta
                    title = ''.join( meta.get('title', ['']) )
                return flask.render_template(template, content = content, title = title, nofooter = True)
        return flask.send_from_directory(SPAR_DIR, path)
    except Exception, e:
        return str(e)

