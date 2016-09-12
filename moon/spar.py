import os, flask, markdown
from moon import *

from citation import makeJinjaBlockPattern
from spar_ext import ArithmatexExtension, SparPeople

def render_markdown(path, md_path):
    kwiki = path.startswith('kwiki/')  # is this page belong to KWiki?
    index = (path == '/') # is this page the index page?

    with open(md_path, 'r') as fp:
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.meta',
            'markdown.extensions.toc',
        ]

        if kwiki:
            extensions += [
                ArithmatexExtension(),
            ]
            
        raw = fp.read().decode('utf-8')
        if index: raw += SparPeople() # TODO: replace it with a plugin

        md = markdown.Markdown(extensions = extensions)
        makeJinjaBlockPattern(md) # render bibtex; TODO: refactor code to have meaningful names

    return flask.render_template(
        'wiki.html' if kwiki else 'spar.html',  # template
        content = md.convert(raw), # contents
        title = ''.join(md.Meta.get('title', [''])), # title
        nofooter = True
    )


@app.route('/spar/', methods = ['GET'])
@app.route('/spar/<path:path>', methods = ['GET'])
def spar(path = '/'):
    if path.endswith('/') and os.path.isdir(SPAR_DIR + os.path.sep + path):
        return render_markdown(path, SPAR_DIR + os.path.sep + path + '/index.md')

    if path.split('.')[-1] in ['html']:
        # test whether the page should be rendered from a markdown file
        md_path = SPAR_DIR + os.path.sep + '.'.join(path.split('.')[:-1]) + '.md'
        if os.path.isfile(md_path):
            return render_markdown(path, md_path)

    # otherwise sends the raw data
    return flask.send_from_directory(SPAR_DIR, path)

