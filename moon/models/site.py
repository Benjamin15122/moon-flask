from moon import *
from moon.utils import to_date, to_time, to_datetime, get_datetime

import os, yaml

import traceback

from flask import safe_join, abort, g

from moon.models.bibtex import Citations
from moon.models.page import load_page_yaml

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
        self._paper_news = load_paper_news()
        self._award_news = load_award_news()
        self._scholarship_news = load_scholarship_news()

        # people
        self._people = load_people()

        # papers
        self._paper = load_paper()
        self._spar_paper = load_spar_paper()

        # awards
        self._awards = load_awards()
        
        # shorturl
        self._shorturl = load_shorturl()

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
    def paper_news(self):
        return self._paper_news()

    @property
    def award_news(self):
        return self._award_news()

    @property
    def scholarship_news(self):
        return self._scholarship_news()

    @property
    def people(self):
        return self._people()

    @property
    def paper(self):
        return self._paper()

    @property
    def spar_paper(self):
        return self._spar_paper()

    @property
    def awards(self):
        return self._awards()

    @property
    def shorturl(self):
        return self._shorturl()

    def find_people_by_url(self, url):
        for role,folks in self.people.iteritems():
            for folk in folks:
                if folk.get('url') == url:
                    return folk

        return None


#####################################

def lazy_load(method):
    def wrapper():
        return GitValueChecker(method)
    return wrapper

class GitValueChecker:

    def __init__(self, callback):
        self.callback = callback
        self.value = None

    def update(self, *args, **kwargs):

        if self.value is None:
            self.value = self.callback(*args, **kwargs)

        return self.value

    def __call__(self, *args, **kwargs):
        ''' shortcut for update
        '''
        return self.update(*args, **kwargs)


@lazy_load
def load_deadlines():
    ''' Load all deadlines, see events/deadlines.yaml

    All deadlines have been sorted manually
    '''
    e = None
    with open(DEADLINES_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@lazy_load
def load_phd_events():
    ''' Load all PhD seminar events, see events/phd.yaml

    All PhD seminar events have been sorted manually
    '''
    e = None
    with open(PHD_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@lazy_load
def load_master_events():
    ''' Load all Master seminar events, see events/master.yaml

    All Master seminar events have been sorted manually
    '''
    e = None
    with open(MASTER_EVENTS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}


@lazy_load
def load_paper_news():
    ''' Load all Master seminar events, see events/master.yaml

    All paper news events have been sorted manually
    '''
    e = None
    with open(PAPER_NEWS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}


@lazy_load
def load_award_news():
    ''' Load all Master seminar events, see events/master.yaml

    All award news have been sorted manually
    '''
    e = None
    with open(AWARD_NEWS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}


@lazy_load
def load_scholarship_news():
    ''' Load all Master seminar events, see events/master.yaml

    All scholarship news have been sorted manually
    '''
    e = None
    with open(SCHOLARSHIP_NEWS_YAML, 'r') as f:
        e = yaml.load(f)

    return e if e else {}

@lazy_load
def load_photos():
    ''' Load all photos shown in gallery

    '''
    p = None
    with open(PHOTO_YAML, 'r') as f:
        p = yaml.load(f)

    return sorted(p, key=get_datetime, reverse=True) if p else {}

@lazy_load
def load_news():
    ''' Load all news and paginations

    Result:
        a tuple of which the first element is the list of news
        and the second element is the Pagination object.
    '''
    n = None

    try:
        page_yaml = NEWS_YAML
        root_dir = NEWS_DIR
        blacklist = ['index.md', 'papers.md', 'awards.md', 'scholarships.md']

        pg = load_page_yaml(page_yaml, root_dir, blacklist=blacklist)
        return pg
    except Exception as e:
        traceback.print_exc(e)

@lazy_load
def load_people():
    ''' Load all people
    '''
    p = None
    with open(PEOPLE_YAML) as f:
        try:
            p = yaml.load(f)
        except Exception as e:
            p = None

    return p if p else {}

@lazy_load
def load_events():
    '''Load general events,

    Empty now so we need check whether e is None and returning a {} accordingly
    '''
    e = None
    with open(EVENTS_YAML, 'r') as f:
        try:
            e = yaml.load(f)
        except Exception as ex:
            e = None

    return sorted(e, key=get_datetime, reverse=False) if e else {}

@lazy_load
def load_paper():
    '''Create a shared site paper
    '''
    return Citations(SITE_PAPER)

@lazy_load
def load_spar_paper():
    '''Create a shared site paper
    '''
    return Citations(SPAR_PAPER)

@lazy_load
def load_awards():
    '''Load ICS awards,

    Empty now so we need check whether e is None and returning a {} accordingly
    '''
    e = None
    with open(AWARDS_YAML, 'r') as f:
        try:
            e = yaml.load(f)
        except Exception as ex:
            e = None

    return sorted(e, key=get_datetime, reverse=False) if e else {}

@lazy_load
def load_shorturl():
    '''Load url shortcuts for personal homepage
       e.g., /~txgu -> /people/tianxiaogu
    '''
    e = None
    with open(SHORTURL_YAML, 'r') as f:
        try:
            e = yaml.load(f)
        except Exception as ex:
            e = None
    return e if e else {}
