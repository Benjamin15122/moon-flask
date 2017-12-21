import yaml, bibtexparser

def render(name, id, p, fname):
    with open(fname, 'w') as fp:
        print >> fp, 'title: {0}'.format(p.title)
        print >> fp
        print >> fp, '## {0}'.format(p.title)
        print >> fp
        print >> fp, '> {{{{ render_bib_entry(g.site.spar_paper.{0}, hl="Yanyan Jiang") }}}}'.format(id)
        if 'desc' in p.__dict__:
            print >> fp
            print >> fp, p.desc.encode('utf-8')

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
    

for (name, values) in yaml.load(open('papers.yaml', 'r')).items():
    id = values['id']
    for (k, v) in values.items():
        db[id].__dict__[k] = v
    render(name, id, db[id], 'pubs/{0}.md'.format(name))


