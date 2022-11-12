#!/bin/sh
# Shell script used to call the skill_start.py script to simplify
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
	/usr/bin/python3 skill_start.py
elif [ $mode == 'boss' ]
then
	/usr/bin/python3 boss_start.py
else
	echo 'Mode $mode not recognized'
fi

# Changes file permissions for the CSV data file so skill_update.py can
# read it.
sudo chmod -R 777 *.csv # Wildcard is a less than ideal solution so
                        # this will probably be replaced by pulling
                        # a value from a config file in the future

sudo chmod -R 777 *log*.txt # Makes logs accessible for future updates.
