from markdown.inlinepatterns import Pattern
from markdown.util import etree

from flask import render_template_string

import traceback

JINJA_EXPRESSION_RE = r'({{.+?(?<!})}})'

class JinjaExpressionPattern(Pattern):

    def __init__(self, pattern, md):
        Pattern.__init__(self, pattern, md)

    def handleMatch(self, m):
        jinja_block = m.group(2)

        try:
            # render returns a unicode object
            html = render_template_string(m.group(2))
        except Exception as e:
            traceback.print_exc(e)
            return etree.fromstring('<em>Error %s in rendering %s</em>' % (e, m.group(2)))

        try:
            return etree.fromstring(html.encode('utf-8'))
        except Exception as e:
            pass

        try:
            e = etree.Element(None)
            e.text = html
            return e
        except Exception as e:
            return html



def makeJinjaExpressionPattern(md):
    md.inlinePatterns.add('jinja expression pattern', JinjaExpressionPattern(JINJA_EXPRESSION_RE, md), ">backtick") # after backtick


