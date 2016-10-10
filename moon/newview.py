from moon import *
import markdown, flask

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
    'latex': ('moon.extensions.latex:ArithmatexExtension',
              ['/static/katex/katex.min.css'],
              ['/static/katex/katex.min.js', '/static/katex/render.js']),
    'index': ('moon.extensions.index:IndexPageExtension', [], []),
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

            
    return flask.render_template(
        'doc.html',
        content = md.convert(md_data),
        title = ''.join(meta.get('title', [''])),
        styles = styles,
        scripts = scripts,
    )

@app.route('/new/', methods=['GET'])
@app.route('/new/<path:path>', methods=['GET'])
def view(path = 'index.html'):
    doc_path = os.path.join(DOC_ROOT, path)

    if doc_path.endswith('.html'):
        md_path = doc_path[:-4] + 'md'
        return render_markdown(md_path)

    return 'Not supported.'
