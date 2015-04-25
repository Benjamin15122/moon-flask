#! /bin/bash

MOON_DIR=/var/www/moon

git -C $MOON_DIR pull origin master
git -C $MOON_DIR submodule init
git -C $MOON_DIR submodule update
git -C $MOON_DIR submodule foreach git pull origin master
