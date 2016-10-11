from moon import app
from moon.jj.bibtex import render_bib_entry, render_bib_file

app.jinja_env.globals.update(render_bib_entry=render_bib_entry)
app.jinja_env.globals.update(render_bib_file=render_bib_file)
