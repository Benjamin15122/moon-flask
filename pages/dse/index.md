title: Dynamic Software Evolution Group

# Dynamic Software Evolution Group

We hack JVM to implement tools and conduct research on

* Dynamic Software Updating
* Automatic Runtime Recovery
* Whole-Program Dynamic Program Analysis
* Android Testing

Check out [gif](./dsegif) showing
what dynamic software updating and automatic runtime recovery are.

## People

{{ render_people(group = "dse", category = ["faculty", "phd", "graduates"]) | safe }}

## Publications

~~~{.bibtexhtml}
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
  doi       = {10.1145/2970276.2970360},
}
@inproceedings{wang_qrs_2016,
    author    = {Wang, Yiqun and An, Shengwei and Ma, Xiaoxing and Cao, Chun and Xu, Chang},
    booktitle = {2016 IEEE International Conference on Software Quality, Reliability and Security (QRS)},
    title     = {Verifying Distributed Controllers with Local Invariants},
    year      = {2016},
    month     = {Aug},
}
@inproceedings{an_qrs_2015,
	author={An, Shengwei and Ma, Xiaoxing and Cao, Chun and Yu, Ping and Xu, Chang}, 
    booktitle={2015 IEEE International Conference on Software Quality, Reliability and Security (QRS)}, 
    title={An Event-Based Formal Framework for Dynamic Software Update}, 
    year={2015}, 
    pages={173-182}, 
    keywords={dynamic software update; formal methods;}, 
    doi={10.1109/QRS.2015.33}, 
    month={Aug},
}



@inproceedings{Zhao:2014:ARD:2677832.2677853,
 author = {Zhao, Zelin and Ma, Xiaoxing and Xu, Chang and Yang, Wenhua},
 title = {Automated Recommendation of Dynamic Software Update Points: An Exploratory Study},
 booktitle = {Proceedings of the 6th Asia-Pacific Symposium on Internetware on Internetware},
 year = {2014},
 location = {Hong Kong, China},
 pages = {136--144},
 numpages = {9},
 url = {http://doi.acm.org/10.1145/2677832.2677853},
 doi = {10.1145/2677832.2677853},
}

@article{JavelusIST14,
	Author = {Gu, Tianxiao and Cao, Chun and Xu, Chang and Ma, Xiaoxing and Zhang, Linghao and L\"{u}, Jian},
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
  url       = {http://dx.doi.org/10.1109/APSEC.2013.66},
  doi       = {10.1109/APSEC.2013.66},
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

We have a couple of projects hacking the Java HotSpot JVM and Android ART.

* [Javelus]({{ page_for(path='/dse/javelus') }}): A dynamic-updating-enabled JVM
* [Ares]({{ page_for(path='/dse/ares') }}): Automatic Runtime Recovery
* [AOTES]({{ page_for(path='/dse/aotes') }}): Synthesizing object transformations for DSU
* MiniTracing and MiniTracing for ART: Whole Program Tracing in JVM
    * [PHD]({{ page_for(path='/dse/phd') }}): Precise Heap Differentiating Using Access Path and Execution Index

## Former Group Members

-------------------

{{ render_people(group = "dse", category = ["alumni"]) | safe }}

-------------------

* Tongbao Zhang (M.S., 2015)
    * First employment: Alibaba, JVM Group
* Guozhao Ren (M.S., 2014)
    * First employment: China Telecom
* Ping Su (M.S., 2014)
* Jiang Wang (M.S., 2013)
* Guozhen Xie (M.S., 2013)
    * First employment: ICBC
* Yan Yao (M.S., 2012)
    * First employment: Microsoft

<style>
svg {
position: relative;
left: 50%;
-webkit-transform: translateX(-50%);
-ms-transform: translateX(-50%);
transform: translateX(-50%);
}
</style>

<div style="position: relative;">
<svg height="200" width="200">
  <path id="D"  d="M0 0 L75 0 L100 100 L50 200 L0 200 Z" fill="#e1004c"/>
  <path id="S"  d="M75 0 L100 100 L50 200 L125 200 L100 100 L150 0 Z" fill="#ffee00"/>
  <path id="E1" d="M150 0 L100 100 L200 100 L200 0 Z" fill="#e1004c"/>
  <path id="E2" d="M125 200 L100 100 L200 100 L200 200 Z" fill="#06799f"/>
  <!--
  <text x="440" y="100" fill="#e1004c"
       font-size="200" font-family="Courier New" font-weight="bold"
       text-anchor="middle"
       dominant-baseline="middle">DSE</text>

  <text x="440" y="175" fill="#06799f"
       font-size="25" font-family="Courier New" font-weight="bold"
       text-anchor="middle"
       dominant-baseline="middle">Dynamic Software Evolution</text>
  -->


  Sorry, your browser does not support inline SVG.
</svg>
</div>


