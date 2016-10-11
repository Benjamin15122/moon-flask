from flask import url_for

BUNDLES = {
    'raphael':[
        [], # style file
        ['js/raphael/raphael.min.js'], # js file
        [], # deps
        ],

    'flowchart':[
        [], # style file
        ['js/flowchart/flowchart.min.js'], # js file
        ['raphael'], # deps
        ],

    'math': [
        ['css/katex.min.css'], # style file
        ['js/katex/katex.min.js'], # js file
        [], # deps
        ],
}


class Bundle(object):
    def __init__(self):
        self.enabled = set()
        self.code = []

    def enable(self,jslib):
        if jslib in self.enabled:
            return

        b = BUNDLES.get(jslib)
        if not b:
            return

        self.enabled.add(jslib)
        for d in b[2]:
            self.enable(d)

    @property
    def js(self):
        ret = []
        for name, b in BUNDLES.iteritems():
            if name in self.enabled:
                for j in b[1]:
                    ret.append(url_for('static', filename=j))

        return ret

    @property
    def css(self):
        ret = []
        for name, b in BUNDLES.iteritems():
            if name in self.enabled:
                for c in b[0]:
                    ret.append(url_for('static', filename=c))

        return ret

