
from flask import request, url_for, g


ORDERED_BREADCRUMB = [
        # Second level
        ['dse/', 'DSE'],
        ['news/', 'News'],
        ['events/', 'Events'],
        # Third level
        ['dse/javelus/', 'Javelus'],
        ['dse/aotes/', 'AOTES'],
        ]



def render_parent_breadcrumb():
    ''' Hard coded breadcrumb
        TODO: scan the page fold to collect title or short title of each index.md
    '''
    endpoint = request.endpoint

    path_list = [['Home', url_for('page')]]

    if endpoint == 'page':
        path = request.view_args.get('path')
        name = request.view_args.get('name')

        if name:
            path_list.append(['People', url_for('page', path='people/')])
            people = g.site.find_people_by_url(name)

            if people and path and path != 'index':
                path_list.append([people.get('name'), url_for('page', name=name)])
                if path != 'blog/' and path.startswith('blog/'):
                    path_list.append(['Blog', url_for('page', name=name, path='blog/')])
        elif path:
            for s in ORDERED_BREADCRUMB:
                if path.startswith(s[0]) and path != s[0]:
                    path_list.append([s[1], url_for('page', path=s[0])])

        else:
            # Hide breadcrumb in home page
            return ''


    return '    \n'.join([u'<li><a href="{1}">{0}</a></li>'.format(*e) for e in path_list])


def static_for(filename):
    return url_for('static', filename=filename)


def page_for(name=None, path=None):
    return url_for('page', name=name, path=path)
