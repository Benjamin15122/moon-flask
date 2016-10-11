from flask import Flask
import os

DEBUG = True

MOON_GIT_URL = 'git@git.artemisprojects.org:moon.git'
MOON_DIR = os.path.dirname(
    os.path.sep.join ( os.path.abspath(__file__).split(os.path.sep)[:-1] )
)

SPAR_DIR = MOON_DIR + os.path.sep + 'spar'

PAGES_DIR = MOON_DIR + os.path.sep + 'pages'
PAGES_SHARE_DIR = PAGES_DIR + os.path.sep + 'share'
SPAR_PAPER = SPAR_DIR + os.path.sep + 'spar.bib'

SITE_PAPER = PAGES_DIR + os.path.sep + 'paper.bib'

NEWS_DIR = PAGES_DIR + os.path.sep + 'news'
EVENTS_DIR = PAGES_DIR + os.path.sep + 'events'
DSE_DIR = PAGES_DIR + os.path.sep + 'dse'

PEOPLE_YAML = PAGES_DIR + os.path.sep + 'people.yaml'
PHOTO_YAML  = PAGES_DIR + os.path.sep + 'photo.yaml'
SHORTURL_YAML = PAGES_DIR + os.path.sep + 'shorturl.yaml'
NEWS_YAML= NEWS_DIR + os.path.sep + 'news.yaml'
PAPER_NEWS_YAML= NEWS_DIR + os.path.sep + 'papers.yaml'
AWARD_NEWS_YAML= NEWS_DIR + os.path.sep + 'awards.yaml'
SCHOLARSHIP_NEWS_YAML= NEWS_DIR + os.path.sep + 'scholarships.yaml'
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


import moon.views, moon.shorturl, moon.models, moon.jj, moon.md

# new view, temporarily parallel with old codes
DOC_ROOT = os.path.join(MOON_DIR, 'docs')
import moon.newview
