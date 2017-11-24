import yaml, bibtexparser

papers = [
    ('survey', 'jiang_approaches_2017'),
    ('aattplus', 'wang_aatt_2017'),
    ('repdroid', 'yue_repdroid_2017'),
    ('c3', 'jiang_crash_2016'),
    ('bc', 'jiang_online_2016'),
    ('aatt', 'li_effectively_2016'),
    ('gat', 'wu_testing_2016'),
    ('gain1', 'sui_hybird_2016'),
    ('rwtrace', 'jiang_optimistic_2015'),
    ('comedy', 'jin_concolic_2015'),
    ('abc', 'zhang_abc_2015'),
    ('att', 'meng_facilitating_2015'),
    ('cosedroid', 'wu_cosedroid_2015'),
    ('care', 'jiang_care_2014'),
    ('uga', 'li_user_2014'),
    ('gain', 'sui_gain_2014'),
]

def render(name, id, p, fname):
    with open(fname, 'w') as fp:
        print >> fp, '## {0}'.format(p.title)
        print >> fp
        print >> fp, '{{{{ render_bib_entry(g.site.spar_paper.{0}, hl="Yanyan Jiang") }}}}'.format(id)
        if 'abstract' in p.__dict__:
            print >> fp
            print >> fp, "#### Abstract"
            print >> fp, p.abstract.encode('utf-8')



parser = bibtexparser.bparser.BibTexParser()
parser.customization = bibtexparser.customization.convert_to_unicode
db = {}

class Paper:
    pass

for p in bibtexparser.load(open('../../spar/spar.bib'), parser=parser).entries:
    paper = Paper()
    for (k, v) in p.items():
        paper.__dict__[k.lower()] = v
    db[paper.id] = paper
    

for p in papers:
    render(p[0], p[1], db[p[1]], 'pubs/{0}.md'.format(p[0]))


