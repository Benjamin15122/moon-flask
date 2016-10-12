from flask import g

def make_flowchart(code, diagramid):
    if diagramid is None:
        diagramid = id(code)
    else:
        diagramid = str(diagramid)

    g.bundle.enable('flowchart')
    g.bundle.code.append(
    u'''$(document).ready(function() {{
        flowchart.parse("{0}").drawSVG("{1}");
    }});'''.format(code.replace('\n', '\\n\\\n'), diagramid)
            )

    return u'<div id="{0}"></div>'.format(diagramid)

def make_raphael(code, diagramid):
    if diagramid is None:
        diagramid = id(code)
    else:
        diagramid = str(diagramid)


    g.bundle.enable('raphael')
    g.bundle.code.append(code)

    return u'<div id="{0}" style="width:100%%;height:100%%;"></div>'.format(diagramid)
