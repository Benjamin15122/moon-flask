title: MiniTrace for Android ART
date: 2016-12-12
category: programming
tags: java,android
template: post.html


我在Android的虚拟机内部实现了一个统计指令覆盖率的工具。
简而言之，我将一些方法标记为`traceable`，
然后强制让这些方法解释执行。
这样我修改后的解释器就能将执行过的指令记录下来了。
这种做法是显然低效率的，
但是我实际应用速度还是能够忍受的，
取决于有多少比例的方法是解释执行的。



这个工具分两个项目，
第一个项目是修改后的ART，第二个用于解析生成的日志文件。

* [MiniTrace for Android ART](https://bitbucket.org/txgu/mini-tracing-art6)
* [Android Toolkit](https://bitbucket.org/txgu/android-toolkit)：用于解析记录的信息



## 编译

**To be added**

## 安装

**To be added**

## 使用

使用该工具统计覆盖率需要如下几个步骤。

1. 准备配置文件和数据文件
2. 丰收记录的覆盖率信息
3. 解析记录的覆盖率信息

### 准备配置文件和数据文件

使用MiniTrace需要配置哪些应用中的哪些类中的方法需要记录覆盖信息。
由于所有应用执行的art进程都是从zygote进程fork来的，
因此我修改了art，
使得其在fork之后的初始化阶段读取特定的配置文件，
来判定是否需要进行覆盖率统计。
此外， 我还将运行时刻记录的数据写进文件里。

但是由于并不是所有的app都有读写`sdcard`的权限。
为此，我之前的做法是修改framework里的fork相关代码，
在fork之后将`sdcard`等权限赋给该应用。
但由于这部分代码在另外的子项目中，
为了避免维护太多修改，
我目前采用了另外一种做法，
即将所有记录的文件写到`data`目录里去。

我对Android的安全机制没有深入研究，
只知道有一部分是基于linux用户组管理模型，有一部分是基于selinux的。
一个应用属于一个用户和用户组，
因此，我们只要通过`chown`命令将文件权限设置为应用对应的用户，
那么该应用就有读写该文件的权利了。
为了开发方便，我将所有的配置文件和存储收集的信息的文件放在`/data/`目录下，
并将其**事先（即运行应用之前）创建好文件再通过`chown`命令修改好权限**。
我不将文件直接放在`sdcard`里是因为`sdcard`的文件系统不支持修改文件属性。
另外，因为我直接将文件存在`/data/`目录下，
我们还需要通过如下命令绕开selinux的限制。

~~~
adb shell su -c setenforce 0
~~~

目前需要下面四个文件，其中UID为应用对应的用户ID，一般为一个五位数。
获取应用的UID有很多方式，这里就不用赘述了。

* 配置文件
    1. `/data/mini_trace_${UID}_config.in`: 配置文件。
* 数据文件
    1. `/data/mini_trace_${UID}_coverage.dat`: 记录了方法的覆盖信息的文件。
    2. `/data/mini_trace_${UID}_data.bin`: 记录方法执行和对象访问的信息，暂时未完全移植成功。
    3. `/data/mini_trace_${UID}_info.log`: 记录方法执行和对象访问的信息，暂时未完全移植成功。

为了方便在windows下也使用该工具，
我提供一个Python脚本文件去准备这四个文件。
其中配置文件只要存在就会出发记录，
而数据文件会在每次写数据的时候覆盖。

1. [`push_config.py`](https://bitbucket.org/txgu/android-toolkit/src/master/minitrace/scripts/push_config.py?at=master&fileviewer=file-view-default)


默认在读到配置文件存在的时候就会开启各种trace功能，
所以用户使用的时候一般不需要做任何配置，
这里就不赘述各种细节的配置即可，感兴趣的用户可以参照代码。

默认的配置（即配置文件是空白文件）会做如下事情：

1. 将所有**不是来自于`/system/framework/`**里的dex文件中的**所有类中的所有方法**都标记为`traceable`。
2. 解释执行标记为`traceable`的所有方法，记录每条执行过的指令。

### 丰收记录的覆盖率信息

我通过信号USR2来dump所有记录的覆盖信息，
用户只要通过`kill`命令根据`pid`向目标进程请求即可。
进程接收到USR2信号之后会将记录的所有覆盖率信息写入并覆盖到文件
`/data/mini_trace_${UID}_coverage.dat`。
因此，dump之后用户需要尽快将`/data/mini_trace_${UID}_coverage.dat`拷贝备份。

我一般的做法是先通过ps命令找寻进程的`pid`，用户也可以通过logcat分析日志获得。

~~~
adb shell su -c ps | grep xxx
~~~

再通过`kill`命令请求dump。

~~~
adb shell su -c kill -USR2 $PID
~~~

为了方便知晓何时dump结束，
我打印了两条信息用于标记dump的开始和结束。
具体代码如下：

~~~
void SignalCatcher::HandleSigUsr2() {
  LOG(INFO) << "SIGUSR2 dumping coverage data begin";
  MiniTrace::DumpCoverageData();
  LOG(INFO) << "SIGUSR2 dumping coverage data end";
}
~~~

因此，用户当通过logcat监控到`SIGUSR2 dumping coverage data end`就可以知晓何时dump结束了。


### 解析记录的覆盖率信息

我提供了一个Java解析项目，通过maven管理，具体的选项可以参照类[`CoverageDataParser`](https://bitbucket.org/txgu/android-toolkit/src/master/minitrace/minitrace/src/main/java/org/javelus/minitrace/android/coverage/CoverageDataParser.java?at=master&fileviewer=file-view-default)。


