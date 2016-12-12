title: MiniTracing for Android ART
date: 2015-10-25
category: programming
tags: java,android
template: post.html


## Install Script

Save the following script into your `$AOSP_HOME`.

~~~{.bash}
#! /bin/bash

ADB=$(which adb)

if [[ "x$ADB" == "x"  ]];
then
    echo "No adb in $PATH"
    exit 1
fi

AOSP_HOME=$(pushd "$(dirname "$BASH_SOURCE[0]")" > /dev/null && pwd && popd > /dev/null )


install_lib() {
 $ADB push "${AOSP_HOME}/out/target/product/generic/system/lib/$LIB_FILE" /sdcard/$LIB_FILE
 $ADB shell su -c cp /system/lib/$LIB_FILE /sdcard/$LIB_FILE.backup
 $ADB shell su -c mv /sdcard/$LIB_FILE /system/lib/$LIB_FILE
 $ADB shell su -c chmod 644 /system/lib/$LIB_FILE
 $ADB shell su -c chown root:root /system/lib/$LIB_FILE
}


LIBS=(libart.so libart-compiler.so)
$ADB shell su -c mount -o remount,rw /system

for LIB in ${LIBS[@]}
do
    LIB_FILE=$LIB
    install_lib
done

$ADB shell su -c reboot
~~~

##
