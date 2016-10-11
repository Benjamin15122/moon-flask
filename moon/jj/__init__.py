from moon import app
from moon.jj.bibtex import render_bib_entry, render_bib_file

from moon.jj.urls import render_parent_breadcrumb

app.jinja_env.globals.update(render_parent_breadcrumb=render_parent_breadcrumb)
app.jinja_env.globals.update(render_bib_entry=render_bib_entry)
app.jinja_env.globals.update(render_bib_file=render_bib_file)
