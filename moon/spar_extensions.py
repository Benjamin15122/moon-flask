"""
Extensions
    SparPeople: replace a line containing "[PEOPLE]" into a list of peoples
    Arithmatex: replace $...$ quoted into inline math
"""
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from flask import g
import re

class SparPeopleProcessor(Preprocessor):
    def run(self, lines):
        def display_people(p):
            d = []
            d.append('<div class="col-lg-2 col-md-3 col-sm-6">')
            d.append('<div class="pblock">')

            if 'url' in p: d.append('<a href="%s">' % p['url'])

            d.append('<table><tr>')
            avatar = p.get('avatar', '/static/img/avatar/default.jpg')
            name = p['name'].split(' ')
            if len(name) == 2: name = ' '.join(name)
            else: name = ' '.join(name[:-1]) + '<br>' + name[-1]
                
            d.append('<td><img class="avatar" src="%s"/></td>' % avatar)
            d.append('<td><span class="spar-name">%s</span></td>' % name)

            d.append('</tr></table>')

            if 'url' in p: d.append('</a>')
            d.append('</div>')
            d.append('</div>')
            return '\n'.join(d)

        ret = []
        ret.append('''<div class="spar-people"><div class="row people" >''')
        for (key, name) in zip(
            ['faculty', 'phd', 'graduates', 'alumni'],
            ['Mentors', 'Ph. D students', 'M. Sc students', 'Alumni/ae'],
        ):
            ret.append("### %s" % name)
            ret.append('<div class="row small k-equal-height">')
            for p in g.site.people[key]:
                groups = [i.strip() for i in p.get('group', '').split(',')]
                if 'spar' in groups:
                    ret.append(display_people(p))
            ret.append('</div>')

        ret.append('</div></div>')

        peoples = '\n'.join(ret)
        new_lines = []
        for line in lines:
            if line == '[SPAR_PEOPLE]':
                new_lines.append(peoples)
            else:
                new_lines.append(line)
        return new_lines

class SparPeopleExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.preprocessors.add(
                "spar-people",
                SparPeopleProcessor(),
                "_end"
            )

"""
Arithmatex.
MIT license.
Copyright (c) 2014 - 2015 Isaac Muse <isaacmuse@gmail.com>
"""

RE_MATH = r'((?<!\\)(?:\\{2})*)([$])(?!\s)((?:\\.|[^$])+?)(?<!\s)(\3)'
RE_DOLLAR_ESCAPE = re.compile(r'\\.')

F_BLOCK = "<span class='math'>%s</span>"
F_INLINE = "<span class='inline_math'>%s</span>"


def escape(txt):
    """Escape HTML content."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class InlineArithmatexPattern(Pattern):
    """Arithmatex inline pattern handler."""

    def __init__(self, pattern, md):
        """Initialize."""

        Pattern.__init__(self, pattern)
        self.markdown = md

    def handleMatch(self, m):
        """Handle notations and switch them to something that will be more detectable in HTML."""

        # Use the more reliable patterns to avoid '$'
        # false positives.
        math = "%s" % RE_DOLLAR_ESCAPE.sub(
            lambda m: '$' if m.group(0) == "\\$" else m.group(0),
            m.group(4)
        )
        return m.group(2) + self.markdown.htmlStash.store(
            F_INLINE % escape(math),
            safe=True
        )


class BlockArithmatexProcessor(BlockProcessor):
    """Mathjax block processor to find $$mathjax$$ content."""

    RE_MATH_BLOCK = re.compile(
        r'(?s)^(?P<dollar>[$]{2})(?P<math>.*?)(?P=dollar)[ ]*$'
    )

    def __init__(self, md):
        """Initialize."""

        BlockProcessor.__init__(self, md.parser)
        self.markdown = md

    def test(self, parent, block):
        """Return 'True' for future Python Markdown block compatibility."""
        return True

    def run(self, parent, blocks):
        """Find and handle block content."""

        handled = False

        m = self.RE_MATH_BLOCK.match(blocks[0])

        if m:
            handled = True
            block = blocks.pop(0)
            # Use the more reliable patterns to avoid '$'
            # false positives.
            math = "%s" % RE_DOLLAR_ESCAPE.sub(
                lambda m: '$' if m.group(0) == "\\$" else m.group(0),
                m.group('math')
            )
            block = self.markdown.htmlStash.store(
                F_BLOCK % escape(math),
                safe=True
            )
            blocks.insert(0, block)
        return handled


class ArithmatexExtension(Extension):
    """Adds delete extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """Extend the inline and block processor objects."""

        md.registerExtension(self)
        if "$" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('$')

        md.inlinePatterns.add(
            "arithmatex-inline",
            InlineArithmatexPattern(RE_MATH, md),
            ">backtick"
        )

        md.parser.blockprocessors.add(
            'arithmatex-block',
            BlockArithmatexProcessor(md),
            "<code"
        )

