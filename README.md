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


## 重构计划

### 基本设计

整个系统只有一个template (`doc.html`)，所有页面元素均为Markdown控制。特殊页面内容以插件形式渲染。

实现在`moon/newview.py`。

### 插件

插件存放在`moon/extensions/`。

* 已经支持的插件：
    * latex: 将`$...$`和`$$...$$`替换为公式。
* 开发中的插件：
    * index: 将单行`[INDEXPAGE]`替换为主页。
* 计划开发的插件：
    * bibtex: 显示一个参考文献。支持作者高亮。

