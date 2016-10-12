title: 为android定制monkey
date: 2016-01-04
category: programming
tags: java,android
template: post.html

最近在准备抛弃动态更新转向测试，着手做的事情是android上的测试。
在android手机里，有一个命令行工具叫做`monkey`，通过这个命令可以生成一些事件，例如touch，scroll等。
monkey做的touch是随机的，不考虑当前界面的具体点击后有反应的地方，这样效率就比较低。
一个改进的地方就是dump出当前GUI layout，幸运的是在android4.4之后有一个命令行工具叫做`uiaotumator`。
这个工具是基于AccessibilityService的，简单来说，monkey和uiautomator虽然都是命令行工具，但是他们都是用java开发，直接调用了android framework里的API。
因此，我们可以很方便的将其结合起来。

由于我从来没有开发过一个android的app，对工具链也不是很熟悉，所以我直接在下载的AOSP里的monkey源码上修改了。
具体的修改就是把monkey的源码和uiautomator的源码结合起来，得到一个新的被我命名为ape的随机测试工具。
ape继承了monkey生成事件的能力和uiautomator获得界面layout的能力。

编译很简单，直接在AOSP里通过`make monkey`即可，最后生成一个空的`monkey.jar`和包含`arm/monkey.odex`文件。
我也不知道也没时间去了解如何安装这两个文件，最简单的就是替换在android系统里`/system/framework/monkey.jar`和`/system/framework/arm/monkey.odex`。
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

