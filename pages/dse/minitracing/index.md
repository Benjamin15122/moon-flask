title: MiniTracing for HotSpot
date: 2016-12-12
category: programming
tags: java,android
template: post.html


## Overview

MiniTracing (MT) for HotSpot aims to trace various events inside a running HotSpot JVM.

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
we have two kinds of logger, a global logger that writes everything in a same stream or buffer
and a thread-local logger that only write data into its own stream or buffer.
We need to associate the thread id for each event if we use the global logger.

A buffer is in length of events.
Currently, an event occupies 14 bytes, which is a very bad design.

* 2 bytes for indicating the type of events:
    * `TODO`: As we only support six types of events, three bits are enough if all method, object and timestamp are aligned to 8 bytes.
* 8 bytes for method, object and timestamps.
* 4 bytes for bytecode index (thread-local buffer only) or thread ID (the last 4 bytes of a thread object pointer when using global logger).

## Build and Install

Check instructions on how to build [`javelus`](../javelus/).

We have a pre-built version for windows.
Contact us for the latest built.

## Options

MT adds the following options to a standard JVM.

~~~{cpp}
bool EnableMiniTracing           = false;
intx MiniTracingBufferSize       = 1024;
bool MiniTracingBytecode         = false;
bool MiniTracingGlobalLogger     = false;
bool MiniTracingLockAcquire      = false;
bool MiniTracingLockRelease      = false;
bool MiniTracingMethodEntry      = false;
bool MiniTracingMethodExit       = false;
bool MiniTracingObjectAlloc      = false;
bool MiniTracingForwardPointers  = false;
~~~

* `EnableMiniTracing`: global switch for all tracing functionalities, e.g., create the output stream and buffer.
* `MiniTracingBufferSize`: a number control the largest number of events in a buffer.
* `MiniTracingBytecode`: if true, we will do a stack walk to fetch corresponding bytecode index (only for thread-local buffer).
* `MiniTracingGlobalLogger`: if true, we write everything into a global buffer.
* `MiniTracingLockAcquire`:
* `MiniTracingLockRelease`:
* `MiniTracingMethodEntry`:
* `MiniTracingMethodExit`:
* `MiniTracingObjectAlloc`:
* `MiniTracingForwardPointers`: Save the old address and the new address of an object when we copy or move it from during GC.


## Object ID

We use the address of an object or method as its ID.
However, an object may be moved during GC.
Therefore, we record every moving and split the trace log into fragments by the timestamp of a moving GC occurs.
An address may be used by different objects but is unique in a single fragment.


## Log

The log is uncompressed.
You can zip it.

## Log File Format

Checkout the project `log-parser` at <https://bitbucket.org/txgu/phd>.

### Method Map

To be added.

### Forward Pointer

To be added.

### Thread Logger Events

To be added.

### Global Logger Events

To be added.
