title: 使用说明

# 使用说明

moon主要用于软件所成员的个人主页的编写和发布。
我们采用`markdown`为主要的文档编写格式，而通过`git`来发布。

这篇文档主要是针对通过项目`moon-share`，`spar`用户请咨询[Yanyan Jiang](/spar/peoples/yyjiang/)

## 快速使用步骤

1. 确认自己的[njuics](git.njuics.cn)的gitlab用户名，无账户在QQ群里吼一声，联系gitlab管理员创建。
2. 联系管理员，将自己的信息加入到[people](/people/)页面。
    * 提供姓名、入学年份、博士研究生或硕士研究生或本科生、头像avatar。
3. 管理员会将你加入gitlab上的`moon-share`项目，确认自己有权限了，克隆[moon-share](https://git.njuics.cn/moon/moon-share)
4. 创建自己的页面，最直接的方式是拷贝已有师兄的复制修改。
    * 例如张三可以复制`yaojingwang`目录，将其重命名为`sanzhang`，管理员会默认将其页面指向`/people/sanzhang/`
5. 最后，通过`git`递交和上传自己的修改。

!!! note "说明："
    当前管理员有顾天晓、蒋炎岩、孟占帅

## 目录结构

每个人都有一个目录，这个目录的名字一般是拼音的全拼小写，例如王瑶菁的就是`yaojingwang`。

~~~
moon-share/
    |
    +---yaojingwang/
    |         |
    |         +---index.md
    |         |
    |         +---publication.md
    |         |
    |         +---static/
    |         |      |
    |         |      +---pic.jpg
    |         +---paper1.pdf
    |
    +---zelinzhao/
~~~

文档按照如下规则解析：


* `http://moon.nju.edu.cn/people/yaojingwang`、`http://moon.nju.edu.cn/people/yaojingwang/`和`http://moon.nju.edu.cn/people/yaojingwang/index`会显示`index.md`对应的文档
* `http://moon.nju.edu.cn/people/yaojingwang/publication`会显示`publication.md`对应的文档
* `http://moon.nju.edu.cn/people/yaojingwang/publication/`会导致404
* `http://moon.nju.edu.cn/people/yaojingwang/paper1.pdf`会下载`paper1.pdf`

## 编写主页

文档采用`markdown`，使用的parser是python中的[markdown](https://pythonhosted.org/Markdown/index.html)，支持的[extension](https://pythonhosted.org/Markdown/extensions/index.html)主要有

* `markdown.extensions.extra`
* `markdown.extensions.meta`
* `markdown.extensions.admonition`
* `markdown.extensions.codehilite`
* `markdown.extensions.toc`

所以，如果你通过第三方或者其他的`markdown`编辑器preview你的文档，可能和最终moon上出现的不一致。


文档开头的部分是元数据定义，不会出现在正文中，至少提供`title`。

~~~{.markdown}
title: Yaojing Wang

# Yaojing Wang

...
~~~


## List

特别需要注意的是多级列表需要四个空格：

~~~{.markdown}
* 第一层
    * 第二层
        * 第三层
~~~

* 第一层
    * 第二层
        * 第三层

## Bootstrap


moon通过[bootstrap](http://getbootstrap.com/)支持mobile和responsive的效果。
最常用的就是[Grid system](http://getbootstrap.com/css/#grid-example-basic)。

~~~{.html}
<div class="row gutter" markdown="1">
<div class="col-lg-2 col-md-2 col-sm-12">
![](/people/tianxiaogu/static/tianxiaogu.png "Tianxiao Gu")
</div>
<div class="col-lg-10 col-md-10 col-sm-12" style="vertical-align:middle">
<ul>
<li>[Dynamic Software Evolution Group](/dse/)
<li>[Institute of Computer Software](http://moon.nju.edu.cn), [Nanjing University](http://www.nju.edu.cn)
<li>[Department of Computer Science and Technology](http://cs.nju.edu.cn), [Nanjing University](http://www.nju.edu.cn)
<li>Address: Room 812, Computer Science and Technology Building
<li>Email: tianxiao.gu (at) gmail dot com
<li>
  [<i class="fa fa-linkedin-square"></i>]("http://www.linkedin.com/in/tianxiaogu")
  [<i class="fa fa-twitter-square"></i>]("https://twitter.com/Xiaotiangu")
  [<i class="fa fa-facebook-square"></i>]("https://www.facebook.com/eric.ku.505")
  [<i class="fa fa-bitbucket"></i>]("https://www.bitbucket.org/txgu/")
</ul>
</div>
</div>
~~~

可以得到如下内容：

<div class="row gutter" markdown="1">
<div class="col-lg-2 col-md-2 col-sm-12">
![](/people/tianxiaogu/static/tianxiaogu.png "Tianxiao Gu")
</div>
<div class="col-lg-10 col-md-10 col-sm-12" style="vertical-align:middle">
<ul>
<li>[Dynamic Software Evolution Group](/dse/)
<li>[Institute of Computer Software](http://moon.nju.edu.cn), [Nanjing University](http://www.nju.edu.cn)
<li>[Department of Computer Science and Technology](http://cs.nju.edu.cn), [Nanjing University](http://www.nju.edu.cn)
<li>Address: Room 812, Computer Science and Technology Building
<li>Email: tianxiao.gu (at) gmail dot com
<li>
  [<i class="fa fa-linkedin-square"></i>]("http://www.linkedin.com/in/tianxiaogu")
  [<i class="fa fa-twitter-square"></i>]("https://twitter.com/Xiaotiangu")
  [<i class="fa fa-facebook-square"></i>]("https://www.facebook.com/eric.ku.505")
  [<i class="fa fa-bitbucket"></i>]("https://www.bitbucket.org/txgu/")
</ul>
</div>
</div>

--------------------

!!! note "说明："
    `markdown`和`html`混合具体参照[这里](https://pythonhosted.org/Markdown/extensions/extra.html#markdown-inside-html-blocks)

## Font-Awesome

通过font-awesome可以实现插入矢量icon，具体的查看[example](http://fontawesome.io/examples/)。

* `<i class="fa fa-bitbucket"></i>`可以得到<i class="fa fa-bitbucket"></i>

## bibtex

我们通过[fenced code](https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html)来实现对bibtex的渲染。

```
~~~{.bibtexhtml hl_lines="Zelin Zhao"}
@inproceedings{gu_improving_2016,
  author    = {Tianxiao Gu and Zelin Zhao and Xiaoxing Ma and Chang Xu and Chun Cao and Jian L{\"u}},
  title     = {Improving reliability of dynamic software updating using runtime recovery},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{zhao_cure_2016,
  author    = {Zelin Zhao and Tianxiao Gu and Xiaoxing Ma and Chang Xu and Jian L{\"u}},
  title     = {CURE: Automated patch generation for dynamic software update},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{zhao_automated_2014,
    author = {Zhao, Zelin and Ma, Xiaoxing and Xu, Chang and Yang, Wenhua},
    title = {Automated Recommendation of Dynamic Software Update Points: An Exploratory Study},
    booktitle = {Proceedings of the 6th Asia-Pacific Symposium on Internetware on Internetware},
    year = {2014},
    location = {Hong Kong, China},
    pages = {136--144},
    numpages = {9},
    url = {http://doi.acm.org/10.1145/2677832.2677853},
    doi = {10.1145/2677832.2677853},
    pdf = {static/internetware-14.pdf},
}
~~~
```

上述代码会显示如下内容：

~~~{.bibtexhtml hl_lines="Zelin Zhao"}
@inproceedings{gu_improving_2016,
  author    = {Tianxiao Gu and Zelin Zhao and Xiaoxing Ma and Chang Xu and Chun Cao and Jian L{\"u}},
  title     = {Improving reliability of dynamic software updating using runtime recovery},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{zhao_cure_2016,
  author    = {Zelin Zhao and Tianxiao Gu and Xiaoxing Ma and Chang Xu and Jian L{\"u}},
  title     = {CURE: Automated patch generation for dynamic software update},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{zhao_automated_2014,
    author = {Zhao, Zelin and Ma, Xiaoxing and Xu, Chang and Yang, Wenhua},
    title = {Automated Recommendation of Dynamic Software Update Points: An Exploratory Study},
    booktitle = {Proceedings of the 6th Asia-Pacific Symposium on Internetware on Internetware},
    year = {2014},
    location = {Hong Kong, China},
    pages = {136--144},
    numpages = {9},
    url = {http://doi.acm.org/10.1145/2677832.2677853},
    doi = {10.1145/2677832.2677853},
    pdf = {static/internetware-14.pdf},
}
~~~


如果你paper很多，可以将bibtex存在一个`.bib`文件里，然后通过`jinja2`插件调用`render_bib_file`渲染。

例如[姚老师](/people/yuanyao)的主页就是通过如下语句，显示selected publications

~~~
{{ render_bib_file('yuanyao.bib', ['TKDE16', 'KDD16', 'IJCAI15', 'TKDE14', 'KDD14', 'CIKM14', 'WWW13'], hl='Yuan Yao') }}
~~~

!!! note "说明："
    `yuanyao.bib`是相对位置，不是存放在`static`里的。




