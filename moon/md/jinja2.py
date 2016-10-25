from markdown.inlinepatterns import Pattern
from markdown.util import etree, AtomicString

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
            place_holder = self.markdown.htmlStash.store(html)
            return place_holder
        except Exception as e:
            traceback.print_exc()

            el = etree.Element('em')
            el.text = AtomicString('Error %s in rendering %s' % (e, m.group(2)))
            return el




def makeJinjaExpressionPattern(md):
    md.inlinePatterns.add('jinja expression pattern', JinjaExpressionPattern(JINJA_EXPRESSION_RE, md), ">backtick") # after backtick


