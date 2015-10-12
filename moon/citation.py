from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.extensions.codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines
from markdown.inlinepatterns import Pattern
from markdown.util import etree

from flask import render_template_string

import re

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
                if self.codehilite_conf:
                    highliter = CodeHilite(m.group('code'),
                            linenums=self.codehilite_conf['linenums'][0],
                            guess_lang=self.codehilite_conf['guess_lang'][0],
                            css_class=self.codehilite_conf['css_class'][0],
                            style=self.codehilite_conf['pygments_style'][0],
                            lang=(m.group('lang') or None),
                            noclasses=self.codehilite_conf['noclasses'][0],
                            hl_lines=parse_hl_lines(m.group('hl_lines')))

                    code = highliter.hilite()
                elif m.group('lang') == 'bibtexhtml':
                    code = self.parse_bibtex(m.group('code'), m.group('hl_lines'));
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


def makeExtension(**kwargs):
    return MoonFencedCodeExtension(**kwargs)


import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from flask import get_template_attribute

def decorate_author(author):
    ''' Simply normalize all FamilyName, GivenName [MiddleName] to GivenName [MiddleName] FamilyName
    '''

    authors = author.split('and')

    new_authors = []
    for a in authors:
        ns = a.strip().split(',')
        if len(ns) == 2:
            new_authors.append(ns[1].strip() + ' ' + ns[0].strip())
        elif len(ns) == 1:
            new_authors.append(ns[0])
        else:
            # should not happen
            new_authors.append[a.strip()]

    # if you modify here, you should modify your template
    #return ' and '.join(new_authors)
    return new_authors


# TODO use bibtexparser library customizations
# see https://bibtexparser.readthedocs.org/en/latest/tutorial.html#parsing-the-file-into-a-bibliographic-database-object

HYPEN_HYPEN = u'\u2013' # -- in LaTeX
PAGES_RE = re.compile(r'(?P<begin>[0-9]+)-+(?P<end>[0-9]+)')

def decorate_pages(pages):
    m = PAGES_RE.match(pages)
    if m:
        return m.group('begin') + HYPEN_HYPEN + m.group('end')

    # if not match return
    return pages


def decorate_entries(entries):
    for entry in entries:
        if 'author' in entry:
            entry['author'] = decorate_author(entry['author'])

        if 'pages' in entry:
            entry['pages'] = decorate_pages(entry['pages'])

    return entries


def convert_bibtex(bibtex, hl=None):
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    try:
        bib_database = bibtexparser.loads(bibtex, parser=parser)
    except:
        return bibtex

    entries = decorate_entries(bib_database.entries)

    return convert_bibentries_to_html(entries, hl)

def convert_bibentries_to_html(entries, hl=''):
    ''' Convert a list of bibtex entries into html

    Args: the list of entries
    '''
    render = get_template_attribute('bibtex.html', 'render_entries')
    return render(entries, hl)



def render_bib_entry(entry, hl=''):
    render = get_template_attribute('bibtex.html', 'render_entry')

    return render(entry, hl)


def render_bib_entries(entries, hl=''):
    render = get_template_attribute('bibtex.html', 'render_entries')

    return render(entries, hl)

def parse_bibtex(bibtex):
    parser = BibTexParser()
    parser.customization = convert_to_unicode

    return bibtexparser.loads(bibtex, parser=parser)


class Citations(object):

    def __init__(self, bibfile):
        with open(bibfile) as f:
            bibtex_str = f.read().decode('utf-8')

        database = parse_bibtex(bibtex_str)
        self.entries = decorate_entries(database.entries)


    def __getitem__(self, key):
        try:
            return next(e for e in self.entries if e.get('id') == key or e.get('ID') == key)
        except:
            raise KeyError(key)

    def render_entry(self, key, hl=''):
        entry = self.__getitem__(key)

        if not entry:
            return "No such entry with key " + key

        return render_bib_entry(entry, hl)

    def render_entries(self, keys, hl=''):
        entries = filter(lambda e: e.get('id') in keys, self.entries)
        entries += filter(lambda e: e.get('ID') in keys, self.entries)
        return render_bib_entries(entries, hl)


    def render_all(self, hl=''):
        return render_bib_entries(self.entries, hl)


#################################################################


JINJA_BLOCK_RE = r'({{[^{}]*}})'

class JinjaBlockPattern(Pattern):

    def __init__(self, pattern, md):
        Pattern.__init__(self, pattern, md)

    def handleMatch(self, m):
        jinja_block = m.group(2)

        try:
            # render returns a unicode object, encode it into a utf-8 string
            html = render_template_string(m.group(2))
        except Exception as e:
            return etree.fromstring('<em>Error: %s</em>' % m.group(2))

        try:
            return etree.fromstring(html)
        except:
            elem = etree.Element(None)
            elem.text = html
            return elem


def makeJinjaBlockPattern(md):
    md.inlinePatterns.add('jinja block pattern', JinjaBlockPattern(JINJA_BLOCK_RE, md), ">backtick") # after backtick

