# -*- coding: utf-8

from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
from markdown.preprocessors import Preprocessor

INDEX_DATA = '''
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
                    <img src="/static/img/slide-5.jpg" alt="Institute of Computer Software" />
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
                    <img src="/static/img/slide-2.jpg" alt="Professor Jiafu Xu" />
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
                    <img src="/static/img/slide-1.jpg" alt="Professor Jian Lü" />
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
'''

class IndexProc(Preprocessor):
    def index(self):
        return INDEX_DATA

    def run(self, lines):
        new_lines = []
        for line in lines:
            if line.lower() == '[indexpage]':
                new_lines.append(self.index())
            else:
                new_lines.append(line)
        return new_lines

class IndexPageExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)

        md.preprocessors.add(
                "index-processor",
                IndexProc(),
                "_end"
            )

