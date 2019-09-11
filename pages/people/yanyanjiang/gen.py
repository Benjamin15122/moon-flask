#!/usr/bin/env python3

import yaml, bibtexparser
from pydot import *

db = {}

class Paper:
  pass

def load_yaml(fname):
  return yaml.load(open(fname, 'r'))

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

# Load all papers in spar.bib

parser = bibtexparser.bparser.BibTexParser()
parser.customization = bibtexparser.customization.convert_to_unicode

for p in bibtexparser.load(open('../../spar/spar.bib'), parser=parser).entries:
  paper = Paper()
  for (k, v) in p.items():
    setattr(paper, k.lower(), v)
  db[paper.id] = paper

# Load all papers in paper.yaml

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

# Render each paper's markdown file

for p in papers():
  render(p, f'pubs/{p.name}.md')

# Render homepage diagram

gv = Dot(rankdir="TB", layout='dot', compound=True, splines=True, remincross=True)
gv.set_node_defaults(color='lightgray', style='filled', shape='Mrecord',
                     fontsize='14')

g = load_yaml('graph.yaml')

nodes = {}
for nd in g['nodes']:
  id = nd['id']
  node = Node()
  node.set_name(id)

  desc = ''
  if 'desc' in nd:
    desc = f'<br></br><font color="#606060" point-size="11" face="Arial">{nd["desc"]}</font>'
  node.set('label', f'< <table><tr><td>{nd["name"]}{desc}</td></tr></table>>')
  gv.add_node(node)
  nodes[id] = node

for eg in g['edges']:
  (fr, dir, to) = eg.strip().split(' ')
  gv.add_edge(Edge(nodes[fr], nodes[to]))

clusters = {}
for nd in g['nodes']:
  node = nodes[nd['id']]
  if 'path' in nd:
    path = nd['path'].split('/')
    for cl_name in path:
      if cl_name not in clusters:
        clusters[cl_name] = Cluster(cl_name)
      cl = clusters[cl_name]
      cl.add_node(node)
    #gv.add_subgraph(clusters[path[0]])

for cl_obj in g['clusters']:
  cl = clusters[cl_obj['id']]
  cl.set_label(cl_obj['label'])
  cl.set_fontsize(14)
  cl.set_fontname('Arial')
  cl.set_pack(True)

gcl = Cluster()
S = set()

def add_subgraph(fr, to):
  if (fr, to) not in S:
    fr.add_subgraph(to)
    S.add((fr, to))

for nd in g['nodes']:
  if 'path' in nd:
    path = nd['path'].split('/')
    for (i, cl_name) in enumerate(path):
      if i == 0:
        add_subgraph(gcl, clusters[path[i]])
      else:
        add_subgraph(clusters[path[i-1]], clusters[path[i]])

# Hack: add invisible edges
gcl.add_edge(Edge('scs', 'abc', style="invis"))
gcl.add_edge(Edge('scs', 'enter', style="invis"))

gv.add_subgraph(gcl)


gv.write_svg('summary.svg')
print(gv.to_string())
