from moon import *
from flask import safe_join, abort, g
import traceback

from moon.md import create_markdown

def get_user_dir(name):
    user_dir = safe_join(PAGES_DIR, name)

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
        return page


class Pagination(object):
    ''' A plain object to facilitate add attr as it has __dict__

    '''
    def __init__(self, items):
        num_per_page = 10
        total_page = len(items) / num_per_page + 1

        self.pages = [[]] * total_page
        self.num_per_page = num_per_page
        self.total_page = total_page

        for index, item in enumerate(items):
            page_num = index / num_per_page + 1 # page number starts from 1
            self.pages[page_num - 1].append(item)
            item['page_num'] = page_num

        self.first = 1
        self.last = total_page

class Page(object):
    ''' A plain object to hold page information instead of using a dict

    '''
    pass


