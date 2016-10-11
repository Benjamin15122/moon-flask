
from flask import request, url_for, g

def render_parent_breadcrumb():
    endpoint = request.endpoint

    path_list = [['Home', url_for('index')]]

    if endpoint == 'page':
        name = request.view_args.get('name')
        path = request.view_args.get('path')

        people = g.site.find_people_by_url(name)

        path_list.append(['People', url_for('people')])
        if path and path.startswith('blog/'):
            path_list.append([people.get('name'), url_for('page', name=name)])
            if path != 'blog/':
                path_list.append(['Blog', url_for('page', name=name, path='blog/')])


    return '    \n'.join(['<li><a href="{1}">{0}</a></li>'.format(*e) for e in path_list])

