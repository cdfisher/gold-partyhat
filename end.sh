#!/bin/sh
# Shell script used to call the skill_end.py script to simplify
# use of the bot with cron when run on a *nix-like OS (recommended).
#
# Use -m 'boss' or -m 'skill' to set mode.

while getopts m: flag
do
	case "${flag}" in
		m) mode=${OPTARG};;
	esac
done

if [ $mode == 'skill' ]
then
	/usr/bin/python3 skill_end.py
elif [ $mode == 'boss' ]
then
	/usr/bin/python3 boss_end.py
else
	echo 'Mode not recognized'
fi
