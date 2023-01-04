# Gold Partyhat
## v0.5 beta
Contest tracking bot for Old School Runescape including Discord integration. 

This is written as a series of Python (and Bash) scripts intended to automate the tracking of Old 
School Runescape contests. As of v0.4, the bot can now track contests based on skilling, bossing,
or any activities listed on the OSRS highscores, such as Guardians of the Rift.

Gold Partyhat is intended to be run on a Raspberry Pi or other small computer, and currently
utilizes cron jobs to function. The bot was written to track several monthly contests for the group
of OSRS players I play with, so new features are largely driven by things we would like to use
ourselves. It will eventually be polished into a more cohesive package that's ready to
use right out of the box, but we had wanted to reach a critical mass of features first (Which we are
approaching).

#### Please note:
This project currently uses a fork of the osrs-highscores package which updates
it and resolves a few bugs that were preventing full functionality.
### Requirements:
#### Running on a Windows machine:
`pandas == 1.3.5`

`requests ~= 2.28.1`

`osrs-highscores @ git+https://github.com/cdfisher/osrs_highscores`

`matplotlib~=3.5.3`
#### Running on a Raspberry Pi
`numpy == 1.23.2`

`requests ~= 2.28.1`

`pandas ~= 1.4.3`

`osrs-highscores @ git+https://github.com/cdfisher/osrs_highscores`

`matplotlib~=3.5.3`
### Running the bot

For the time being, please see the docstrings for `start_contest.py`, 
`update_contest.py`, and `end_contest.py` for examples of how to call those
scripts.

### Using the automated weekly and monthly contests
Using `cron`, make sure your `crontab` file has `$HOME` set to the location of the directory
where you have saved the files for `Gold Partyhat`. Then add the following lines to your `crontab` file.
```
0  0  *     * 1     /usr/bin/bash $HOME/weekly_start.sh
55 23 *     * 7     /usr/bin/bash $HOME/weekly_end.sh
0  0  1     * *     /usr/bin/bash $HOME/monthly_start.sh
55 23 28-31 * *     /usr/bin/bash $HOME/monthly_end.sh
```

### Changelog
Starting with v0.4, any significant changes will be listed here.

#### v0.5

- Adds support for weekly and monthly contests tracking top XP gains
- Moves to using embeds where possible for cleaner messages

#### v0.4.2

- Reworks contest parameters to make it significantly simpler to start a contest from the command line
- Adds new optional flags `--force_id`, `--participants`, and `--dynamic_prizes`
- Corrects a potential issue with row id collision in the master dataframe

#### v0.4.1

- Adds graphing of the top players' progress with each contest update
- Includes rewrites of certain OSRS Highscores API-related functions
in order to be significantly cleaner and more idiomatic
- Corrects a design error introduced in v0.4 which caused contest updates to 
run significantly more slowly.

#### v0.4:

- With this update, I'm now considering Gold Partyhat to have enough features to consider it to be in beta!
- Major refactor of the contest scripts to combine boss and skill contests into one set of scripts
- The bot now supports activity based contests
- Configuration of contest parameters through the command line is now possible
- Contest update Discord messages now have more information
- Laid the foundations for some upcoming features