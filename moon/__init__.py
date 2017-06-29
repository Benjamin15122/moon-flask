from flask import Flask
import os

DEBUG = True

MOON_DIR = os.path.dirname(
    os.path.sep.join ( os.path.abspath(__file__).split(os.path.sep)[:-1] )
)

CACHE_DIR = MOON_DIR + os.path.sep + 'cache'
DATA_DIR = MOON_DIR + os.path.sep + 'data'

PAGES_DIR = MOON_DIR + os.path.sep + 'pages'
PAGES_SHARE_DIR = PAGES_DIR + os.path.sep + 'share'

SPAR_DIR = PAGES_DIR + os.path.sep + 'spar'
SPAR_PAPER = SPAR_DIR + os.path.sep + 'spar.bib'
SITE_PAPER = PAGES_DIR + os.path.sep + 'paper.bib'
NEWS_DIR = PAGES_DIR + os.path.sep + 'news'
EVENTS_DIR = PAGES_DIR + os.path.sep + 'events'
DSE_DIR = PAGES_DIR + os.path.sep + 'dse'

PEOPLE_DIR = os.path.join(PAGES_DIR, 'people')

#############

PEOPLE_YAML = os.path.join(DATA_DIR, 'people.yaml')
PHOTO_YAML  = os.path.join(DATA_DIR, 'photo.yaml')
AWARDS_YAML= os.path.join(DATA_DIR, 'awards.yaml')
SHORTURL_YAML = os.path.join(DATA_DIR, 'shorturl.yaml')
PAPER_NEWS_YAML= os.path.join(DATA_DIR, 'papers_news.yaml')
AWARD_NEWS_YAML= os.path.join(DATA_DIR, 'awards_news.yaml')
SCHOLARSHIP_NEWS_YAML= os.path.join(DATA_DIR, 'scholarships_news.yaml')
EVENTS_YAML = os.path.join(DATA_DIR, 'events.yaml')
DEADLINES_YAML = os.path.join(DATA_DIR, 'deadlines_events.yaml')
PHD_EVENTS_YAML = os.path.join(DATA_DIR, 'phd_events.yaml')
MASTER_EVENTS_YAML = os.path.join(DATA_DIR, 'master_events.yaml')
NEWS_YAML = os.path.join(CACHE_DIR, 'news.yaml')

#############
GITSUBMODULES = MOON_DIR + os.path.sep + '.gitsubmodules'

GIT_CMD = 'git'

GIT_PULL_MOON = [GIT_CMD, '-C', MOON_DIR, 'pull', 'origin', 'master']
GIT_INIT_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'init']
GIT_UPDATE_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'update']
GIT_PULL_SUBMODULES = [GIT_CMD, '-C', MOON_DIR, 'submodule', 'foreach', 'git', 'pull', 'origin', 'master']

GIT_SHOW_HEAD_HASH = [GIT_CMD, '-C', MOON_DIR, 'log', '-1', '--format=%H']

#############

app = Flask(__name__,
    template_folder = MOON_DIR + os.path.sep + 'templates',
    static_folder = MOON_DIR + os.path.sep + 'static')
app.config.from_object(__name__)


import moon.views, moon.shorturl, moon.models, moon.jj, moon.md
