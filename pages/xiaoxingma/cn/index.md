title: Xiaoxing Ma (Chinese)

<a href="../"><img width="32" alt="" src="../static/uk-icon-small.png" />English</a>
<img width="32" alt="" src="../static/china-icon-small.png" />中文

<hr/>


<table cellspacing="3" cellpadding="0" border="0"><tbody><tr>
        <td>
            <img src="../static/xxm-small.jpg" alt="Xiaoxing Ma in Rome" width="220">
        </td>
        <td> &nbsp;&nbsp;&nbsp;&nbsp; </td>
        <td>

            <table cellspacing="0" id="table1" cellpadding="0" border="0">
                <tbody><tr>
                    <td colspan="2" valign="top"> <h2>马晓星 &nbsp;&nbsp;<small>博士</small> </h2> </td>
                </tr>
                <tr>
                    <td colspan="2" valign="top"> 南京大学计算机科学与技术系 教授，博士生导师 <br>南京大学计算机软件研究所 副所长<br>南京大学计算机软件新技术国家重点实验室 </td>
                </tr>
                <tr>
                    <td width="15%" valign="top"> 地址: </td>
                    <td width="85%" valign="top"> 中国江苏省南京市栖霞区仙林大道163号南大仙林校区603信箱计算机系 <br> 邮编： 210023 </td>
                </tr>
                <tr>
                    <td width="15%" valign="top"> 办公室: </td>
                    <td width="85%" valign="top"> <a href="/contact/">计算机科学与技术楼816</a> </td>
                </tr>
                <tr>
                    <td width="25%" valign="top"> E-mail: </td>
                    <td width="85%" valign="top"> <img width="114" alt="Ma Xiaoxing's email" src="../static/email_nju.gif" id="_x0000_i1066" height="16" border="0"> </td>
                </tr>
                <tr>
                    <td width="15%" valign="top"> 电话: </td>
                    <td width="85%" valign="top"> +86 25 83686068 </td>
                </tr>
                <tr>
                    <td width="15%" valign="top"> 传真: </td>
                    <td width="85%" valign="top"> +86 25 83593283 </td>
            </tr></tbody></table>
        </td>
</tr></tbody></table>

## 简历
我从1997年来南京大学后就一直在此读书，2003年获得博士学位，而后留校任教至今。 

## 研究兴趣
我的研究领域属于软件工程，目前的工作集中于

* 自适应软件系统
* 软件体系结构与中间件
* 服务计算

## [发表论文](../publications)
近期部分论文：

