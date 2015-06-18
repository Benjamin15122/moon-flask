import flask
from moon import app

# TODO: move code to a better place (e.g., configuration file)
SHORT_URLS = {
    'jyy': 'http://moon.nju.edu.cn/spar/people/jyy.html',
    'txgu': '/people/tianxiaogu',
}

@app.route('/~<name>', methods=['GET'])
def short_url(name, path = None):
    if name in SHORT_URLS:
        return flask.redirect(SHORT_URLS[name])
    else:
        return flask.redirect('/')
