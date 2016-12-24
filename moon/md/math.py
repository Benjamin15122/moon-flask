"""
Arithmatex.
MIT license.
Copyright (c) 2014 - 2015 Isaac Muse <isaacmuse@gmail.com>
"""

from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor
from flask import g
import re

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

        g.bundle.enable('math')
        g.bundle.code.append(
'''function decode(h) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = h;
    val = textArea.value;
    if ('remove' in Element.prototype) textArea.remove();
    return val;
}

$(function() {
  $("span.math").each(function(idx, e) {
    try {
      var d = katex.renderToString(decode(e.innerHTML), { displayMode: true, throwOnError: false });
      e.innerHTML = d;
    } catch (err) {}
  });

  $("span.inline_math").each(function(idx, e) {
    try {
      var d = katex.renderToString(decode(e.innerHTML), { throwOnError: false });
      e.innerHTML = d;
    } catch (err) {}
  });

});''')

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

