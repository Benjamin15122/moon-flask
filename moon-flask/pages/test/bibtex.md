title: A test page for bibtex

-----------------

{{ render_bib_entry(g.site.paper['Huang:2014:NSR']) }}

-----------------

{{ render_bib_file(None) }}

-----------------

{{ render_bib_file(None, group_by_year=True) }}

-----------------

{{ render_bib_file('test.bib') }}

-----------------

{{ render_bib_file('test.bib', 'Huang:2014:NSR') }}

-----------------

{{ render_bib_file('test.bib', ['Huang:2014:NSR', 'Huang:2014:NSR', 'Xi:2014:APSEC']) }}
