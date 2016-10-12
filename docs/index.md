title: Institute of Computer Software (new)
extensions: math
compact_layout: true

<table>
<div id="k-body">
<div class="row no-gutter fullwidth"><!-- row -->
    <div class="col-lg-12 clearfix"><!-- featured posts slider -->
        <div id="carousel-featured" class="carousel slide" data-interval="4000" data-ride="carousel"><!-- featured posts slider wrapper; auto-slide -->
            <ol class="carousel-indicators"><!-- Indicators -->
                <li data-target="#carousel-featured" data-slide-to="0" class="active"></li>
                <li data-target="#carousel-featured" data-slide-to="1"></li>
                <li data-target="#carousel-featured" data-slide-to="2"></li>
            </ol><!-- Indicators end -->
            <div class="carousel-inner"><!-- Wrapper for slides -->
                <div class="item active">
                    <img src="{{ url_for('static', filename='img/slide-5.jpg') }}" alt="Institute of Computer Software" />
                    <div class="k-carousel-caption pos-c-2-3 scheme-dark no-bg">
                        <div class="caption-content">
                            <h3 class="caption-title title-giant">Institute of Computer Software</h3>
                            <p>
                                Founded in 1984. Advancing software technology in China.
                            </p>
                            <p>
                                <a href="/about" class="btn btn-sm btn-danger" title="Button">READ MORE</a>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="item ">
                    <img src="{{ url_for('static', filename='img/slide-2.jpg') }}" alt="Professor Jiafu Xu" />
                    <div class="k-carousel-caption pos-2-3-right scheme-dark">
                        <div class="caption-content">
                            <h3 class="caption-title">Professor Jiafu Xu, Founding Director</h3>
                            <p>
                                Pioneering researcher and educatior of software technolgoy in China. 
                            </p><p>
                                CCF Liftime Achievement Award Winner. 
                               <!--中国计算机软件学先驱，中国计算机科学奠基人之一，南京大学教授。-->
                            </p>
                        </div>
                    </div>
                </div>
                <div class="item">
                    <img src="{{ url_for('static', filename='img/slide-1.jpg') }}" alt="Professor Jian Lü" />
                    <div class="k-carousel-caption pos-2-3-left scheme-dark">
                        <div class="caption-content">
                            <h3 class="caption-title">Professor Jian Lü, Vice President of Nanjing University</h3>
                            <p>
                            Director of the State Key Laboratory of Novel Software Technology at Nanjing University
                            <!--博士生导师，计算机软件新技术国家重点实验室主任。2013年当选中国科学院院士。-->
                            </p>
                        </div>
                    </div>
                </div>
            </div><!-- Wrapper for slides end -->
            <!-- Controls -->
            <a class="left carousel-control" href="#carousel-featured" data-slide="prev"><i class="fa fa-chevron-left"></i></a>
            <a class="right carousel-control" href="#carousel-featured" data-slide="next"><i class="fa fa-chevron-right"></i></a>
            <!-- Controls end -->
        </div><!-- featured posts slider wrapper end -->
    </div><!-- featured posts slider end -->
</div><!-- row end -->

