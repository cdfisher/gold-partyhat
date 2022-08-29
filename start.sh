#!/bin/sh
# Shell script used to call the skill_start.py script to simplify
# use of the bot with cron when run on a *nix-like OS (recommended).
/usr/bin/python3 skill_start.py

# Changes file permissions for the CSV data file so skill_update.py can
# read it.
sudo chmod -R 777 star-thieving-test-ranks.csv # Replace with file name
                                               # used in gph_config.py
sudo chmod -R 777 *log*.txt # Makes logs accessable for future updates.