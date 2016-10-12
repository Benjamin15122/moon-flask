# READ ME

## NOTE

1. `yaml.load` may return `None` if the yaml file is empty.
2. `sys.setdefaultencoding` may not work in Docker. Remove it and explicit decode and encode `str` and `unicode`.

    Some I/O may convert a `str` into `unicode` and than byte array

3. Currently, we load all small files on demand and cache them.
   (See `install_content_hook`)
   Keep those `yaml` files in small sizes and build an archive version
   once they become bigger than bigger.

   Note that **ARCHIVE** is not implemented yet.

## TODO

1. publications.html + bibtexparser
1. a proxy that embed web pages of changxu, yuhunag
1. A set of basic templates that generates pages from yaml 
1. tags and category of news

## Install

Dependencies:

1. markdown
2. bibtexparser
3. docutils

## Update

Do Not Use **crond**

See http://lab.artemisprojects.org/help/web_hooks/web_hooks

## Manage

Step to add a user

Suppose that you want to add an entry for Tom.

1. Create a project for Tom at gitlab in the group **moon**, with name `moon-tom`
2. Give the **Developer** previlege to Tom.
3. Add the submodule:

        git submodule add git@git.artemisprojects.org:moon/moon-tom.git pages/tom

4. Edit `pages/people.yaml` and add an entry. You can learn from other entries.

