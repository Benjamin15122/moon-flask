title: Tianxiao Gu

# Tianxiao Gu



## Information

* Institute of Computer Software, Nanjing University
* Room 812, Computer Science and Technology Building
* tianxiao.gu (at) gmail dot com

<div>
<img width="200" src="static/tianxiaogu.png" alt="Tianxiao Gu"/>
</div>


## Supervisor

* Professor Jian Lü, [Xiaoxing Ma](http://moon.nju.edu.cn/~XiaoxingMa "Xiaoxing Ma"), [Chang Xu](http://cs.nju.edu.cn/changxu/ "Chang Xu"), Chun Cao

## Education and Work Experience

* 2013.9 - 2014.9: Visiting Student, University of California, Davis, [Professor Zhendong Su](http://www.cs.ucdavis.edu/~su/).
* 2012.9 - Present: Ph.D. Candidate, Department of Computer Science and Technology, Nanjing University
* 2010.9 - 2012.7: Ph.D. Student, Department of Computer Science and Technology, Nanjing University
* 2006.9 - 2010.6: B.S., Department of Computer Science and Technology, Nanjing University


## Research Interests

* Dynamic Software Updating (DSU)
* Program Analysis
* Programming Languages

## Publications

~~~{.bibtexhtml hl_lines="Tianxiao Gu"}
@inproceedings{li_effectively_2016,
  author    = {Qiwei Li and Yanyan Jiang and Tianxiao Gu and Chang Xu and Jun Ma and Xiaoxing Ma and Jian L{\"u}},
  title     = {Effectively manifesting concurrency bugs in Android apps},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{gu_improving_2016,
  author    = {Tianxiao Gu and Zelin Zhao and Xiaoxing Ma and Chang Xu and Chun Cao and Jian L{\"u}},
  title     = {Improving Reliability of Dynamic Software Updating Using Runtime Recovery},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{zhao_cure_2016,
  author    = {Zelin Zhao and Tianxiao Gu and Xiaoxing Ma and Chang Xu and Jian L{\"u}},
  title     = {CURE: Automated Patch Generation for Dynamic Software Update},
  booktitle = {Proceedings of the 23rd Asia-Pacific Software Engineering Conference (APSEC)},
  pages     = {to appear},
  year      = {2016},
}
@inproceedings{DBLP:conf/kbse/GuSMLS16,
  author    = {Tianxiao Gu and
               Chengnian Sun and
               Xiaoxing Ma and
               Jian L{\"u} and
               Zhendong Su},
  title     = {Automatic runtime recovery via error handler synthesis},
  booktitle = {Proceedings of the 31st IEEE/ACM International Conference on Automated
               Software Engineering, ASE 2016, Singapore, September 3-7, 2016},
  pages     = {684--695},
  year      = {2016},
  url       = {http://doi.acm.org/10.1145/2970276.2970360},
}
@article{DBLP:journals/infsof/GuCXMZL14,
  author    = {Tianxiao Gu and
               Chun Cao and
               Chang Xu and
               Xiaoxing Ma and
               Linghao Zhang and
               Jian L{\"u}},
  title     = {Low-disruptive dynamic updating of Java applications},
  journal   = {Information & Software Technology},
  volume    = {56},
  number    = {9},
  pages     = {1086--1098},
  year      = {2014},
  url       = {http://dx.doi.org/10.1016/j.infsof.2014.04.003},
}

@inproceedings{DBLP:conf/icse/JiangGXML14,
  author    = {Yanyan Jiang and
               Tianxiao Gu and
               Chang Xu and
               Xiaoxing Ma and
               Jian L{\"u}},
  title     = {CARE: cache guided deterministic replay for concurrent Java programs},
  booktitle = {36th International Conference on Software Engineering, ICSE '14,
               Hyderabad, India - May 31 - June 07, 2014},
  pages     = {457--467},
  year      = {2014},
  url       = {http://doi.acm.org/10.1145/2568225.2568236},
}

@inproceedings{DBLP:conf/apsec/ZhangXMGHCL12,
  author    = {Linghao Zhang and
               Chang Xu and
               Xiaoxing Ma and
               Tianxiao Gu and
               Xuezhi Hong and
               Chun Cao and
               Jian L{\"u}},
  title     = {Resynchronizing Model-Based Self-Adaptive Systems with Environments},
  booktitle = {19th Asia-Pacific Software Engineering Conference, APSEC 2012, Hong
               Kong, China, December 4-7, 2012},
  pages     = {184--193},
  year      = {2012},
  url       = {http://dx.doi.org/10.1109/APSEC.2012.62},
}

@inproceedings{DBLP:conf/apsec/GuCXMZL12,
  author    = {Tianxiao Gu and
               Chun Cao and
               Chang Xu and
               Xiaoxing Ma and
               Linghao Zhang and
               Jian L{\"u}},
  title     = {Javelus: A Low Disruptive Approach to Dynamic Software Updates},
  booktitle = {19th Asia-Pacific Software Engineering Conference, APSEC 2012, Hong
               Kong, China, December 4-7, 2012},
  pages     = {527--536},
  year      = {2012},
  url       = {http://dx.doi.org/10.1109/APSEC.2012.55},
}
~~~

## Projects

* [Javelus](http://lab.artemisprojects.org/javelus/javelus)
    * A dynamic-updating-enabled JVM
* [Ares](http://lab.artemisprojects.org/groups/ares)
    * An automatic-runtime-recovery-enabled JVM
* [AOTES](http://lab.artemisprojects.org/javelus/aotes)
    * Automating object transformations for dynamic software updating via execution synthesis
* [MiniTracing](http://lab.artemisprojects.org/tianxiaogu/mini-tracing)
    * A light-weight tracing tool built on top of the HotSpot JVM in OpenJDK 7.
    * Currently only support tracing events like method entry/exit, object allocation, object moving by GC (for identifying objects in the log).
* [MiniTracingForAndroidART](http://lab.artemisprojects.org/tianxiaogu/mini-tracing-for-art)
    * This project extends the built-in trace mechanism of Android ART by supporting logging Field Read/Written events.
    * Obviously, it is an experimantal extension and I only add 170 lines of code.
* [myblog](http://lab.artemisprojects.org/tianxiaogu/myblog)
    * A quite simple blog system built on top of `flask`, `SQLAlchemy`, `bootstrap`, `font-awesome` and many open source plugins.
    * It is simple as I almost do no customization on the style.
    * It can be deployed on Sina App Engine, a cheap PaaS cloud in China.
* [web-crawler](http://lab.artemisprojects.org/tianxiaogu/web-crawler)
    * A simple crawler based on selenium


<div id="clustrmaps-widget"></div><script type="text/javascript">var _clustrmaps = {'url' : 'http://moon.nju.edu.cn/~TianxiaoGu', 'user' : 995449, 'server' : '3', 'id' : 'clustrmaps-widget', 'version' : 1, 'date' : '2012-03-15', 'lang' : 'zh', 'corners' : 'square' };(function (){ var s = document.createElement('script'); s.type = 'text/javascript'; s.async = true; s.src = 'http://www3.clustrmaps.com/counter/map.js'; var x = document.getElementsByTagName('script')[0]; x.parentNode.insertBefore(s, x);})();</script><noscript><a href="http://www3.clustrmaps.com/user/94ef3079"><img src="http://www3.clustrmaps.com/stats/maps-no_clusters/moon.nju.edu.cn-~TianxiaoGu-thumb.jpg" alt="Locations of visitors to this page" /></a></noscript>
