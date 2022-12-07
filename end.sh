#!/bin/sh
# Shell script used to call the end_contest.py script to simplify
# use of the bot with cron when running on a *nix-like OS (recommended)
/usr/bin/python3 end_contest.py "$@"
