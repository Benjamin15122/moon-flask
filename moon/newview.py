from moon import *
import markdown, flask, re
from flask import g

class DocTemplate:
    def __init__(self, styles, scripts, extensions):
        self.styles = styles
        self.scripts = scripts
        self.extensions = extensions

# TODO: use classes to hold extensions
EXTENSIONS = {
    'math': 'moon.md.math:ArithmatexExtension',
    'spar': 'moon.md.spar:SparExtension',
    'fencedcode': 'moon.md.fencedcode:MoonFencedCodeExtension',
}

def render_markdown(md_path):
    with open(md_path, 'r') as fp:
        md_data = fp.read().decode('utf-8')

    # First pass to get md.Meta
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    md.convert(md_data)
    meta = md.Meta

    # Second (full) pass with all extensions
    extensions = [ 'markdown.extensions.extra', 'markdown.extensions.toc', 'markdown.extensions.meta'] + \
        [ EXTENSIONS[ext] for ext in meta.get('extensions', []) ]

    md = markdown.Markdown(extensions = extensions)
    templated = flask.render_template_string(md_data)
    rendered = md.convert(templated)

    return flask.render_template('doc.html', 
        content = rendered,
        title = ''.join(meta.get('title', ['']))
    )

def render_html(html_path):
    with open(html_path, 'r') as fp:
        data = fp.read().decode('utf-8')

    return flask.render_template('doc.html', content = data)


# TODO: we'd move this out of here.

REDIRECTS = {
    '/spar/people/wxy/sogr.html': '/spar/peoples/xywu/sogr.html',
}

def view(path):
    if path in REDIRECTS:
        return flask.redirect(REDIRECTS[path])

    if path.endswith('.html'):
        base = MOON_DIR + os.path.sep + path[:-5]
        if os.path.exists(base + '.md'):
            return render_markdown(base + '.md')
        elif os.path.exists(base + '.html'):
            return render_html(base + '.html')
        flask.abort(404)

    return flask.send_file(MOON_DIR + os.path.sep + path)

@app.route('/spar/')
@app.route('/spar/<path:path>', methods=['GET'])
def spar(path = None):
    path = flask.request.path
    if path.endswith('/'): path += 'index.html'
    return view(path)