<div class="row no-gutter"><!-- row -->
    <div class="col-lg-4 col-md-4"><!-- upcoming events wrapper -->
        <div class="col-padded col-shaded"><!-- inner custom column -->
            <ul class="list-unstyled clear-margins"><!-- widgets -->
                <li class="widget-container widget_up_events"><!-- widgets list -->
                    <h1 class="title-widget">Upcoming Events</h1>
                    <ul class="list-unstyled">
                         <!-- the most close deadline -->

                         <!-- -->
                         {% if phd|first %}
                         <li class="up-event-wrap">
                         <h1 class="title-median"><a href="{{ url_for('events', path='phd') }}" title="{{ phd[0].speaker }}">PhD Seminar: {{ phd[0].speaker }}</a></h1>
                             <div class="up-event-meta clearfix">
                                 <div class="up-event-date">{{ phd[0].date | to_date }}</div><div class="up-event-time">{{ phd[0].date | to_time }}</div>
                             </div>
                         </li>
                         {% endif %}
                         {% if master|first %}
                         <li class="up-event-wrap">
                         <h1 class="title-median"><a href="{{ url_for('events', path='master') }}" title="{{ master[0].speaker }}">Master Seminar: {{ master[0].speaker }}</a></h1>
                             <div class="up-event-meta clearfix">
                                 <div class="up-event-date">{{ master[0].date | to_date }}</div><div class="up-event-time">{{ master[0].date | to_time }}</div>
                             </div>
                         </li>
                         {% endif %}
                         {% for e in events %}
                            {% if loop.index <= 3 %}
                                <li class="up-event-wrap">
                                <h1 class="title-median"><a href="{{ e.url }}" title="{{ e.title }}">{{ e.title }}</a></h1>
                                    <div class="up-event-meta clearfix">
                                        <div class="up-event-date">{{ e.date | to_date }}{% if e.endDate %} - {{ e.endDate | to_date }}{% endif %}</div>
                                        {% if e.time %}
                                            <div class="up-event-time">{{ e.time | to_time }} {% if e.endTime %} - {{ e.endTime | to_time}} {% endif %}</div>
                                        {% endif %}
                                    </div>
                                    {% if e.summary %}
                                    <p>
                                        {{ e.summary|truncate(150)|safe}}
                                        <!--<a href="{{ e.events }}" class="moretag" title="read more">MORE</a>-->
                                    </p>
                                    {% endif %}
                                </li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                </li><!-- widgets list end -->
                {% if deadlines | first %}
                <li class="widget-container widget_up_events" style="margin-top: 10px"><!-- widgets list -->
                    <h1 class="title-widget">Deadlines</h1>
                    <ul class="list-unstyled">
                          {% for e in deadlines %}
                            {% if loop.index <= 3 %}
                         <li class="">
                         <h1 class="title-median"><a href="{{ url_for('events', path='deadlines') }}" title="{{ e.label}}">DEADLINE: {{ e.label }}</a></h1>
                             <div class="up-event-meta clearfix">
                                 <div class="up-event-date">{{ e.date | to_date }}</div>
                             </div>
                         </li>
                         {% endif %}
                         {% endfor %}
                    </ul>
                </li><!-- widgets list end -->
                {% endif %}
             </ul><!-- widgets end -->
        </div><!-- inner custom column end -->
    </div><!-- upcoming events wrapper end -->
    <div class="col-lg-4 col-md-4"><!-- recent news wrapper -->
        <div class="col-padded"><!-- inner custom column -->
            <ul class="list-unstyled clear-margins"><!-- widgets -->
                <li class="widget-container widget_recent_news"><!-- widgets list -->
                    <h1 class="title-widget">News</h1>
                    <ul class="list-unstyled">
                        {% for n in news %}
                            {% if loop.index <= 3 %}
                                <li class="recent-news-wrap">
                                <h1 class="title-median"><a href="{{ url_for('news_page', path=n.path) }}" title="{{n.title}}">{{ n.title }}</a></h1>
                                    <div class="recent-news-meta">
                                        <div class="recent-news-date">{{ n.date | to_date }}</div>
                                    </div>
                                    <div class="recent-news-content clearfix">
                                        {% if n.img_path %}
                                        <figure class="recent-news-thumb">
                                            <a href="{{ url_for('news_page', path=n.path) }}" title="{{ n.img_title }}"><img src="{{url_for('static', filename=n.img_path)}}" class="attachment-thumbnail wp-post-image" alt="Thumbnail 1" /></a>
                                        </figure>
                                        <div class="recent-news-text">
                                            <p>{{ n.summary|truncate(110)|safe }}</p>
                                        </div>
                                        {% else %}
                                        <div class="recent-news-text" style="margin-left:0px">
                                            <!-- no image, show more words use 200 -->
                                            <p>{{ n.summary|truncate(300)|safe }}</p>
                                        </div>
                                        {% endif %}
                                    </div>
                                </li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                    <div class="recent-news-wrap" style="text-align:right">
                       <a href="{{ url_for('news') }}" class="moretag" title="read more">more</a>
                    <div>
                </li><!-- widgets list end -->
            </ul><!-- widgets end -->
        </div><!-- inner custom column end -->
    </div><!-- recent news wrapper end -->
    <div class="col-lg-4 col-md-4"><!-- misc wrapper -->
        <div class="col-padded col-shaded"><!-- inner custom column -->
            <ul class="list-unstyled clear-margins"><!-- widgets -->
                <li class="widget-container widget_nav_menu"><!-- widget -->
                    <h1 class="title-widget">Recent Papers</h1>
                    <ul class="list-unstyled">
                        {% for n in g.site.paper_news %}
                            {% if loop.index <= 3 %}
                                <li style="text-transform: none">{{ n.title }}</li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                    <div class="recent-news-wrap" style="text-align:right">
                       <a href="{{ url_for('short_news', path='papers') }}" class="moretag" title="read more">more</a>
                    <div>
                </li><!-- widget end -->
                <li class="widget-container widget_nav_menu" style="margin-top: 10px"><!-- widget -->
                    <h1 class="title-widget">Awards</h1>
                    <ul class="list-unstyled">
                        {% for n in g.site.award_news %}
                            {% if loop.index <= 3 %}
                                <li style="text-transform: none">{{ n.title }}</li>
                            {% endif %}
                        {% endfor %}
                    </ul>
                    <div class="recent-news-wrap" style="text-align:right">
                       <a href="{{ url_for('short_news', path='awards') }}" class="moretag" title="read more">more</a>
                    <div>
                </li><!-- widget end -->
                 <li class="widget-container widget_nav_menu" style="margin-top: 10px"><!-- widget -->
                    <h1 class="title-widget">Scholarships</h1>
                    <ul class="list-unstyled">
                        {%-for n in g.site.scholarship_news-%}
                            {%-if loop.index <= 3-%}
                                <li style="text-transform: none">{{ n.title }}</li>
                            {%-endif-%}
                        {%-endfor-%}
                    </ul>
                    <div class="recent-news-wrap" style="text-align:right">
                       <a href="{{ url_for('short_news', path='scholarships') }}" class="moretag" title="read more">more</a>
                    <div>
                </li><!-- widget end -->
            </ul><!-- widgets end -->
        </div><!-- inner custom column end -->
    </div><!-- misc wrapper end -->
