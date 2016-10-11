from moon import *
import markdown, flask, re

class DocTemplate:
    def __init__(self, styles, scripts, extensions):
        self.styles = styles
        self.scripts = scripts
        self.extensions = extensions

# TODO: maybe we should put these information in another place

DOC_TEMPLATES = {
    'base': DocTemplate(
        styles = [
            '/static/font-awesome/css/font-awesome.min.css',
            '/static/js/dropdown-menu/dropdown-menu.css',
            '/static/bootstrap/css/bootstrap.min.css',
            '/static/css/style.css',
            '/static/css/moon.css',
            '/static/css/bibtex.css',
        ],
        scripts = [
            '/static/jQuery/jquery-2.1.1.min.js',
            '/static/jQuery/jquery-migrate-1.2.1.min.js',
            '/static/bootstrap/js/bootstrap.min.js',
            '/static/js/dropdown-menu/dropdown-menu.js',
            '/static/js/theme.js',
        ],
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.toc',
            'markdown.extensions.meta',
        ]),
    }

EXTENSIONS = {
    'math': ('moon.md.math:ArithmatexExtension',
              ['/static/katex/katex.min.css'],
              ['/static/katex/katex.min.js', '/static/katex/render.js']),
    'spar': ('moon.md.spar:SparExtension', [], []),
}

def render_markdown(md_path):
    with open(md_path, 'r') as fp:
        md_data = fp.read().decode('utf-8')

    # First pass to get md.Meta
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    md.convert(md_data)
    meta = md.Meta

    # Second (full) pass with all extensions
    template = DOC_TEMPLATES['base']

    styles = template.styles
    scripts = template.scripts
    extensions = template.extensions

    for ext in meta.get('extensions', []):
        (name, style, script) = EXTENSIONS[ext]
        extensions.append(name)
        styles += style
        scripts += script

    def dedup(xs):
        (S, ys) = (set(), [])
        for x in xs:
            if x not in S: ys.append(x)
            S.add(x)
        return ys

    (styles, scripts, extensions) = (dedup(styles), dedup(scripts), dedup(extensions))
    md = markdown.Markdown(extensions = extensions)

    templated = flask.render_template_string(md_data)
    rendered = md.convert(templated)

    args = {
        'content': rendered,
        'title': ''.join(meta.get('title', [''])),
        'styles': styles,
        'scripts': scripts,
    }
    for key in meta:
        if key not in args: args[key] = meta[key]
    return flask.render_template('doc.html', **args)

def render_html(html_path):
    with open(html_path, 'r') as fp:
        data = fp.read().decode('utf-8')

    return flask.render_template('doc.html', content = data)

def view(root_dir, path):
    if path.endswith('.html'):
        base = flask.safe_join(root_dir, path[:-5])
        if os.path.exists(base + '.md'):
            return render_markdown(base + '.md')
        elif os.path.exists(base + '.html'):
            return render_html(base + '.html')
        flask.abort(404)

    return flask.send_from_directory(root_dir, path)

@app.route('/spar/')
@app.route('/spar/<path:path>', methods=['GET'])
def spar(path = 'index.html'):
    return view(SPAR_DIR, path)
