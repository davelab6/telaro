#!/bin/sh
# you will need to read the top level README, and run boostrap.py
# in order to make pyjsbuild

options="$*"
#if [ -z $options ] ; then options="-O";fi
~/src/sf.pyjamas/svn-pyjamas/pyjamas/bin/pyjsbuild --print-statements $options dash2
