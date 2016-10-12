from moon import *
from flask import safe_join, abort, g
import traceback

from moon.md import create_markdown

from moon.utils import get_datetime

import os, codecs, urllib, yaml

def update_page_yaml(page_yaml, page_md_files, base_dir):
    pages = []

    for md_file in page_md_files:
        try:
            page = get_markdown_page(md_file)

            # ignore draft
            if page.meta.get('status') == 'draft':
                continue

            page_dict = {}
            page_dict.update(page.meta)
            page_dict['path'] = os.path.splitext(urllib.pathname2url(os.path.relpath(md_file, base_dir)))[0]

            pages.append(page_dict)
        except Exception as e:
            traceback.print_exc(e)
            continue

    pages = sorted(pages, key=get_datetime, reverse=True)
    pg = Pagination(pages)

    page_cache = yaml.safe_dump(pages, default_flow_style=False, allow_unicode=True, encoding='utf-8')
    # cache is a utf-8 encoded str object
    # convert it into an unicode object
    with codecs.open(page_yaml, 'w', 'utf-8') as f:
        f.write(page_cache.decode("utf-8"))

    return pg

def load_page_yaml(page_yaml, page_root_dir, path_base_dir=PAGES_DIR, blacklist=['index.md']):
    dirty, md_files = check_cache(page_yaml, page_root_dir, blacklist)

    if dirty:
        pg = update_page_yaml(page_yaml, md_files, path_base_dir)
    else:
        with open(page_yaml, 'r') as f:
            n = yaml.load(f)
        pg = Pagination(n)

    return pg

def check_cache(cache_file, rootdir, blacklist):
    if not os.path.exists(cache_file):
        parent_dir= os.path.dirname(os.path.abspath(cache_file))
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        dirty = True
    else:
        cache_last_mtime = os.path.getmtime(cache_file) # mtime is a number in seconds
        dirty = False

    md_files = []
    for subdir, dirs, files in os.walk(rootdir):
        curdir = os.path.join(rootdir, subdir)
        for f in files:
            if f.endswith('.md') and f not in blacklist:
                f = os.path.join(curdir, f)
                md_files.append(f)
                if not dirty and os.path.getmtime(f) > cache_last_mtime:
                    dirty = True

    return dirty, md_files




def get_cache_dir(page_path):
    path = os.path.relpath(page_path, PAGES_DIR)
    return safe_join(CACHE_DIR, path)

def get_user_dir(name):
    user_dir = safe_join(PEOPLE_DIR, name)

    # pages in the 'share' folder can be either
    # accessed by /people/share/haosun/ or /people/haosun/
    if not os.path.exists(user_dir):
        user_dir = safe_join(PAGES_SHARE_DIR, name)

    return user_dir



def get_page(page_dir, path):
    page_path = None

    try:
        md_path = safe_join(page_dir, path + '.md')
        if os.path.exists(md_path):
            try:
                return get_markdown_page(md_path)
            except Exception as e:
                traceback.print_exc(e)
    except Exception as e:
        pass

    abort(404)

def get_markdown_page(page_path):
    page = Page()
    with open(page_path, 'r') as f:
        md = create_markdown()
        page.html = md.convert(f.read().decode('utf-8'))
        page.meta = md.Meta # flask-pages naming convention
        for key, value in page.meta.iteritems():
            page.meta[key] = ''.join(value) # meta is a list

        bundle = page.meta.get('bundle')
        if bundle:
            for b in bundle.split(','):
                g.bundle.enable(b.strip())

        return page


class Pagination(object):
    ''' A plain object to facilitate add attr as it has __dict__

    '''
    def __init__(self, items):
        num_per_page = 10
        total_page = len(items) / num_per_page + 1

        self.items = items
        self.pages = [[]] * total_page
        self.num_per_page = num_per_page
        self.total_page = total_page

        for index, item in enumerate(items):
            page_num = index / num_per_page + 1 # page number starts from 1
            self.pages[page_num - 1].append(item)
            if isinstance(item, dict):
                item['page_num'] = page_num
            else:
                item.page_num = page_num

        self.first = 1
        self.last = total_page
        self.current = 1

    @property
    def current_items(self):
        try:
            return self.pages[self.current - 1]
        except:
            return []

class Page(object):
    ''' A plain object to hold page information instead of using a dict

    '''
    pass



####################################
def load_blog_yaml(name):
    user_dir = get_user_dir(name)
    root_dir = safe_join(user_dir, 'blog')
    blog_yaml = get_cache_dir(safe_join(root_dir, 'blogs.yaml'))

    pg = load_page_yaml(blog_yaml, root_dir, user_dir, blacklist=['index.md'])


    return Pagination([Blog(name, user_dir, i) for i in pg.items])


class Blog(object):

    def __init__(self, name, user_dir, yaml_dict):
        self.name = name
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
