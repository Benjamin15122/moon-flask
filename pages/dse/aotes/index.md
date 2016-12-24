title: Synthesizing object transformation for Dynamic Software Updating



# Synthesizing object transformation for Dynamic Software Updating


<!--
Dynamic software updating could be viewed as runtime state transformation of a running program.
For Java programs, we need to transform the state of a stale object (i.e., objects created by stale classes) to a new state.
Apparently, object transformation is critical to correct and reliable dynamic software updating of Java programs.
However, fully automatic object transformations for arbitrary programs are impossible.

Existing DSU systems either provide weak automatic or semi-automatic support of object transformations
or totally delegate the responsibility to programmers,
which make DSU systems hard-to-use.

This project, AOTES, aims to automate object transformation for specific kinds of updates.
AOTES is based on two observations.

1. The state of an object can be reified from its method invocation history.
2. The method invocation history of an object usually keeps unchanged in the history.

Hence, once we can obtain the method invocation history of a stale object,
we can use it to construct a new method invocation history by replacing every old method with its new version
and initialize the new state by replaying the new method invocation history.

The problem is that obtaining the method invocation history of a running program is also difficult.
Naive record-and-replay of every method invocation is obviously expensive in production environments.
To this end, AOTES tries to synthesize a method invocation synthesis.
However, synthesizing method invocation is also non-trivial as we must provide the arguments.
For example, an `int` parameter in Java may be any integer number between -2<sup>31</sup> and 2<sup>31</sup>-1.

To make execution synthesis possible and scalable,
AOTES attempts to synthesizes a specific kind of inverse methods, which has no parameter,
and uses these inverse methods for execution synthesis instead of the original complicated methods.

More details about AOTES can be found in our paper.
-->

## Source Code

AOTES-ASM:

* [bitbucket](https://bitbucket.org/txgu/aotes-asm)

Subjects for ICSE 2017

* [subjects-for-icse-2017](https://bitbucket.org/txgu/aotes-icse17-subjects)

## Documentation

* To be added
