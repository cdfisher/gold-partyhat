#!/bin/sh
# Shell script used to call the skill_start.py script to simplify
# use of the bot with cron when run on a *nix-like OS (recommended).
/usr/bin/python3 skill_start.py

# Changes file permissions for the CSV data file so skill_update.py can
# read it.
sudo chmod -R 777 *.csv # Wildcard is a less than ideal solution so
                        # this will probably be replaced by pulling
                        # a value from a config file in the future

sudo chmod -R 777 *log*.txt # Makes logs accessable for future updates.
