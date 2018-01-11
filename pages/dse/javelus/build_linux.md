title: Build javelus on Linux

# Build javelus on Linux


## Build

There is a `Makefile` inside `./make/`.
Before building the project, you need to set some variables.

1. A bootstrap JDK.
    * To avoid building the entire JDK, you have to download a `jdk1.8.0_65`.
2. You will get promoted message indicating which tool you are missing.
    * Possible tools: `gcc`, `zip`, `bison`...
    * A full list could be found at <http://hg.openjdk.java.net/jdk8u/jdk8u/raw-file/dcfe85bcd901/README-builds.html>
3. Javelus only support `amd64`. `ARCH_DATA_MODEL` must be set to 64.
4. Save the following `quick_build.sh` into `./make/`
5. By default, all versions (e.g., debug or product) are built.
    * Build a debug version by `./quick_build.sh fastdebug`.
    * Build a product version by `./quick_build.sh product`.


!!! note:
    Remember to update your `JDK_IMPORT_PATH`.


`quick_build.sh`:

```
#! /bin/bash

JOBS=1

which nproc
if [[ "x$?" == "x0" ]]; then
    JOBS=$(nproc)
fi

# Install a JDK 8 as the bootstrap JDK for building the hotspot in OpenJDK 8
export JDK_IMPORT_PATH=/home/t/.jdks/jdk1.8.0_65/
export ALT_BOOTDIR=$JDK_IMPORT_PATH

make HOTSPOT_BUILD_JOBS=$JOBS  ARCH_DATA_MODEL=64 $*
```
# Run

There is a script to launch the newly built hotspot JVM.

* `./build/linux/linux_amd64_compiler2/product/hotspot`.

You need to setup an environment varibale `ALT_JAVA_HOME`.

```{.bash}
export ALT_JAVA_HOME=/home/t/.jdks/jdk1.8.0_65
```
