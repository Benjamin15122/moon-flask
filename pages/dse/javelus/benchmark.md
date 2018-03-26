title: Benchmark

# Benchmark

1. Checkout the following four projects.
    * [javelus](https://bitbucket.org/javelus/javelus-samples)
    * [developer-interface](https://bitbucket.org/javelus/developer-interface)
    * [dpg](https://bitbucket.org/javelus/dpg)
    * [javelus-samples](https://bitbucket.org/javelus/javelus-samples)
2. Build each tool following its README.
    * `developer-interface` and `dpg` can be built via `ant`.
    * `javelus` can be built by following [Build Javelus on Linux](./build_linux).
    * `javelus-samples/agent`, `javelus-samples/tomcat-bms` and `javelus-samples/h2-bms` can be built via `ant`.
3. Run DaCapo Benchmark.
    * Run `javelus-samples/tomcat-bms/run.sh` or `javelus-samples/h2-bms/run.sh`
4. Run JMeter.
    * Download [JMeter](http://jmeter.apache.org/)
    * Learn how to run [JMeter](http://jmeter.apache.org/usermanual/get-started.html)
    * Check various JMemter scripts under `javelus-samples/tomcat-bms/jmeter`.

