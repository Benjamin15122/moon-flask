from flask import url_for

BUNDLES = {
    'qqmap': [
        [],
        [ 'http://map.qq.com/api/js?v=2.exp&key=WBEBZ-EL6WS-A4ZOR-643I5-VIJE5-SYBU7',
          'http://open.map.qq.com/plugin/v2/PanoramaOverview/PanoramaOverview-min.js'],
        [],
        ],

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

def make_url(path):

    if path.startswith('http://') or path.startswith('https://'):
        return path

    return url_for('static', filename=path)

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
                    ret.append(make_url(j))

        return ret

    @property
    def css(self):
        ret = []
        for name, b in BUNDLES.iteritems():
            if name in self.enabled:
                for c in b[0]:
                    ret.append(make_url(c))

        return ret

