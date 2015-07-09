from flask import Flask
import os

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'

FLATPAGES_MARKDOWN_EXTENSIONS = []

MOON_GIT_URL = 'git@git.artemisprojects.org:moon.git'
MOON_DIR = os.path.dirname(
    os.path.sep.join ( os.path.abspath(__file__).split(os.path.sep)[:-1] )
)

SPAR_DIR = MOON_DIR + os.path.sep + 'spar'

PAGES_DIR = MOON_DIR + os.path.sep + 'pages'
NEWS_DIR = PAGES_DIR + os.path.sep + 'news'
EVENTS_DIR = PAGES_DIR + os.path.sep + 'events'

PEOPLE_YAML = PAGES_DIR + os.path.sep + 'people.yaml'
PHOTO_YAML  = PAGES_DIR + os.path.sep + 'photo.yaml'
SHORTURL_YAML = PAGES_DIR + os.path.sep + 'shorturl.yaml'
NEWS_YAML= NEWS_DIR + os.path.sep + 'news.yaml'
EVENTS_YAML = EVENTS_DIR + os.path.sep + 'events.yaml'
DEADLINES_YAML = EVENTS_DIR + os.path.sep + 'deadlines.yaml'
PHD_EVENTS_YAML = EVENTS_DIR + os.path.sep + 'phd.yaml'
MASTER_EVENTS_YAML = EVENTS_DIR + os.path.sep + 'master.yaml'

GITSUBMODULES = MOON_DIR + os.path.sep + '.gitsubmodules'

GIT_CMD = 'git'

GIT_PULL_MOON = [GIT_CMD, '-C', MOON_DIR, 'pull', 'origin', 'master']
GIT_INIT_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'init']
GIT_UPDATE_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'update']
GIT_PULL_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'foreach', 'git', 'pull', 'origin', 'master']

GIT_SHOW_HEAD_HASH = [GIT_CMD, '-C', MOON_DIR, 'log', '-1', '--format=%H']

app = Flask(__name__,
    template_folder = MOON_DIR + os.path.sep + 'templates',
    static_folder = MOON_DIR + os.path.sep + 'static')
app.config.from_object(__name__)

import moon.views, moon.shorturl, moon.spar, moon.gitlet
