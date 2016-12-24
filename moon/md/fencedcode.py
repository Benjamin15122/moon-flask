from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
from markdown.inlinepatterns import Pattern
from markdown.util import etree


import re

from moon.models.bibtex import convert_bibtex
from moon.models.jstrick import make_flowchart, make_raphael, make_customjs

"""Copied from FencedCodeExtension
"""
class MoonFencedCodeExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        """ Add MoonFencedBlockPreprocessor to the Markdown instance. """
        md.registerExtension(self)

        md.preprocessors.add('moon_fenced_code_block',
                                 MoonFencedBlockPreprocessor(md),
                                 ">normalize_whitespace")


class MoonFencedBlockPreprocessor(Preprocessor):
    FENCED_BLOCK_RE = re.compile(r'''
(?P<fence>^(?:~{3,}|`{3,}))[ ]*         # Opening ``` or ~~~
(\{?\.?(?P<lang>[a-zA-Z0-9_+-]*))?[ ]*  # Optional {, and lang
# Optional highlight lines, single- or double-quote-delimited
(hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot))?[ ]*
}?[ ]*\n                                # Optional closing }
(?P<code>.*?)(?<=\n)
(?P=fence)[ ]*$''', re.MULTILINE | re.DOTALL | re.VERBOSE)
    CODE_WRAP = '<pre><code%s>%s</code></pre>'
    LANG_TAG = ' class="%s"'

    def __init__(self, md):
        super(MoonFencedBlockPreprocessor, self).__init__(md)

        self.checked_for_codehilite = False
        self.codehilite_conf = {}

    def run(self, lines):
        """ Match and store Fenced Code Blocks in the HtmlStash. """

        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, CodeHiliteExtension):
                    self.codehilite_conf = ext.config
                    break

            self.checked_for_codehilite = True

        text = "\n".join(lines)
        while 1:
            m = self.FENCED_BLOCK_RE.search(text)
            if m:
                lang = ''
                if m.group('lang'):
                    lang = self.LANG_TAG % m.group('lang')

                # If config is not empty, then the codehighlite extension
                # is enabled, so we call it to highlight the code
                if m.group('lang') == 'bibtexhtml':
                    code = self.parse_bibtex(m.group('code'), m.group('hl_lines'));
                elif m.group('lang') == 'flowchart':
                    code = self.parse_flowchart(m.group('code'), m.group('hl_lines'));
                elif m.group('lang') == 'raphael':
                    code = self.parse_raphael(m.group('code'), m.group('hl_lines'));
                elif m.group('lang') == 'customjs':
                    code = self.parse_customjs(m.group('code'));
                elif self.codehilite_conf:
                    highliter = CodeHilite(m.group('code'),
                            linenums=self.codehilite_conf['linenums'][0],
                            guess_lang=self.codehilite_conf['guess_lang'][0],
                            css_class=self.codehilite_conf['css_class'][0],
                            style=self.codehilite_conf['pygments_style'][0],
                            lang=(m.group('lang') or None),
                            noclasses=self.codehilite_conf['noclasses'][0],
                            hl_lines=parse_hl_lines(m.group('hl_lines')))

                    code = highliter.hilite()
                else:
                    code = self.CODE_WRAP % (lang, self._escape(m.group('code')))

                placeholder = self.markdown.htmlStash.store(code, safe=True)
                text = '%s\n%s\n%s'% (text[:m.start()], placeholder, text[m.end():])
            else:
                break
        return text.split("\n")

    def _escape(self, txt):
        """ basic html escaping """
        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        return txt

    def parse_bibtex(self, bibtex, hl=None):
        return convert_bibtex(bibtex, hl)

    def parse_flowchart(self, code, diagramid=None):
        return make_flowchart(code, diagramid)

    def parse_raphael(self, code, diagramid=None):
        return make_raphael(code, diagramid)

    def parse_customjs(self, code):
        return make_customjs(code)

def makeExtension(**kwargs):
    return MoonFencedCodeExtension(**kwargs)


