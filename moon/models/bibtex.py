
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from flask import get_template_attribute
import re

from itertools import groupby

def getyear(e):
    return e.get('year', 'Unknown')



def decorate_author(author):
    ''' Simply normalize all FamilyName, GivenName [MiddleName] to GivenName [MiddleName] FamilyName
    '''

    authors = author.split('and')

    new_authors = []
    for a in authors:
        ns = a.strip().split(',')
        if len(ns) == 2:
            new_authors.append(ns[1].strip() + ' ' + ns[0].strip())
        elif len(ns) == 1:
            new_authors.append(ns[0])
        else:
            # should not happen
            new_authors.append(a.strip())

    # if you modify here, you should modify your template
    #return ' and '.join(new_authors)
    return new_authors


# TODO use bibtexparser library customizations
# see https://bibtexparser.readthedocs.org/en/latest/tutorial.html#parsing-the-file-into-a-bibliographic-database-object

HYPEN_HYPEN = u'\u2013' # -- in LaTeX
PAGES_RE = re.compile(r'(?P<begin>[0-9]+)-+(?P<end>[0-9]+)')

def decorate_pages(pages):
    m = PAGES_RE.match(pages)
    if m:
        return m.group('begin') + HYPEN_HYPEN + m.group('end')

    # if not match return
    return pages


def decorate_entries(entries):
    for entry in entries:
        if 'author' in entry:
            entry['author'] = decorate_author(entry['author'])

        if 'pages' in entry:
            entry['pages'] = decorate_pages(entry['pages'])

    return entries

def parse_bibtex(bibtex):
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    try:
        bib_database = bibtexparser.loads(bibtex, parser=parser)
    except Exception as e:
        return bibtex

    entries = decorate_entries(bib_database.entries)
    return entries

def convert_bibtex(bibtex, hl=None):
    entries = parse_bibtex(bibtex)
    return convert_bibentries_to_html(entries, hl)

def convert_bibentries_to_html(entries, hl=''):
    ''' Convert a list of bibtex entries into html

    Args: the list of entries
    '''
    render = get_template_attribute('bibtex.html', 'render_entries')
    return render(entries, hl)


def render_bib_entry(entry, hl=''):
    render = get_template_attribute('bibtex.html', 'render_entry')
    return render(entry, hl).replace('\n', '')


def render_bib_entries(entries, hl='', group_by_year=False):
    if group_by_year:
        entries = sorted(entries, key=getyear, reverse=True)
        conferences = filter(lambda e: e['ENTRYTYPE'] in ['inproceedings','proceedings'], entries)
        journals = filter(lambda e: e['ENTRYTYPE'] in ['article'], entries)

        conf_years = sorted(set([getyear(e) for e in conferences]), reverse=True)
        jour_years = sorted(set([getyear(e) for e in journals]), reverse=True)

        grouped_conf = groupby(conferences, getyear)
        grouped_jour = groupby(journals, getyear)
        try:
            render = get_template_attribute('bibtex.html', 'render_entries_group_by_year')
            return render(conf_years, grouped_conf, jour_years, grouped_jour, hl)
        except Exception as e:
            print(e)

    render = get_template_attribute('bibtex.html', 'render_entries')
    return render(entries, hl)



class Citations(object):

    def __init__(self, bibfile):
        with open(bibfile) as f:
            bibtex_str = f.read().decode('utf-8')

        self.entries = parse_bibtex(bibtex_str)


    def __getitem__(self, key):
        try:
            return next(e for e in self.entries if e.get('ID') == key or e.get('id') == key)
        except:
            raise KeyError(key)

    def render_entry(self, key, hl=''):
        entry = self.__getitem__(key)

        if not entry:
            return "No such entry with key " + key

        return render_bib_entry(entry, hl)

    def render_entries(self, keys, hl='', group_by_year=False):
        entries = filter(lambda e: e.get('ID') in keys or e.get('id') in keys, self.entries)
        return render_bib_entries(entries, hl)


    def render_all(self, hl='', group_by_year=False):
        return render_bib_entries(self.entries, hl, group_by_year)



