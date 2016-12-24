title: Developing Javelus using Visual Studio


# Developing Javelus using Visual Studio

Checkout the source code of javelus.
There is a `create.bat` at `make/windows/`.

1. Install [cygwin](https://cygwin.com/)
    1. Download the 32-bit [setup-x86.exe](https://cygwin.com/setup-x86.exe).
    2. Run `setup-x86.exe`, you had better choose to install at `C:/cygwin` as this path is hard-coded.
    3. Select the closest mirror, e.g., http://mirrors.ustc.edu.cn. 
    4. Search and add all packages listed in the [README-build.html](http://hg.openjdk.java.net/jdk8u/jdk8u/file/b77f17326a42/README-builds.html).
    5. Append `C:\cygwin\bin` to your `PATH` environment variable.
2. Install Visual Studio 2012.
    1. The latest supported MSC version is 1700.
    2. `create.bat` generates a `jvm.vcxproj` based on the version of your MSC version.
         This version number is grepped from the output of an English version`cl.exe`
         So, if your have installed a Chinese version, set an environment variable `set FORCE_MSC_VER=1700`
3. Install a JDK 8, suppose that the `JDK8_HOME` points to the installation folder.
    1. Do not include any white space in the path.
4. Build VS project file.
    1. Open a new `cmd` terminal.
    2. Change directory to the VC location, e.g., `C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC`
    3. Setup environment variables by invoking `vcvarsall.bat amd64`.
    4. Change directory to the source code of this project in the same terminal.
    5. Change directory to `make/windows`, and you will find a file named `create.bat`
    6. Run `create.bat %JDK8_HOME%`
    7. If there is no error, you will find a `jvm.vcxproj` in the `build/vs-amd64`.
    8. Open this file and click update.
    9. Select the configuration `compiler2-fastdebug`, and click build project.
