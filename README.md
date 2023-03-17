# Gold Partyhat
## v0.7 beta
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

`urllib3~=1.25.11`

`python-dotenv~=0.21.1`

`python-crontab~=2.7.1`
#### Running on a Raspberry Pi
`numpy == 1.23.2`

`requests ~= 2.28.1`

`pandas ~= 1.4.3`

`osrs-highscores @ git+https://github.com/cdfisher/osrs_highscores`

`matplotlib~=3.5.3`

`urllib3~=1.25.11`

`python-dotenv~=0.21.1`

`python-crontab~=2.7.1`
### Running the bot

#### Initial setup
Before running the bot for the first time, a few environmental variables need to be set, typically in a `.env` file.


| **Environmental variable** | **Use**                                                                                                                                                       |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `WEBHOOK`                  | Default Discord webhook URL for the bot to use for messages                                                                                                   |
| `TOP_PLAYERS_WEBHOOK`      | (Optional) Discord webhook used by `top_players.py` for the weekly and monthly top player tracking.                                                           |
| `TEST_WEBHOOK`             | (Optional) Discord webhook used in conjunction with setting `TEST_MODE` in `gph_config.py` to `1`. Sends messages to a separate channel for testing purposes. |


#### Using the bot

For the time being, please see the docstrings for `start_contest.py`, 
`update_contest.py`, and `end_contest.py` for examples of how to call those
scripts.

#### Setting up a contest

To set up a contest, run `setup_contest.py` as below:

`$ python3 setup_contest.py 'target' 'title' 'start_time' 'end_time' 'group'
--threshold 50000`

**setup_contest.py arguments:**

*Default values for these arguments are set in /gph_utils/gph_config.py*

| **Argument**                                   | **Type** | **Description**                                                                                                                                                                                    |
|------------------------------------------------|----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `target`                                       | `str`    | Skill, target, activity, or 'multi' (NYI) denoting the specific target to track                                                                                                                    |
| `title`                                        | `str`    | The name of the contest                                                                                                                                                                            |
| `start`                                        | `str`    | Representation of a Python `datetime` object in the form '[DD MM YYYY - HH:MM]' to mark the start of the contest.                                                                                  |
| `end`                                          | `str`    | Representation of a Python `datetime` object in the form '[DD MM YYYY - HH:MM]' to mark the end of the contest.                                                                                    |
| `group`                                        | `str`    | Name of the text file listing group members to track, excluding the file extension.                                                                                                                |
| *(Optional)* `--force_id`                      | `str`    | Manually sets contest_id to a given value. Otherwise defaults to generating an ID value.                                                                                                           |
| *(Optional)* `--threshold`                     | `int`    | Minimum increase in score a user needs to gain during the contest in order to be considered a participant at the end. Default value: 100                                                           |
| *(Optional)* `--top_n`                         | `int`    | Number of top participants to list when running updates. Default value: 5                                                                                                                          |
| *(Optional)* `--winners`                       | `int`    | Number of contest winners. Default value: 3                                                                                                                                                        |
| *(Optional)* `--raffle_winners`                | `int`    | Number of participation prizes available. Default value: 3                                                                                                                                         |
| *(Optional)* `--raffle_mode`                   | `str`    | Options: `classic`, `top_participants` (Default). Sets eiligbility rules for the end of contest raffle.                                                                                            |
| *(Optional)* `--participants`                  | `int`    | Number of top participants to include in the end of contest raffle if the raffle mode is set to `top_participants`. Default value: 10                                                              |
| *(Optional)* `--datafile`                      | `str`    | Manually sets the name of the file where contest data is stored, not including a file extension.  Defaults to title.lower.replace(' ', '-'), with any other special characters removed.            |
| *(Optional)* `--logfile`                       | `str`    | Manually sets the name of the file where log messages are stored, not including a file extension. Defaults to (title.lower.replace(' ', '-') + '-log'), with any other special characters removed. |
| *(Optional)* `--interval`                      | `int`    | Interval (in hours) at which the contest tracking updates. Default value: 6                                                                                                                        |
| *(Optional)* `--silent`, `-s`                  | None     | If used, disables the sending of messages to Discord when running contest scripts for the duration of the contest.                                                                                 |

#### Removing a contest

To remove a contest, run `remove_contest.py` as below:

`$ python3 remove_contest.py 'contest_id'`

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

#### v0.7
- Adds automatic management of contest cron jobs via `python-crontab`.
- Improved documentation.

#### v0.6

- Returned to using environmental variables to store API secrets rather than a configuration file.
- Implemented a contest table file and significantly simplified the process of
running a contest (Detailed instructions and documentation coming soon).
- Moved utility files into a dedicated subpackage `gph_utils`
- Multiple minor cleanup and restructuring items.
- Bash scripts are no longer needed to start, update, and end contests.

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