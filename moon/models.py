from moon import *
from gitlet import git_update_check
from citation import Citations
from utils import to_date, to_time, to_datetime

import os, yaml, codecs

import os
from flask import safe_join, abort, g

def get_page(page_dir, path):
    page_path = None

    # 1) Test markdown
    try:
        md_path = safe_join(page_dir, path + '.md')
        if os.path.exists(md_path):
            page_path = md_path
    except Exception as e:
        print(e)
        print("Cannot find md path for " + path)

    if page_path:
        return get_markdown_page_or_404(page_path)

    abort(404)

def get_markdown_page_or_none(page_path):
    try:
        return get_markdown_page(page_path)
    except Exception as e:
        print(e)
        return None

def get_markdown_page(page_path):
    page = Page()
    with open(page_path, 'r') as f:
        #if not hasattr(g, 'md'):
        #    g.md = markdown.Markdown(['markdown.extensions.extra', 'markdown.extensions.meta'])

        page.html = g.md.convert(f.read().decode('utf-8'))
        page.meta = g.md.Meta # flask-pages naming covention
        for key, value in page.meta.iteritems():
            page.meta[key] = ''.join(value) # meta is a list
        return page

    abort(404)

def get_markdown_page_or_404(page_path):
    try:
        return get_markdown_page(page_path)
    except Exception as e:
        print(e)
        abort(404)

    abort(404)



class Pagination(object):
    ''' A plain object to facilitate add attr as it has __dict__

    '''
    pass

class Page(object):
    ''' A plain object to hold page information instead of using a dict

    '''
    pass

class Site(object):

    def __init__(self):
        # photos
        self._photos = load_photos()

        # events
        self._events = load_events()
        self._phd_events = load_phd_events()
        self._deadlines = load_deadlines()
        self._master_events = load_master_events()
        # news
        self._news = load_news()

        # people
        self._people = load_people()

        # papers
        self._paper = load_paper()
        self._spar_paper = load_spar_paper()

    @property
    def photos(self):
        return self._photos()

    @property
    def events(self):
        return self._events()

    @property
    def phd_events(self):
        return self._phd_events()

    @property
    def master_events(self):
        return self._master_events()

    @property
    def deadlines(self):
        return self._deadlines()

    @property
    def news(self):
        return self._news()

    @property
    def people(self):
        return self._people()

    @property
    def paper(self):
        return self._paper()

    @property
    def spar_paper(self):
        return self._spar_paper()

#####################################

def get_date(e):
    ''' A helper method used to sort entries
        No crash but will result in a bad page, e.g., incorrect date
    '''
    return e.get('date', '')


@git_update_check(DEADLINES_YAML)
def load_deadlines():
    ''' Load all deadlines, see events/deadlines.yaml

    All deadlines have been sorted manually
    '''
    e = None
    with open(DEADLINES_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(PHD_EVENTS_YAML)
def load_phd_events():
    ''' Load all PhD seminar events, see events/phd.yaml

    All PhD seminar events have been sorted manually
    '''
    e = None
    with open(PHD_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(MASTER_EVENTS_YAML)
def load_master_events():
    ''' Load all Master seminar events, see events/master.yaml

    All Master seminar events have been sorted manually
    '''
    e = None
    with open(MASTER_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@git_update_check(PHOTO_YAML)
def load_photos():
    ''' Load all photos shown in gallery

    '''
    p = None
    with open(PHOTO_YAML, 'r') as f:
        p = yaml.load(f)

    return sorted(p, key=get_date, reverse=True) if p else {}

@git_update_check(NEWS_DIR)
def load_news():
    ''' Load all news and paginations

    Result:
        a tuple of which the first element is the list of news
        and the second element is the Pagination object.
    '''
    n = None

    if not os.path.exists(NEWS_YAML):
        update_news_yaml()

    with open(NEWS_YAML, 'r') as f:
        n = yaml.load(f)
        if not (n and len(n)):
            # TODO raise 404 or 500?
            abort(500)
        n = sorted(n, key=get_date, reverse=True)

    pg = Pagination()
    pg.first = n[0]['page_num']
    pg.last  = n[-1]['page_num']

    return n, pg


def pagination(news_pages):
    ''' Set all news with a page_num

    '''
    num_per_page = 10

    for index, page in enumerate(news_pages):
        page['page_num'] = index / num_per_page + 1 # page number starts from 1

def update_news_yaml():
    ''' Scan news folder and save all news into a single yaml file

    Arguments:
        path: the path of the news in relative to the NEWS_DIR
        title: title in the metadata
        date: date in the metadata
        summary: summary in the metadata
        img_title: a image title should be 90x90 or 150x150 or MMxMM
        img_path: path in relative to the static folder
    '''
    rootdir = NEWS_DIR
    news_pages = []
    for subdir, dirs, files in os.walk(rootdir):
        curdir = os.path.join(rootdir, subdir)
        for f in files:
            f = os.path.join(curdir, f)
            if f.endswith('.md'):
                page = get_markdown_page_or_none(f)
            else:
                continue

            if page is None:
                print("Get page " + str(f) + " failed")
                continue

            pagedict = {}
            pagedict['path'] = os.path.splitext(os.path.relpath(f, rootdir).replace('\\','/'))[0]
            pagedict['title'] = page.meta.get('title', 'Please add a title')
            pagedict['date'] = to_datetime(page.meta.get('date', ''))
            pagedict['summary'] = page.meta.get('summary', 'Please provide a news body')
            pagedict['img_title'] = page.meta.get('img_title')
            pagedict['img_path'] = page.meta.get('img_path')
            # TODO Support news draft
            pagedict['status'] = page.meta.get('status')

            news_pages.append(pagedict)

    news_pages = sorted(news_pages, key=get_date, reverse=True)

    pagination(news_pages)

    news_cache = yaml.safe_dump(news_pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    # news_cache is a utf-8 encoded str object
    # convert it into an unicode object
    with codecs.open(NEWS_YAML, 'w', 'utf-8') as f:
        f.write(news_cache.decode("utf-8"))

@git_update_check(PEOPLE_YAML)
def load_people():
    ''' Load all people
    '''
    p = None
    with open(PEOPLE_YAML) as f:
        p = yaml.load(f)

    return p if p else {}

@git_update_check(EVENTS_YAML)
def load_events():
    '''Load general events,

    Empty now so we need check whether e is None and returning a {} accordingly
    '''
    e = None
    with open(EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return sorted(e, key=get_date, reverse=True) if e else {}

@git_update_check(SITE_PAPER)
def load_paper():
    '''Create a shared site paper
    '''
    return Citations(SITE_PAPER)

@git_update_check(SPAR_PAPER)
def load_spar_paper():
    '''Create a shared site paper
    '''
    return Citations(SPAR_PAPER)