</div><!-- row end -->
</div>

<div id="k-footer"><!-- footer -->
    <div class="container"><!-- container -->
        <div class="row no-gutter"><!-- row -->
            <div class="col-lg-4 col-md-4"><!-- widgets column left -->
                <div class="col-padded col-naked">
                    <ul class="list-unstyled clear-margins"><!-- widgets -->
                        <li class="widget-container widget_nav_menu"><!-- widgets list -->
                            <h1 class="title-widget">Links</h1>
                            <ul>
                                <li><a href="http://cs.nju.edu.cn/" title="menu item">Department of Computer Science and Technology</a></li>
                                <li><a href="http://www.nju.edu.cn/" title="menu item">Nanjing University</a></li>
                                <li><a href="http://keysoftlab.nju.edu.cn/site/ndjsjx/" title="menu item">State Key Laboratory for Novel Software Technology</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div><!-- widgets column left end -->
            <div class="col-lg-4 col-md-4"><!-- widgets column center -->
                <div class="col-padded col-naked">
                    <ul class="list-unstyled clear-margins"><!-- widgets -->
                        <li class="widget-container widget_recent_news"><!-- widgets list -->
                            <h1 class="title-widget">Contact</h1>
                            <div itemscope itemtype="http://data-vocabulary.org/Organization"> 
                                <h2 class="title-median m-contact-subject" itemprop="name">Institute of Computer Software</h2>
                                <div class="m-contact-address" itemprop="address" itemscope itemtype="http://data-vocabulary.org/Address">
                                    <span class="m-contact-street" itemprop="street-address">No. 163 Xianlin Avenue, Qixia</span>
                                    <span class="m-contact-city-region"><span class="m-contact-city" itemprop="locality">Nanjing</span>, <span class="m-contact-region" itemprop="region">Jiangsu</span></span>
                                    <span class="m-contact-zip-country"><span class="m-contact-zip" itemprop="postal-code">210023</span> <span class="m-contact-country" itemprop="country-name">China</span></span>
                                </div>
                                <div class="m-contact-tel-fax">
                                    <span class="m-contact-tel">Tel: <span itemprop="tel">025-89686068</span></span>
                                    <span class="m-contact-fax">Fax: <span itemprop="fax">025-83593283</span></span>
                                </div>
                            </div>
                            <!--
                            <div class="social-icons">
                                <ul class="list-unstyled list-inline">
                                    <li><a href="#" title="Contact us"><i class="fa fa-envelope"></i></a></li>
                                    <li><a href="#" title="Twitter"><i class="fa fa-twitter"></i></a></li>
                                    <li><a href="#" title="Facebook"><i class="fa fa-facebook"></i></a></li>
                                </ul>
                            </div>
                            -->
                        </li>
                    </ul>
                </div>
            </div><!-- widgets column center end -->
            {% if g.site %}
            <div class="col-lg-4 col-md-4"><!-- widgets column right -->
                <div class="col-padded col-naked">
                    <ul class="list-unstyled clear-margins"><!-- widgets -->
                        <li class="widget-container widget_sofa_flickr"><!-- widgets list -->
                            <h1 class="title-widget">Photo</h1>
                            <ul class="k-flickr-photos list-unstyled">
                                {% for p in g.site.photos %}
                                    {% if loop.index <= 8 %}
                                       <li><a href="{{ p.url }}" title="{{ p.title }}"><img src="{{ url_for('static', filename=p.src) }}" alt="{{ p.title }}" /></a></li>
                                    {% endif %}
                                {% endfor %}
                            </ul>
                        </li>
                    </ul>
                </div>
            </div><!-- widgets column right end -->
            {% endif %}
        </div><!-- row end -->
    </div><!-- container end -->
</div><!-- footer end -->
</table>

