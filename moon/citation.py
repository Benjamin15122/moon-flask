import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


#############################################
# Bibtex Support (reStructuredText only)
#############################################

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives

def convert_bibtex(bibtex, hl):
    parser = BibTexParser()
    parser.customization = convert_to_unicode
    try:
        bib_database = bibtexparser.loads(bibtex, parser=parser)
    except:
        return bibtex

    return convert_bibentries_to_html(bib_database.entries)

ip_temp = Template('<li><a name="$id"></a><b>$title</b>,$author,<em>$booktitle</em>,$pages,$month $year</li>')

def render_interproceedings(e):
    '''Generate HTML for an bibtex inproceedings entry

    Args:
        e is a dict
    '''
    if 'month' not in e:
        e['month'] = ''
    return ip_temp.substitute(e)



def render_article(e):
    '''Not implemented
    '''
    pass

def isEntry(e, t):
    ''' check wether a bibtex entry is the specified type

    Args:
        e, the bibtex entry represented by a dict
        t, the specified type string, e.g., 'inproceedings'
    '''
    return e.get('type') == t

def convert_bibentries_to_html(entries):
    ''' Convert a list of bibtex entries into html

    Args: the list of entries

    Result:
        a HTML string 

        <ol>
            <li>entry html</li>
        </ol>
    '''
    html = []
    html.append('<ol>')
    for e in entries:
        if isEntry(e, 'inproceedings'):
            html.append(render_interproceedings(e))
        elif isEntry(e, 'article'):
            html.append(render_article(e))
        else:
            html.append(' '.join(e.values()))

    html.append('</ol>')

    return '\n'.join(html)

class BibtexDirective(rst.Directive):
    '''A reStructuredText directive to support generate HTML for bibtex entries

    Usage:
        .. bibtex::

            @inproceedings{an_id,
              title = {A title},
              booktitle = {a proceeding},
              author = {Xiaoming and Xiaohong}
              years = {2015}
            }

        will be converted into an html
    '''

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'hl': directives.unchanged}
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        b = convert_bibtex(text, self.options.get('hl', ''))
        n = nodes.raw(rawsource=self.block_text, text=b, format='html')
        return [n]

# Register this directive into docutils
directives.register_directive('bibtex', BibtexDirective)

################



