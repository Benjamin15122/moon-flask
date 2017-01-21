title: MiniTracing for HotSpot
date: 2016-12-12
category: programming
tags: java,android
template: post.html

MiniTracing for HotSpot aims to trace various events inside a running HotSpot JVM.

Currently, we support the following events.

* Method Entry
    * Data logged: method pointer
* Method Exit
    * Data logged: method pointer
* Lock Acquire
    * Data logged: monitor pointer
* Lock Release
    * Data logged: monitor pointer
* Object Allocation
    * Data logged: object pointer
* GC Timestamp
    * Data logged: timestamp when a stop-the-world compacting GC starts

As Java is natively multi-threaded,
we have two kinds of logger, a global logger that writes everything in a same stream
and a thread-local logger that only write data into its own stream.
We need to associate the thread id for each event if we use the global logger.
