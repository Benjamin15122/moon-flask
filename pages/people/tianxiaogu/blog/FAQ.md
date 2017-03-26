title: FAQ
date: 2016-12-12
author: tianxiaogu
category: programming
tags: java
template: post.html



## Maven

### maven下载速度慢？

国内用阿里云的源速度会飞快，直接修改`settings.xml`，找到`mirrors`一项，添加阿里云地址。

~~~{.xml}
<mirror>
    <id>nexus-aliyun</id>
    <mirrorOf>*</mirrorOf>
    <name>Nexus aliyun</name>
    <url>http://maven.aliyun.com/nexus/content/groups/public</url>
</mirror>
~~~

### `*-SNAPSHOT-*`依赖无？

这个一般发生在编译一个临时版本出现的问题，
最简单的就是直接先`mvn install`，安装一个临时版本。

### 避免一些测试、检查导致构建失败

* Test, `-Dmaven.test.skip`
* RAT, `-Drat.skip`

### Maven运行程序

1. 直接运行


~~~
mvn exec:java -Dexec.mainClass="com.example.Main"
~~~

2. 生成classpath


~~~
mvn dependency:build-classpath -Dmdep.outputFile="classpath.txt"
~~~

## Bash

1. 获取脚本当前目录


~~~
DIR=$(pushd "$(dirname "$BASH_SOURCE[0]")" > /dev/null && pwd -P && popd > /dev/null)
~~~

## VIM


### 删除特定行

* `v/\.class/d`: 删除不包含`.class`字符的行
* `g/\.class/d`: 删除包含`.class`字符的行
* `g/^$/d`: 删除空白行

## 项目编译

### JDK 1.4的enum问题

* `find -name *.java -exec sed -i "s/\<enum\>/enum1/g" {} \;`

### Bug Report和Patch Commit无关联

一些项目可能经过CVS、SVN，最终转成了GIT，
所以Bug Report里的fix commit无法和GIT的commit映射起来。
此外，一些Bug Report系统会由bugzilla转为jira，因此Bug的ID也无法对应，
这个时候我们就需要猜出哪个GIT的commit和哪个Bug相关。

1. 根据Bug ID搜索
2. svn2git会包含svn的commit id，根据svn commit id搜索
3. 根据Author搜索，因为一些人可能会参与项目然后退出
4. 根据Bug Report的时间搜索
5. 根据Bug Report的关键字搜索，一般异常名和出现问题的类名。

