title: Flowchart and Raphael

# Flowchart and Raphael

## Flowchart

```
~~~{.flowchart}
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
~~~
```

~~~{.flowchart}
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
~~~

## Raphael

```
~~~{.raphael hl_lines="canvas"}
var paper = Raphael("canvas", 640, 480);
paper.rect(0, 0, 640, 480, 10).attr({fill: "#fff", stroke: "none"});
paper.circle(320, 240, 60).animate({fill: "#223fa3", stroke: "#000", "stroke-width": 80, "stroke-opacity": 0.5}, 2000);
~~~
```

~~~{.raphael hl_lines="canvas"}
var paper = Raphael("canvas", 640, 480);
paper.rect(0, 0, 640, 480, 10).attr({fill: "#fff", stroke: "none"});
paper.circle(320, 240, 60).animate({fill: "#223fa3", stroke: "#000", "stroke-width": 80, "stroke-opacity": 0.5}, 2000);
~~~