~~~{.bibtexhtml}
@article{JavelusIST14,
  abstract = {Context
In-use software systems are destined to change in order to fix bugs or add new features. Shutting down a running system before updating it is a normal practice, but the service unavailability can be annoying and sometimes unacceptable. Dynamic software updating (DSU) migrates a running software system to a new version without stopping it. State-of-the-art Java DSU systems are unsatisfactory as they may cause a non-negligible system pause during updating.

Objective
In this paper we present Javelus, a Java HotSpot VM-based Java DSU system with very short pausing time.

Method
Instead of updating everything at once when the running application is suspended, Javelus only updates the changed code during the suspension, and migrates stale objects on-demand after the application is resumed. With a careful design this lazy approach neither sacrifices the update flexibility nor introduces unnecessary object validity checks or access indirections.

Results
Evaluation experiments show that Javelus can reduce the updating pausing time by one to two orders of magnitude without introducing observable overheads before and after the dynamic updating.

Conclusion
Our experience with Javelus indicates that low-disruptive and type-safe dynamic updating of Java applications can be practically achieved with a lazy updating approach.},
  author = {Gu, Tianxiao and Cao, Chun and Xu, Chang and Ma, Xiaoxing and Zhang, Linghao and L\"{u}, Jian},
  date-added = {2014-04-10 07:59:01 +0000},
  date-modified = {2015-01-03 08:01:12 +0000},
  journal = {Information and Software Technology},
  keywords = {Dynamic software updating; JVM; Lazy updating; Low disruption},
  number = {9},
  month = {September},
  pages = {1086-1098},
  title = {Low-disruptive Dynamic Updating of Java Applications},
  volume = {56},
  year = {2014},
  url = {http://dx.doi.org/10.1016/j.infsof.2014.04.003}
}
@article{Yang:2014tpds,
  author = {Yiling Yang and Yu Huang and Jiannong Cao and Xiaoxing Ma and Jian Lu},
  doi = {10.1109/TPDS.2013.233},
  issn = {1045-9219},
  journal = {IEEE Transactions on Parallel and Distributed Systems},
  keywords = {Clocks;Lattices;Maintenance engineering;Middleware;Monitoring;Runtime;Sensors;Asynchronous event streams;Lattice of snapshots;Predicate detection;Sliding window},
  title = {Design of a sliding window over distributed and asynchronous event streams},
  volume = {25},
  number = {10},
  pages = {2551-2560},
  year = {2014},
  month = {October},
  url = {http://dx.doi.org/10.1109/TPDS.2013.233}
}
@inproceedings{JYY:2014:ICSE,
  author = {Jiang, Yanyan and Gu, Tianxiao and Xu, Chang and Ma, Xiaoxing and Lu, Jian},
  title = {CARE: Cache guided deterministic replay for concurrent Java programs},
  booktitle = {Proceedings of the 36th International Conference on Software Engineering},
  confabbr = {ICSE '14},
  year = {2014},
  isbn = {978-1-4503-2756-5},
  location = {Hyderabad, India},
  confdate = {May 31 - June 7, 2014},
  pages = {457--467},
  numpages = {11},
  month = {June},
  url = {http://doi.acm.org/10.1145/2568225.2568236},
  doi = {10.1145/2568225.2568236},
  acmid = {2568236},
  publisher = {ACM},
  address = {New York, NY, USA},
  keywords = {Cache, Concurrency, Debugging, Replay}
}
@article{Yang2013TPDS,
  abstract = {Formal specification and runtime detection of contextual properties is one of the primary approaches to enabling context awareness in pervasive computing environments. Due to the intrinsic dynamism of the pervasive computing environment, dynamic properties, which delineate concerns of context-aware applications on the temporal evolution of the environment state, are of great importance. However, detection of dynamic properties is challenging, mainly due to the intrinsic asynchrony among computing entities in the pervasive computing environment. Moreover, the detection must be conducted at runtime in pervasive computing scenarios, which makes existing schemes do not work. To address these challenges, we propose the property detection for asynchronous context (PDAC) framework, which consists of three essential parts: 1) Logical time is employed to model the temporal evolution of environment state as a lattice. The active surface of the lattice is introduced as the key notion to model the runtime evolution of the environment state; 2) Specification of dynamic properties is viewed as a formal language defined over the trace of environment state evolution; and 3) The SurfMaint algorithm is proposed to achieve runtime maintenance of the active surface of the lattice, which further enables runtime detection of dynamic properties. A case study is conducted to demonstrate how the PDAC framework enables context awareness in asynchronous pervasive computing scenarios. The SurfMaint algorithm is implemented and evaluated over MIPA--the open-source context-aware middleware we developed. Performance measurements show the accuracy and cost-effectiveness of SurfMaint, even when faced with dynamic changes in the asynchronous pervasive computing environment.},
  author = {Yang, Yiling and Huang, Yu and Cao, Jiannong and Ma, Xiaoxing and Lu, Jian},
  date-added = {2013-06-28 02:01:55 +0000},
  date-modified = {2013-06-28 02:02:29 +0000},
  doi = {10.1109/TPDS.2012.259},
  issn = {1045-9219},
  journal = {IEEE Transactions on Parallel and Distributed Systems},
  keywords = {Context;Formal languages;Heuristic algorithms;Labeling;Lattices;Pervasive computing;Runtime;Dynamic property;asynchrony;context awareness;lattice;predicate detection},
  number = {8},
  pages = {1546-1555},
  title = {Formal Specification and Runtime Detection of Dynamic Properties in Asynchronous Pervasive Computing Environments},
  volume = {24},
  year = {2013},
  url = {http://dx.doi.org/10.1109/TPDS.2012.259}
}
@inproceedings{Ma:2011:FSE,
  acmid = {2025148},
  address = {New York, NY, USA},
  author = {Ma, Xiaoxing and Baresi, Luciano and Ghezzi, Carlo and Panzica La Manna, Valerio and Lu, Jian},
  booktitle = {Proceedings of the 19th ACM SIGSOFT symposium and the 13th European conference on Foundations of software engineering},
  date-added = {2013-04-05 06:50:02 +0000},
  date-modified = {2014-04-10 13:25:34 +0000},
  doi = {10.1145/2025113.2025148},
  isbn = {978-1-4503-0443-6},
  keywords = {component-based distributed system, dynamic reconfiguration, version-consistency},
  location = {Szeged, Hungary},
  numpages = {11},
  pages = {245--255},
  publisher = {ACM},
  confabbr = {ESEC/FSE '11},
  confdate = {September 05 - 09, 2011},
  title = {Version-consistent dynamic reconfiguration of component-based distributed systems},
  url = {http://doi.acm.org/10.1145/2025113.2025148},
  year = {2011},
  bdsk-url-1 = {http://doi.acm.org/10.1145/2025113.2025148}
}
~~~


([还有...](../publications))

## 研究项目

* [Funds](../funds)
* [Projects](../projects)

## 课程教学

* [程序设计语言概论](../copl)
* [面向对象的软件构造](../oot2007)



## 荣誉奖励

* 2010年度教育部高等学校科学研究优秀成果奖技术发明奖，“网构化软件关键技术、平台与应用”，第二完成人。
* 2009年度 “中创软件人才” 奖。
* 2007年度入选教育部 “新世纪优秀人才支持计划”。
* 2006年度国家科技进步二等奖：“对象化与主体化的软件协同技术、平台与应用”，第二完成人。

## 专业服务

* 国际会议程序委员
   * SEAMS 2012: [7th International Symposium on Software Engineering for Adaptive and Self-Managing Systems](http://www.seams2012.cs.uvic.ca/)
   * VINCI 2011, 2010, 2009: [Visual Information Communication - International Symposium](http://www.cse.ust.hk/vinci2011/)
   * SCORE 2011: [Student Contest on Software Engineering](http://score-contest.org/2011/)
   * [Software engineering education track of ICSE 2010](http://www.sbs.co.za/ICSE2010/3-EVENTS/_TRACKS/ICSE2010_SE-EDUCATION.html)
* 期刊编委
   * [软件学报](http://www.jos.org.cn)  2011 - 2014

Maintained by [Xiaoxing Ma](/people/xiaoxingma) Last updated 2014-02-12
