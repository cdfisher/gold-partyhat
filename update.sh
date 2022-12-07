#!/bin/sh
# Shell script used to call the update_contest.py script to simplify
# use of the bot with cron when running on a *nix-like OS (recommended).
/usr/bin/python3 update_contest.py "$@"
