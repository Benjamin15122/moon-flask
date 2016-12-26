title: Android


# Android




## mini-tracing-art


We believe that implementing a dynamic program analysis tool using bytecode instrumentation
at least has the following limitations:

* Overhead
* No sealed Android APKs
* No JDK classes

As a result, we prefer to custom the runtime environment (Java HotSpot VM and Android ART)
to implement everything as a drop-in replacement.


We have many versions of `mini-tracing-art`,
based on:

* [Android 5.0.1](https://bitbucket.org/txgu/mini-tracing-art5)
* [Android 6.0.1](https://bitbucket.org/txgu/mini-tracing-art6)
* [xposed-marshmallow](https://bitbucket.org/txgu/xposed-minitrace-art6)

MiniTracing on Android 5.0.1 supports the following functionalities/features:

* Coverage: at the bytecode instruction level
* Tracing: method enter/exit/unwind and field read/write events
* Fuzzing: throw exceptions or sleep for seconds at method entry/exit
* RaceFuzzer for Android: reschedule concurrent access to shared objects
    * Following the paper ["Race directed random testing of concurrent programs"](http://dl.acm.org/citation.cfm?id=1375584)


MiniTracing on Android 6.0.1 and [xposed-marshmallow](https://github.com/rovo89/android_art) now only support

* basic method event tracing
* coverage


## ape

[Ape](https://bitbucket.org/txgu/ape): `android-6.0.1_r41` only

* A more intelligent `monkey`
* Use  `uiautomator dump`(in fact based on [Accessibility Service](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService.html) of android framework) to guide monkey.
    * The command `uiautomator dump` has a delay.
      This tool uses the API used by the `uiautomator` to capture UI information immediately without any delay.
* Currently only two simple strategies: A random strategy and a DFS strategy. You can extend this tool with your own strategy.
    * By using MiniTracing for ART to profile the runtime, we could implement various kinds of feedback directed testing tools.




