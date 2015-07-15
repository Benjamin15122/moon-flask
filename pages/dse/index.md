title: Dynamic Software Evolution Group

# Dynamic Software Evolution Group

## People

* Prof. [Xiaoxing Ma](http://moon.nju.edu.cn/~xxm)
* [Tianxiao Gu](http://moon.nju.edu.cn/~txgu)
* [Shengwei An](/people/shengweian/ )
* [Ruiqi Liu](/people/ruiqiliu/)
* Yiqun Wang
* [Zelin Zhao](http://moon.nju.edu.cn/spar/people/zzl/zzl.html)

## Publications

~~~{.bibtexhtml}

@inproceedings{an_qrs_2015,
	author = {An, Shengwei and Ma, Xiaoxing and Cao, Chun and Yu, Ping and Xu, Chang},
	booktitle = {Proceedings of the 2015 IEEE International Conference on Software Quality, Reliability & Security},
	numpages = {10},
	title = {An Event-based Formal Framework for Dynamic Software Update},
	year = {2015},
}

@inproceedings{Zhao:2014:ARD:2677832.2677853,
 author = {Zhao, Zelin and Ma, Xiaoxing and Xu, Chang and Yang, Wenhua},
 title = {Automated Recommendation of Dynamic Software Update Points: An Exploratory Study},
 booktitle = {Proceedings of the 6th Asia-Pacific Symposium on Internetware on Internetware},
 series = {INTERNETWARE 2014},
 year = {2014},
 isbn = {978-1-4503-3303-0},
 location = {Hong Kong, China},
 pages = {136--144},
 numpages = {9},
 url = {http://doi.acm.org/10.1145/2677832.2677853},
 doi = {10.1145/2677832.2677853},
 acmid = {2677853},
 publisher = {ACM},
 address = {New York, NY, USA},
 keywords = {Dynamic software updating (DSU), automated recommendation, update points},
}

@article{JavelusIST14,
	Abstract = {Context
In-use software systems are destined to change in order to fix bugs or add new features. Shutting down a running system before updating it is a normal practice, but the service unavailability can be annoying and sometimes unacceptable. Dynamic software updating (DSU) migrates a running software system to a new version without stopping it. State-of-the-art Java DSU systems are unsatisfactory as they may cause a non-negligible system pause during updating.

Objective
In this paper we present Javelus, a Java HotSpot VM-based Java DSU system with very short pausing time.

Method
Instead of updating everything at once when the running application is suspended, Javelus only updates the changed code during the suspension, and migrates stale objects on-demand after the application is resumed. With a careful design this lazy approach neither sacrifices the update flexibility nor introduces unnecessary object validity checks or access indirections.

Results
Evaluation experiments show that Javelus can reduce the updating pausing time by one to two orders of magnitude without introducing observable overheads before and after the dynamic updating.

Conclusion
Our experience with Javelus indicates that low-disruptive and type-safe dynamic updating of Java applications can be practically achieved with a lazy updating approach.},
	Author = {Gu, Tianxiao and Cao, Chun and Xu, Chang and Ma, Xiaoxing and Zhang, Linghao and L\"{u}, Jian},
	Date-Added = {2014-04-10 07:59:01 +0000},
	Date-Modified = {2015-01-03 08:01:12 +0000},
	Journal = {Information and Software Technology},
	Keywords = {Dynamic software updating; JVM; Lazy updating; Low disruption},
	Number = {9},
	Month = {September},
	Pages = {1086-1098},
	Title = {Low-disruptive Dynamic Updating of Java Applications},
	Volume = {56},
	Year = {2014},
	Url={http://dx.doi.org/10.1016/j.infsof.2014.04.003}}

@inproceedings{DBLP:conf/apsec/SuCML13,
  author    = {Ping Su and
               Chun Cao and
               Xiaoxing Ma and
               Jian Lu},
  title     = {Automated Management of Dynamic Component Dependency for Runtime System
               Reconfiguration},
  booktitle = {Proceedings of the 20th Asia-Pacific Software Engineering Conference},
  pages     = {450--458},
  year      = {2013},
  crossref  = {DBLP:conf/apsec/2013-1},
  url       = {http://dx.doi.org/10.1109/APSEC.2013.66},
  doi       = {10.1109/APSEC.2013.66},
  timestamp = {Mon, 15 Jun 2015 19:00:08 +0200},
  biburl    = {http://dblp.uni-trier.de/rec/bib/conf/apsec/SuCML13},
  bibsource = {dblp computer science bibliography, http://dblp.org}
}

@inproceedings{Gu:2012:JLD:2452575.2454416,
	Acmid = {2454416},
	Address = {Washington, DC, USA},
	Author = {Gu, Tianxiao and Cao, Chun and Xu, Chang and Ma, Xiaoxing and Zhang, Linghao and Lu, Jian},
	Booktitle = {Proceedings of the 19th Asia-Pacific Software Engineering Conference},
	Date-Added = {2013-04-05 06:51:39 +0000},
	Date-Modified = {2013-04-05 06:51:39 +0000},
	Doi = {10.1109/APSEC.2012.55},
	Isbn = {978-0-7695-4922-4},
	Keywords = {dynamic software updates, Java, virtual machine},
	Numpages = {10},
	Pages = {527--536},
	Publisher = {IEEE Computer Society},
	Series = {APSEC '12},
	Title = {Javelus: A Low Disruptive Approach to Dynamic Software Updates},
	Url = {http://dx.doi.org/10.1109/APSEC.2012.55},
	Year = {2012},
	Bdsk-Url-1 = {http://dx.doi.org/10.1109/APSEC.2012.55}}

@inproceedings{Ma:2011:FSE,
	Acmid = {2025148},
	Address = {New York, NY, USA},
	Author = {Ma, Xiaoxing and Baresi, Luciano and Ghezzi, Carlo and Panzica La Manna, Valerio and Lu, Jian},
	Booktitle = {Proceedings of the 19th ACM SIGSOFT Symposium and the 13th European Conference on Foundations of Software Engineering},
	Date-Added = {2013-04-05 06:50:02 +0000},
	Date-Modified = {2014-04-10 13:25:34 +0000},
	Doi = {10.1145/2025113.2025148},
	Isbn = {978-1-4503-0443-6},
	Keywords = {component-based distributed system, dynamic reconfiguration, version-consistency},
	Location = {Szeged, Hungary},
	Numpages = {11},
	Pages = {245--255},
	Publisher = {ACM},
	confabbr = {ESEC/FSE '11},
	confdate = {September 05 - 09, 2011},
	Title = {Version-consistent Dynamic Reconfiguration of Component-based Distributed Systems},
	Url = {http://doi.acm.org/10.1145/2025113.2025148},
	Year = {2011},
	Bdsk-Url-1 = {http://doi.acm.org/10.1145/2025113.2025148}}
~~~

## Software

* [Javelus](http://lab.artemisprojects.org/javelus/javelus)

## Former Group Members

* Ping Su (M.S., 2013)
* Guozhen Xie (M.S., 2013)
    * Current employment: ICBC
* Yan Yao (M.S., 2012)
    * Current employment: Microsoft


