title: Xiaoxing Ma

<img width="32" alt="" src="static/uk-icon-small.png" />English
<a href="cn/"><img width="32" alt="" src="static/china-icon-small.png" />中文</a>

<hr/>

<table border="0" cellpadding="0" cellspacing="0" width="100%">
    <tbody>
    <tr>
        <td valign="top" width="300"><img src="static/xxm-small.jpg" width="249" height="297"></td>
        <td valign="top">
            <table border="0" cellpadding="0" cellspacing="0">
                <tbody>
                <tr>
                    <td colspan="2">
                        <span style="font-size:24pt">Dr. Xiaoxing Ma</span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <span style="font-size:14pt">Professor</span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <span style="font-size:14pt">State Key Laboratory for Novel Software Technology, Nanjing University</span>
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        <span style="font-size:14pt">Department of Computer Science and Technology, Nanjing University</span>
                    </td>
                </tr>
                <tr>
                    <td align="right" style="vertical-align:top;padding-top:10pt">Address:</td>
                    <td style="padding-left:15px;vertical-align:top;padding-top:10pt">
                        Department of Computer Science,<br/>
                        Nanjing University Xianlin Campus (Mailbox 603)<br/>
                        163 Xianlin Avenue, Qixia, Nanjing 210023, Jiangsu, China
                    </td>
                </tr>
                <tr>
                    <td align="right">Office:</td>
                    <td style="padding-left:15px">Computer Science and Technology Building 816</td>
                </tr>
                <tr>
                    <td align="right">Phone:</td>
                    <td style="padding-left:15px">+86 25 89686068</td>
                </tr>
                <tr>
                    <td align="right">Fax:</td>
                    <td style="padding-left:15px">+86 25 83593283</td>
                </tr>
                <tr>
                    <td align="right">Email:</td>
                    <td style="padding-left:15px"><img src="static/email_nju.gif"/></td>
                </tr>
                </tbody>
            </table>
        </td>
    </tr>
    </tbody>
</table>


<!--
## Short biography
Dr. Xiaoxing Ma is a professor at the [[http://cs.nju.edu.cn][Department of Computer Science and Technology]], [[http://www.nju.edu.cn][Nanjing University]]. He got his B.Sc., M.Sc. and Ph.D., all in Computer Science, from the same University in 1997, 2000 and 2003, respectively. 

He worked as a Borsa Post-Doc in the [[http://deepse.dei.polimi.it/][DEEP-SE group]], [[http://www.polimi.it/][Politecnico di Milano]] from Dec. 2009 to Nov. 2010. He was once a research assistant in the [[http://www.comp.polyu.edu.hk/][Department of Computing]], [[http://www.polyu.edu.hk/][Hong Kong Polytechnic University]] from Oct. 2001 to Mar. 2002. 
-->

## Research interests

I am interested in various topics in software engineering, especially

* Adaptive software systems ( _newly funded by [NSFC](http://www.nsfc.gov.cn/): [ESEEPS](eseeps)_)
* Software architectures and middleware systems
* Service-oriented computing

## [Publications](publications)

* *[English publications](publications)*
* *[Chinese publications](http://www.cdblp.cn/search_result.php?author_name=%E9%A9%AC%E6%99%93%E6%98%9F&domain=computer)*

### Some recent publications:

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

## Teaching
   * 2015, Spring: [Discrete Mathematics and Its Applications](http://moon.nju.edu.cn/courses/course/view.php?id=31) (Dept. CSE)
   * 2014, Autumn: [Discrete Mathematical Structures] (Inst. Softw.)
   * 2014, Spring: [Discrete Mathematics and Its Applications](http://moon.nju.edu.cn/courses/course/view.php?id=25) (Dept. CSE)
   * 2008-2014, Spring: [Concepts of Programming Languages](copl)
   * 2013, Autumn: [Discrete Mathematical Structures](DMS2013.html) (Inst. Softw.)
   * Before 2007:  [Object-Oriented Software Construction](OOT2007.html)

## Awards
   * 2006: China National Award for Science and Technology Progress, 2nd prize. Dr. Ma is the 2nd awardee of the team. （国家科技进步二等奖，第二完成人）
   * 2011: China National Award for Science and Technology Progress, 2nd prize. Dr. Ma is the 4th awardee of the team. （国家科技进步二等奖，第四完成人）
   * 2009: _CVIC SE_ Award for Software Researchers. （中创软件人才奖）
   * 2010: MOE Award for S&T Research in Universities, 1st class, Ministry of Education. I am the 2nd awardee of the team. （教育部高校优秀科研成果技术发明一等奖，第二完成人）

## Professional activities

* Member of program committees 
   * SEAMS [2014](http://seams2014.uni-paderborn.de/), [2013](http://www.yorku.ca/mlitoiu/seams2013/), [2012](http://www.seams2012.cs.uvic.ca/): 9th/8th/7th International Symposium on Software Engineering for Adaptive and Self-Managing Systems
   * [SOSE 2013](http://sei.pku.edu.cn/conference/sose2013/): 7th International Symposium on Service Oriented System Engineering
   * [WICSA/ECSA 2012 - Joint 10th Working IEEE/IFIP Conference on Software Architecture & 6th European Conference on Software Architecture](http://www.wicsa.net/)
   * VINCI 2011, 2010, 2009: [Visual Information Communication - International Symposium](http://www.cse.ust.hk/vinci2011/)
   * SCORE 2011: [Student Contest on Software Engineering](http://score-contest.org/2011/)
   * [Software engineering education track of ICSE 2010](http://www.sbs.co.za/ICSE2010/3-EVENTS/_TRACKS/ICSE2010_SE-EDUCATION.html)
* Editorial Board Member 
   * [Journal of Software](http://www.jos.org.cn) (in Chinese), Jan. 2011 - Dec. 2014
* Guest Editor 
   * Special Focus on Internetware, _Science China: Information Sciences_ Volume 56, Number 1, January 2013.


Maintained by [Xiaoxing Ma](/people/xiaoxingma) Last updated 2014-02-12
