title: 为android定制monkey
date: 2016-01-04
category: programming
tags: java,android
template: post.html

### 在模拟器镜像上执行ape

1. 准备好编译AOSP的环境，安装必须的依赖项、开发工具。具体参照这里：<https://source.android.com/source/requirements.html>。
2. 下载AOSP的源码，由于ape是基于`android-6.0.1_r41`，所以最好是下载这个版本的AOSP源码。具体参照这里：<https://source.android.com/source/downloading.html>。

    !!! note:
        国内可以使用中科大的镜像<https://mirrors6.ustc.edu.cn/>，具体的help文档可以参照<https://lug.ustc.edu.cn/wiki/mirrors/help/aosp>

3. [ape](https://bitbucket.org/txgu/ape)的代码是基于[development](https://github.com/android/platform_development)子项目的，
   该子项目在下载好的本地ASOP代码树的`development`目录里，通过`git add remote ape git@bitbucket.org:txgu/ape.git`添加remote，
   之后通过`get pull ape master`下载ape的master分支。
4. 按照<https://source.android.com/source/building.html>描述的编译方法：先`source build/envsetup.sh`，再`lunch aosp_arm-eng`，然后`make -jN`（`N`并行编译的线程数），最后启动模拟器`emulator`。

    !!! note:
        按照官网的指示会编译所有模块，具体的模块可以通过`make modules`查看所有模块。
        在镜像编译之后的，如果只编译`monkey`可以通过`make monkey`。
        此外，AOSP里自带一个emulator，通过`source build/envsetup.sh`设置好环境变量之后的终端里，
        通过`emulator`会设定好各种变量，默认打开新编译的镜像。

5. 启动镜像之后就可以通过`adb shell`登陆上手机，执行`monkey`可以查看帮助文档。实际上，ape只增加了两个选项，具体参照[源码](https://bitbucket.org/txgu/ape/src/a990b1439635aa8f13fdad3b4138a36e071e45f3/cmds/monkey/src/com/android/commands/monkey/Monkey.java?at=master&fileviewer=file-view-default#Monkey.java-778)

    !!! note:
        ape只修改了一个文件[Monkey.java](https://bitbucket.org/txgu/ape/src/master/cmds/monkey/src/com/android/commands/monkey/Monkey.java?at=master&fileviewer=file-view-default#Monkey.java)
        添加了两个文件[MonkeySourceRandomUiAutomator.java](https://bitbucket.org/txgu/ape/src/master/cmds/monkey/src/com/android/commands/monkey/MonkeySourceRandomUiAutomator.java?at=master&fileviewer=file-view-default)和[MonkeySourceUiAutomatorDFS](https://bitbucket.org/txgu/ape/src/master/cmds/monkey/src/com/android/commands/monkey/MonkeySourceUiAutomatorDFS.java?at=master&fileviewer=file-view-default)

### **2016-10-13更新**

之前的系统是在`android-5.0.1`上的，
后来换到了`android-6.0.1_r41`，在`make monkey`之后搜索`javalib.jar`，无需`dx`，直接替换即可。

项目在[bitbucket](https://bitbucket.org/txgu/ape)上。

~~~{.bash}
#! /bin/bash

ADB=$(which adb)

if [[ "x$ADB" == "x"  ]];
then
    echo "No adb in $PATH"
    exit 1
fi

ANDROID_HOME=$(pushd "$(dirname "$BASH_SOURCE[0]")" > /dev/null && pwd && popd > /dev/null )

#"${ANDROID_HOME}/out/host/linux-x86/bin/dx" --dex --output=${ANDROID_HOME}/out/monkey.jar "${ANDROID_HOME}/out/target/common/obj/JAVA_LIBRARIES/monkey_intermediates/classes.jar"
$ADB push ${ANDROID_HOME}/out/target/common/obj/JAVA_LIBRARIES/monkey_intermediates/javalib.jar /sdcard/monkey.jar
#$ADB push "${ANDROID_HOME}/out/target/product/generic/system/framework/monkey.jar" /sdcard/
#$ADB push "${ANDROID_HOME}/out/target/product/generic/system/framework/oat/arm/monkey.odex" /sdcard/
$ADB shell su -c mount -o remount,rw /system
$ADB shell su -c mv /sdcard/monkey.jar /system/framework/monkey.jar
#$ADB shell su -c mv /sdcard/monkey.odex /system/framework/oat/arm/monkey.odex
$ADB shell su -c chmod 644 /system/framework/monkey.jar #/system/framework/oat/arm/monkey.odex
$ADB shell su -c chown root:root /system/framework/monkey.jar #/system/framework/oat/arm/monkey.odex
#$ADB shell su -c chmod 644 /system/framework/arm/monkey.odex
#$ADB shell su -c chown root:root /system/framework/arm/monkey.odex
#$ADB shell su -c cp /system/framework/arm/monkey.odex /data/dalvik-cache/arm/system@framework@monkey.jar@classes.dex
#$ADB shell su -c chmod 644 /data/dalvik-cache/arm/system@framework@monkey.jar@classes.dex
#$ADB shell su -c chown system:system /data/dalvik-cache/arm/system@framework@monkey.jar@classes.dex
#$ADB shell su -c patchoat --instruction-set=arm --input-oat-location=/system/framework/arm/monkey.odex --output-oat-file=/data/dalvik-cache/arm/system@framework@monkey.jar@classes.dex

#$ADB shell su -c stop zygote
#$ADB shell su -c start zygote

~~~

## ape的想法和实现

最近在准备抛弃动态更新转向测试，着手做的事情是android上的测试。
在android手机里，有一个命令行工具叫做`monkey`，通过这个命令可以生成一些事件，例如`touch`，`scroll`等。
monkey做的`touch`是随机的，不考虑当前界面的具体点击后有反应的地方，这样效率就比较低。
一个改进的地方就是dump出当前GUI layout，幸运的是在android4.4之后有一个命令行工具叫做`uiaotumator`。
这个工具是基于AccessibilityService的，简单来说，monkey和uiautomator虽然都是命令行工具，
但是他们都是用java开发，直接调用了android framework里的API。
因此，我们可以很方便的将其结合起来。

由于我从来没有开发过一个android的app，对工具链也不是很熟悉，所以我直接在下载的AOSP里的monkey源码上修改了。
具体的修改就是把monkey的源码和uiautomator的源码结合起来，得到一个新的被我命名为[ape](http://bitbucket.org/txgu/ape)的随机测试工具。
ape继承了monkey生成事件的能力和uiautomator获得界面layout的能力。

编译很简单，直接在AOSP里通过`make monkey`即可，最后生成一个空的`monkey.jar`和包含`arm/monkey.odex`文件。
我也不知道也没时间去了解如何安装这两个文件，
最简单的就是替换在android系统里`/system/framework/monkey.jar`和`/system/framework/arm/monkey.odex`。
结果，由于实际上用的是在`/data/dalvik-cache/arm`里的文件，根据目测，直接将`monkey.odex`拷贝并重命名为`system@framework@monkey.jar@classes.dex`，
结果不幸过不了校验。

万般无奈之下只好自己打包生成`monkey.jar`替换，然后让dex2oat自己去生成各种cache文件。

用了下面一个脚本，在nexus 5上亲测有效。

~~~{.bash}
#! /bin/bash

ADB=$(which adb)

if [[ "x$ADB" == "x"  ]];
then
    echo "No adb in $PATH"
    exit 1
fi

ANDROID_HOME=$(pushd "$(dirname "$BASH_SOURCE[0]")" > /dev/null && pwd && popd > /dev/null )

"${ANDROID_HOME}/out/host/linux-x86/bin/dx" --dex --output=${ANDROID_HOME}/out/monkey.jar "${ANDROID_HOME}/out/target/common/obj/JAVA_LIBRARIES/monkey_intermediates/classes.jar"
$ADB push ${ANDROID_HOME}/out/monkey.jar /sdcard/monkey.jar
$ADB shell su -c mount -o remount,rw /system
$ADB shell su -c mv /sdcard/monkey.jar /system/framework/monkey.jar
$ADB shell su -c chmod 644 /system/framework/monkey.jar
$ADB shell su -c chown root:root /system/framework/monkey.jar
~~~



