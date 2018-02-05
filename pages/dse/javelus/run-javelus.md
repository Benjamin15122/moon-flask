title: Run Javelus


# Run Javelus


To run Javelus, you should additionally disable some options:

* `-XX:-TieredCompilation`
* `-XX:-UseCompressedClassPointers`
* `-XX:-UseCompressedOops`

!!! note
    `-XX:-TieredCompilation` means option `TieredCompilation` is disabled.

You can simply invoke Javelus by script `hotspot` and aforementioned options.

```
./build/linux/linux_amd64_compiler2/fastdebug/hotspot -XX:-TieredCompilation -XX:-UseCompressedClassPointers -XX:-UseCompressedOops
```

Script `hotspot` uses `ALT_JAVA_HOME` to locate a bootstrap JDK.
Therefore, you should set `ALT_JAVA_HOME` to your `jdk1.8.0_65`.

```
export ALT_JAVA_HOME=/home/t/.jdks/jdk1.8.0_65/
```

Actually, you can start Javelus by the jvm launcher.

```
./jdk1.8.0_65/bin/java -Dsun.java.launcher=gamma -XXaltvm=<target-dir>  -XX:-TieredCompilation -XX:-UseCompressedClassPointers -XX:-UseCompressedOops
```

where `target-dir` is the directory containing all built objects, e.g., `./build/linux/linux_amd64_compiler2/fastdebug`.

!!! note
    Windows users should write a DOS batch script to facilitate launching Javelus.
