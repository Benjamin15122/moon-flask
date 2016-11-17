title: Run Ares on Linux

# Run Ares on Linux


## Get Source

Checkout the following projects.

* [ares](https://bitbucket.org/txgu/ares)
* [ares-jpf](https://bitbucket.org/txgu/ares-jpf)


You should download a `jdk1.8.0_65` from oracle to build Ares.

## Build

### Ares-JPF


1. Just use [ant](http://ant.apache.org)

!!! note
    `ares-jpf` depends on an old version of JPF.
    I have to build a local `jpf-core` in `ares-jpf` since
    [JPF](http://babelfish.arc.nasa.gov/hg/jpf/jpf-core/) has reset its source history.

### Ares

1. Install `redis` and `libhiredis-dev`
    * For a feature under development.
2. Check `make\quick_build.sh`
    * In default, this script will build all configurations.
      Usually I only build two configurations, i.e., `product` and `fastdebug`.
      You can specify a configuration.

            quick_build.sh fastdebug

3. If everything is OK, you will find a script `hotspot` at `build/linux/linux_amd64_compiler2/fastdebug/hotspot`
   Run this script as a replacement of the command `java`.

        hotspot HelloWorld

## Setup


Ares can be used as a drop-in replacement of `java`
and it provides many extra options.

* Checkout the options declared in [globals.hpp](https://bitbucket.org/txgu/ares/src/master/src/share/vm/runtime/globals.hpp?at=master&fileviewer=file-view-default#globals.hpp-3948)

The following is what I have set during my evaluation.
~~~{.bash}
ARES_LOG="-XX:TraceRuntimeRecovery=2048"
# JVM has two JIT compilers, c1 (compiler1) and c2 (compiler2).
# We only implemented Ares on c2.
# So, disable c1 here.
ARES_VM="-XX:-TieredCompilation"

export ARES_HOME=/code/ares/hotspot/
export ARES_JPF_HOME=/code/ares/ares-jpf
export ARES_BIN=${ARES_HOME}/build/linux/linux_amd64_compiler2/fastdebug/hotspot


# JPF Options
ARES_JPF="${ARES_JPF_HOME}/ares-jpf.jar:${ARES_JPF_HOME}/lib/jpf-classes.jar:${ARES_JPF_HOME}/lib/jpf.jar"

# Use JPF
export JPF="$ARES_VM $ARES_LOG -XX:+UseJPF -Xbootclasspath/a:${ARES_JPF}"

# Use 1-ER
export FER="$ARES_VM $ARES_LOG -XX:-UseErrorTransformation -XX:+UseEarlyReturn -XX:-OnlyEarlyReturnVoid"

# Use VOER
export VOER="$ARES_VM $ARES_LOG -XX:-UseErrorTransformation -XX:+UseEarlyReturn -XX:+OnlyEarlyReturnVoid"

# Use SBET
export SBET="$ARES_VM $ARES_LOG -XX:+UseErrorTransformation -XX:-UseEarlyReturn -XX:+UseStack -XX:-UseForceThrowable"

# Use FTET
export FTET="$ARES_VM $ARES_LOG -XX:+UseErrorTransformation -XX:-UseEarlyReturn -XX:-UseStack -XX:+UseForceThrowable"
~~~

During my evaluation, I always created a script named `run.sh`.
So, I made the following aliases.
Therefore, `$RUN_FER` will be expand to `JAVA=$ARES_BIN VM_OPTS=$FER ./run.sh > fer.txt`.

~~~{.bash}
export RUN_FER="JAVA=\"$ARES_BIN\"  VM_OPTS=\"$FER\" ./run.sh > fer.txt"
export RUN_VOER="JAVA=\"$ARES_BIN\" VM_OPTS=\"$VOER\" ./run.sh > voer.txt"
export RUN_SBET="JAVA=\"$ARES_BIN\" VM_OPTS=\"$SBET\" ./run.sh > sbet.txt"
export RUN_FTET="JAVA=\"$ARES_BIN\" VM_OPTS=\"$FTET\" ./run.sh > ftet.txt"
export RUN_JPF="JAVA=\"$ARES_BIN\" VM_OPTS=\"$JPF\" ./run.sh > jpf.txt"
~~~


## Run

### Unit Test

Let's begin with a program that throws a `RuntimeException`.

~~~{.java}
import java.io.*;
public class ThrowRuntimeException{

    public static void do_throw_RuntimeException(){
        throw new RuntimeException();
    }

    public static void throw_IOException_wrapper() throws IOException{
        do_throw_RuntimeException();
        FileInputStream fis = new FileInputStream("hello.txt");

    }

    public static void do_throw_IOException(){
        try{
            throw_IOException_wrapper();
        }catch(IOException e){
            System.out.println("Catch an IOException " + e.toString());
        }
    }

    public static void do_catch_Exception(){
        try{
            do_throw_IOException();
        }catch(Exception e){
            System.out.println("Catch a/an " + e);
        }
    }

    public static void main(String []args){
        do_catch_Exception();
    }

}
~~~

1. Build it

    `javac ThrowRuntimeException.java`

2. Run it with `java`

    `java ThrowRuntimeException`

3. Run it with Ares

    `$ARES_BIN $FER ThrowRuntimeException`

Checkout the output and try to understand Ares how to mitigate an unchecked exception.

### ASE 2016

Subjects are hosted in [git.njuics.cn](https://git.njuics.cn/ares).

Every bug should has a `run.sh`.
Otherwise, send an email to me.

* [Tomcat](https://git.njuics.cn/ares/ares-tomcat)
* [Jetty](https://git.njuics.cn/ares/ares-jetty)
* [GanttProject](https://git.njuics.cn/ares/ares-ganttproject)
* [JMeter](https://git.njuics.cn/ares/ares-jmeter)
* If you cannot access this web site, send an email to me.


!!! warn
    Ares is only a prototype.
    If you encounter any crash,
    disable compiler by adding a VM option `-Xint` and then make a retry.


