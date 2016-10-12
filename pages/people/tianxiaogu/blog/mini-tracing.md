title: MiniTracing
date: 2015-10-25
category: programming
tags: java,android
template: post.html
status: draft


最近因为科研需要，花了几天时间，自己修改HotSpot JVM实现了一个MiniTracing。
这个tracing工具主要记录method的entry和exit事件，此外还有object allocation事件。
做这件事情的目的是为了得到**每一个**对象创建时的call string，也就是stack trace。
我的方法就是先记录method的entry和exit，然后分析日志构造出call string。

这个工具和JVMTI相似，不过更加暴力。JVMTI只在未编译的方法的开始和结尾处fire event，而且要把封装好数据以供callback处理。
而我直接存储的是原始地址，所以在GC中移动对象的时候，我还要记录所有的移动，所幸GC的设计就是考虑到减少移动的，所以这个移动对象的log并不是很大。

我为每一个线程设计了一个固定大小的Buffer用于快速写入时间，直觉上来看写入buffer肯定比写入I/O要快，
但是这个Buffer的实现能否带来效率提升还是一个未知数，因为我代码写的很随意。

此外，我也没有为assembly那块做任何优化，所以任何的`call`指令之前都是`push_CPU_state`。

跑了单线程的dacapo h2 benchmark，也就是`java -jar dacapo.jar -t 1 -n 1 h2`，时间由3秒多飙升到30多秒。
由于我改了代码生成，所以要设置一个恰当好处的`InlineSmallCode`去控制Inline的方法。
这里我的`InlineSmallCode`设置为了1800，而原始值在我的机器上则为1000，这样下来，刚刚那个h2的benchmark会有一个接近10GB的二进制log文件。

项目地址见[MiniTracing](http://lab.artemisprojects.org/tianxiaogu/mini-tracing)，具体用法可以参见`README.md`。

