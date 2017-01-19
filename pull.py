#! /usr/bin/python2

import os, sys, traceback, subprocess

MOON_DIR=os.path.abspath(os.path.dirname(__name__))

cmds = ['git -C {MOON_DIR} pull origin master',
        'git -C {MOON_DIR} submodule init',
        'git -C {MOON_DIR} submodule update',
        'git -C {MOON_DIR} submodule foreach git pull origin master']


if __name__ == '__main__':
    try:
        for cmd in cmds:
            subprocess.check_call(cmd.format(MOON_DIR=MOON_DIR).split(' '))
    except:
        traceback.print_exc()
        exit(1)
