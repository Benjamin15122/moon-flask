from moon import *
from moon.utils import to_date, to_time, to_datetime, get_date

import os, yaml, codecs

import traceback

from flask import safe_join, abort, g

from moon.models.bibtex import Citations
from moon.models.page import get_markdown_page, Pagination, get_user_dir, get_page

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

    return sorted(p, key=get_date, reverse=True) if p else {}

@lazy_load
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
        n = filter(lambda news : news.get('status') != 'draft', n)

    return n

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
        if os.path.abspath(subdir) == os.path.abspath(rootdir):
            continue
        curdir = os.path.join(rootdir, subdir)
        for f in files:
            f = os.path.join(curdir, f)
            if f.endswith('.md'):
                page = get_markdown_page(f)
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

    pg = Pagination(news_pages)

    news_cache = yaml.safe_dump(news_pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    # news_cache is a utf-8 encoded str object
    # convert it into an unicode object
    with codecs.open(NEWS_YAML, 'w', 'utf-8') as f:
        f.write(news_cache.decode("utf-8"))

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

    return sorted(e, key=get_date, reverse=False) if e else {}

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


####################################

class Blogs(object):

    def __init__(self, name, p):
        self.name = name
        self.blogs = load_blogs(name)
        self.current = p
        if self.blogs and len(self.blogs) > 0:
            self.first = self.blogs[0].page_num
            self.last = self.blogs[-1].page_num
        else:
            self.first = self.last = 1

    @property
    def current_pages(self):
        return [b for b in self.blogs if b.page_num == self.current]


def load_blogs(name):
    user_dir = get_user_dir(name)
    return list([Blog(user_dir, y) for y in load_blog_yaml(user_dir)])

def load_blog_yaml(user_dir):
    rootdir = safe_join(user_dir, 'blog')
    blog_yaml = safe_join(rootdir, 'blogs.yaml')

    if not os.path.exists(blog_yaml):
        dirty = True
    else:
        cache_last_mtime = os.path.getmtime(blog_yaml) # mtime is a number in seconds
        dirty = False

    blog_pages = []
    blog_md_files = []
    for subdir, dirs, files in os.walk(rootdir):
        curdir = os.path.join(rootdir, subdir)
        for f in files:
            if f == 'index.md':
                continue
            f = os.path.join(curdir, f)
            if f.endswith('.md'):
                blog_md_files.append(f)
                if not dirty and os.path.getmtime(f) > cache_last_mtime:
                    dirty = True
            else:
                continue

    if dirty:
        return update_blog_yaml(user_dir, blog_yaml, blog_md_files)


    with open(blog_yaml, 'r') as f:
        try:
            return yaml.load(f)
        except Exception as e:
            pass

    return {}


def update_blog_yaml(user_dir, blog_yaml, blog_md_files):
    blog_pages = []

    for md_file in blog_md_files:
        try:
            page = get_markdown_page(md_file)

            # ignore draft
            if page.meta.get('status') == 'draft':
                continue

            blog_dict = {}

            blog_dict['path'] = os.path.splitext(os.path.relpath(md_file, user_dir).replace('\\','/'))[0]
            blog_dict['title'] = page.meta.get('title', 'Please add a title')
            blog_dict['date'] = to_datetime(get_date(page.meta))
            blog_dict['category'] = page.meta.get('category')
            blog_dict['tags'] = page.meta.get('tags')

            blog_pages.append(blog_dict)
        except Exception as e:
            traceback.print_exc(e)
            continue

    Pagination(blog_pages)

    blog_cache = yaml.safe_dump(blog_pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    # cache is a utf-8 encoded str object
    # convert it into an unicode object
    with codecs.open(blog_yaml, 'w', 'utf-8') as f:
        f.write(blog_cache.decode("utf-8"))

    return blog_pages


class Blog(object):

    def __init__(self, user_dir, yaml_dict):
        self.user_dir = user_dir
        self.__dict__.update(yaml_dict)
        self._page = None

    @property
    def page(self):
        if self._page:
            return self._page

        try:
            self._page = get_page(self.user_dir, self.path)
        except Exception as e:
            traceback.print_exc(e)
            abort(500)

        return self._page
