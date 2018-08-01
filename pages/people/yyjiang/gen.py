import yaml, bibtexparser

def render(name, id, p, fname):
  lines = [
    f'title: {p.title}\n',
    f'## {p.title}\n',
    f'> {{{{ render_bib_entry(g.site.spar_paper.{id}, hl="Yanyan Jiang") }}}}\n',
  ]
  if 'desc' in p.__dict__:
    lines += [f'{p.desc}\n']

  with open(fname, 'w') as fp:
    fp.write('\n'.join(lines))

parser = bibtexparser.bparser.BibTexParser()
parser.customization = bibtexparser.customization.convert_to_unicode
db = {}

class Paper:
  pass

for p in bibtexparser.load(open('../../spar/spar.bib'), parser=parser).entries:
  paper = Paper()
  for (k, v) in p.items():
    setattr(paper, k.lower(), v)
  db[paper.id] = paper
  
for (name, values) in yaml.load(open('papers.yaml', 'r')).items():
  id = values['id']
  for (k, v) in values.items():
    setattr(db[id], k, v)
  paper = db[id]
  render(name, id, paper, 'pubs/{0}.md'.format(name))
  print(name, '-', paper.title)