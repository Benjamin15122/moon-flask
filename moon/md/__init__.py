import markdown
from moon.md import jinja2, fencedcode

def create_markdown():
    md = markdown.Markdown(extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.meta',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            fencedcode.makeExtension()],
            extension_configs= {
                'markdown.extensions.codehilite' : {
                        'linenums' : True
                    }
                })

    jinja2.makeJinjaExpressionPattern(md)
    return md


