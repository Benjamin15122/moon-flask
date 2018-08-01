import yaml, bibtexparser
from pydot import *

def load_yaml(fname):
  return yaml.load(open('papers.yaml', 'r'))

def render(p, fname):
  lines = [
    f'title: {p.title}\n',
    f'## {p.title}\n',
    f'> {{{{ render_bib_entry(g.site.spar_paper.{p.id}, hl="Yanyan Jiang") }}}}\n',
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
  
for (name, values) in load_yaml('papers.yaml').items():
  id = values['id']
  p = db[id]
  p.name = name
  for (k, v) in values.items():
    setattr(p, k, v)

def papers():
  for (id, p) in db.items():
    if hasattr(p, 'name'): # exist in yaml
      yield p

for p in papers():
  render(p, f'pubs/{p.name}.md')

G = Dot()

for p in papers():
  G.add_node(Node(p.name))

G.write_png('summary.png')