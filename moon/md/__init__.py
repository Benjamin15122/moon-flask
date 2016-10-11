import markdown
from moon.md import jinja2, fencedcode

def create_markdown():
    md = markdown.Markdown(['markdown.extensions.extra',
            'markdown.extensions.meta',
            fencedcode.makeExtension()])

    jinja2.makeJinjaExpressionPattern(md)
    return md


