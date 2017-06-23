title: 使用说明

# 使用说明


## 网站架构

moon主要用于软件所成员的个人主页的编写和发布。
我们采用`markdown`为主要的文档编写格式，而通过`git`来发布。

moon需要两台服务器协作

* 作为Web服务器的<http://moon.nju.edu.cn>
* 作为GitLab服务器的<http://git.njuics.cn>

!!! warning "注意："
    本文的【GitLab服务器】以及【GitLab账号】不是指的是<https://about.gitlab.com/>以及其上的账号，
    而是指的我们搭建的<https://git.njuics.cn>以及其上的账号，感谢曹总提供`njuics.cn`的域名支持。

用户所有的编辑修改都是需要push到GitLab服务器上，
然后Web服务器检测到更新之后将数据从GitLab抓取到Web服务器本地，最终通过Web服务器展现出更新。
具体而言，我们利用了GitLab的webhook功能。
当有新的内容push到GitLab服务器时，对应项目的webhook会被触发，
进而触发Web服务器向GitLab服务器请求新数据。

* `moon-flask`: 包含站点全局的信息、内容、数据、代码。




## 快速使用步骤

1. 确认自己的[njuics](git.njuics.cn)的GitLab用户名，无账户在QQ群里吼一声，联系GitLab管理员创建。
    * 最好在自己机器上通过配置sshkey免密码访问GitLab
    !!! note "说明："
        由于学校限制使用22端口，因此我们需要将`git.njuics.cn`配置为2222端口，具体见[【配置GitLab】](#configure-gitlab)。
2. 联系管理员，将自己的信息加入到[people](/people/)页面。
    * 提供姓名、入学年份、博士研究生或硕士研究生或本科生、头像avatar。
3. 管理员会将你加入GitLab上的`moon-flask`项目，确认自己有权限了，克隆项目。

        git clone git@git.njuics.cn:moon/moon-flask.git
!!! warning "注意："
    每个人都会在`moon-flask/pages/people/`下有一个文件夹

4. 创建自己的页面，最直接的方式是拷贝已有师兄的复制修改。
    * 例如张三可以复制`yaojingwang`目录，将其重命名为`sanzhang`，管理员会默认将其页面指向`/people/sanzhang/`
    !!! note "说明："
        这里推荐拷贝[孟占帅](/people/zsmeng)，即目录`zsmeng`。
5. 学习如何[添加、修改、编辑主页内容](#writing)：
    * 了解[moon-flask的目录结构](#folder-structure)，以学会如何添加文件，通过URL访问文件。
    * 了解[markdown](#markdown)，了解Parser支持的特性。
    * 了解[List](#list)，学会如何创建多级列表。
    * 了解[Boostrap](#bootstrap)，学会如何创建表格以及responsive的内容。
    * 了解[Font-awesome](#icon)，学会如何插入丰富的矢量图标。
    * 了解[bibtex](#bibtex)，如果通过bibtex的内容展示你的论文列表
    * 查看其他人的主页的内容是如何撰写的，例如这篇[使用说明](https://git.njuics.cn/moon/moon-flask/raw/master/pages/userguide.md)
6. 最后，通过`git`递交和上传自己的修改。

    !!! note "说明："
        因为是多人协同项目，但是各自一般只修改自己的目录下的内容，因此存在不能自动合并的冲突的情况十分少见。
        因此，建议每次先commit，再pull，然后再push。

            git commit -am "Update xxx"
            git pull origin master
            git push origin master

-------------

!!! note "说明："
    当前管理员有顾天晓、蒋炎岩、孟占帅

!!! warning "注意："
    所有文件必须保存为无BOM的UTF-8编码，尤其Windows用户。

### 高级用户使用说明

需要在本地调试的成员可以按照如下步骤

1. 在机器上安装`python2`，目前`moon-flask`一直在`python2`环境下开发，对于`python3`有一些不兼容的地方。
2. 克隆`moon-flask`项目
3. 查看`README.md`, 安装对应的Python依赖包
4. 启动系统`python moon.py`
5. 打开浏览器，访问`localhost:8000/userguide`


## <a name="writing"></a>编写主页

### <a name="folder-structure"></a>目录结构

每个人都有一个目录，这个目录的名字一般是拼音的全拼小写，例如王瑶菁的就是`yaojingwang`。

~~~
moon-flask/pages/people/
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

!!! note "说明："
    在markdown文档里，建议使用相对路径，因为每一个markdown的地址是固定的，这样可以保持文档简洁，而且在服务端可以很容易的解析到绝对路径。
    而在其余文件里(例如，配置文件，bibtex文件)，建议使用完整路径或者完整的URL。
    因为这些内容可能会在多处出现，因此相对路径是不稳定的。
    另外，moon的域名一般来说不会更改，实在不清楚就使用完整的URL链接。



### <a name="markdown"></a>Markdown

文档采用`markdown`，使用的parser是python中的[markdown](https://pythonhosted.org/Markdown/index.html)，支持的[extension](https://pythonhosted.org/Markdown/extensions/index.html)主要有

* `markdown.extensions.extra`
* `markdown.extensions.meta`
* `markdown.extensions.admonition`
* `markdown.extensions.codehilite`
* `markdown.extensions.toc`

所以，如果你通过第三方或者其他的`markdown`编辑器预览你的文档，可能和最终moon上出现的不一致。

### 文档编码

所有的文件必须满足如下条件

1. `.md`结尾，我们根据这个模式映射其为html
2. `utf-8`**无BOM**编码。BOM编码会在文件开头加几个字符，造成markdown插件解析失败。
3. `unix`行尾。

以上几点Windows用户需要特别注意。


### 文档结构

文档开头的部分是元数据定义，不会出现在正文中，至少提供`title`。

~~~{.markdown}
title: Yaojing Wang

# Yaojing Wang

...
~~~


!!! warning "注意："
    `title: Yaojing Wang`里面存储的是原始的meta data，不支持任何`html`以及`markdown`的style。



### <a name="list"></a>List

特别需要注意的是多级列表需要四个空格：

~~~{.markdown}
* 第一层
    * 第二层
        * 第三层
~~~

* 第一层
    * 第二层
        * 第三层

### <a name="list"></a>Bootstrap


moon通过[bootstrap](http://getbootstrap.com/)支持Mobile和responsive的效果。
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

### <a name="icon"></a>Font-Awesome

通过font-awesome可以实现插入矢量icon，具体的查看[example](http://fontawesome.io/examples/)。

* `<i class="fa fa-bitbucket"></i>`可以得到<i class="fa fa-bitbucket"></i>

### <a name="bibtex"></a>bibtex

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


如果你论文很多，可以将bibtex存在一个`.bib`文件里，然后通过`jinja2`插件调用`render_bib_file`渲染。

例如[姚老师](/people/yuanyao)的主页就是通过如下语句，显示【selected publications】

~~~
{{ render_bib_file('yuanyao.bib', ['TKDE16', 'KDD16', 'IJCAI15', 'TKDE14', 'KDD14', 'CIKM14', 'WWW13'], hl='Yuan Yao') }}
~~~

!!! note "说明："
    `yuanyao.bib`是相对位置。



## <a name="configure-gitlab"></a>配置GitLab

1. 配置使用SSH Key，具体见<https://git.njuics.cn/help/ssh/README#generating-a-new-ssh-key-pair>
2. 编辑或创建`~/.ssh/config`，添加如下内容，将端口设置为2222。

        Host git.njuics.cn
        Port 2222

3. 通过链接<git@git.njuics.cn:moon/moon-flask.git>克隆项目，已经克隆的项目可以更改remote

        git remote rm origin
        git remote add origin git@git.njuics.cn:moon/moon-flask.git

## 使用扩展

moon目前支持如下扩展

- `qqmap`
- `math`（katex）
- `flowchart`以及其依赖的`raphael`[【用例】](/test/flowchart)

此外，还支持jQuery，可以通过customjs来实现，所有代码将会在页面结尾插入。

例如，以下代码会将所有的table添加css类，并设置其宽度为100%。

```{.js}
~~~{.customjs}
// add Bootstrap css class via jQuery
$('table').addClass('table-responsive').addClass('table').addClass('table-bordered').css('width', '100%')
~~~
```

