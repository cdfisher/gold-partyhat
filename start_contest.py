"""start_contest.py
Script to start tracking group members for a skill-, boss-, or activity-based competition.
Also updates a master dataframe that tracks all entries on each user's highscores page.

@:arg target: str in hs.SKILLS, hs.ACTIVITIES, or hs.BOSSES denoting the specific target to track.
@:arg title: str The name of the contest.
@:arg threshold: int The minimum increase in score a user needs to gain during the contest in order to be
considered a participant at the end.
@:arg group: str The name of the text file listing group members to track, excluding the file extension.
@:arg top_n: int The number of top participants to list when running updates
@:arg winners: int The number of contest winners.
@:arg raffle_winners: int The number of participation prizes available.
@:arg start: str representation of a datetime object in the form '[DD MM YYYY - HH:MM]' to mark the start of the
contest. Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg end: str representation of a datetime object in the form '[DD MM YYYY - HH:MM]' to mark the end of the
contest. Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg --raffle_mode: str in {'classic', 'top_participants'}. Optional flag defaulting to 'top_participants' used
to set how the end of contest raffle works.
@:arg --datafile: str. Optional flag to set the name of the file where contest data is stored, not including a file
extension.  Defaults to title.lower.replace(' ', '-')
@:arg --logfile: str. Optional flag to set the name of the file where log messages are stored, not including a file
extension.  Defaults to (title.lower.replace(' ', '-') + '-log')
@:arg --interval: int Optional argument to set the interval at which the contest updates, in hours. Defaults to 6.
Included for future use by a planned feature to automatically create cronjobs. Not yet used.
@:arg --silent, -s: bool Optional argument to disable sending of messages to Discord when running contest
scripts for the duration of the contest. Defaults to False
@:arg --quiet, -q: bool Runs script without sending messages to Discord, but does not stop other updates run for
this contest from sending messages. Defaults to False

Example call for a contest:

"python start_contest.py 'skill' 'attack' 'Attack test contest' 5000 'my_group' 5 3 3
 '[01 12 2022 - 19:00]' '[08 12 2022 - 19:00]'"
"""
import os
import argparse
from hashlib import sha1
from gph_config import *
from data_updater import *
from gph_logging import log_message
from webhook_handler import WebhookHandler

# Establish and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, help='The goal to track with this contest.')
parser.add_argument('title', type=str, help='Title of the contest.')
parser.add_argument('threshold', type=int, help='The amount of XP, KC, or score needed to be counted as a participant.')
parser.add_argument('group', type=str, help='Name of the text file where group members are listed, excluding the'
                                            'file extension.')
parser.add_argument('top_n', type=int, help='The number of top participants to list when updating the contest.')
parser.add_argument('winners', type=int, help='The number of contest winners.')
parser.add_argument('raffle_winners', type=int, help='The number of participation prizes available.')
parser.add_argument('start', type=str, help='Timestamp marking the start of the contest, '
                                            'in the form "[DD MM YYYY - HH:MM]."')
parser.add_argument('end', type=str, help='Timestamp marking the end of the contest, '
                                          'in the form "[DD MM YYYY - HH:MM]."')
parser.add_argument('--raffle_mode', type=str, choices=['classic', 'top_participants'], default='top_participants',
                    help='The mode to use at the end of the contest to draw participation prizes.')
parser.add_argument('--datafile', type=str, help='File name of where to save contest data, excluding the extension.')
parser.add_argument('--logfile', type=str, help='File name of where the logs will be saved, excluding the extension.')
parser.add_argument('--interval', type=int, default=6, help='The number of hours between updates.')
parser.add_argument('-s', '--silent', help='Runs script without sending messages to Discord,'
                                           ' and persists for the whole contest.', action='store_true')
parser.add_argument('-q', '--quiet', help='Runs script without sending messages to Discord, but does not stop '
                                          'other updates run for this contest from sending messages.',
                    action='store_true')

# Assign variables from args and use defaults if no value given
args = parser.parse_args()
target = args.target
title = args.title
threshold = args.threshold
group = args.group + '.txt'
top_n = args.top_n
winners = args.winners
raffle_winners = args.raffle_winners
start = args.start
end = args.end
raffle_mode = args.raffle_mode
if args.datafile is None:
    datafile = title.replace(' ', '-')
    datafile = datafile.lower() + '.csv'
else:
    datafile = args.datafile + '.csv'
if args.logfile is None:
    logfile = title.replace(' ', '-')
    logfile = logfile.lower() + '-log.txt'
else:
    logfile = args.logfile + '.txt'
interval = args.interval
silent = args.silent
quiet = args.quiet

mode = ''
if target in hs.SKILLS:
    mode = 'skill'
elif target in hs.ACTIVITIES:
    mode = 'activity'
elif target in hs.BOSSES:
    mode = 'boss'
else:
    log_message(f'Target \'{target}\' not found, unable to set mode', log=logfile)

# Generate an 8 character code as a contest identifier. Not currently used but
# implemented for a planned future feature.
contest_id = str(sha1((mode + target + title + start + end).encode('utf-8')))[-9:-1]

units = ''

update_number = 0

# Set units appropriate to the contest's target
if mode == 'boss':
    units = 'KC'
elif mode == 'skill':
    units = 'XP'
elif mode == 'activity':
    if target == 'league_points' or 'bounty_hunter' in target:
        units = 'points'
    elif 'clue' in target:
        units = 'caskets'
    elif 'rank' in target:
        units = 'rank'
    elif target == 'soul_wars_zeal':
        units = 'zeal'
    elif target == 'rifts_closed':
        units = 'rifts closed'
    else:
        log_message(f'Activity "{target}" not recognized.', log=logfile)
else:
    log_message(f'Mode {mode} not recognized.', log=logfile)

# Start building start-of-contest message to send to Discord
msg = f'Running {BOT_NAME} {GPH_VERSION}\n'
log_message(f'Starting competition for {mode} {target}, running Gold '
            f'Partyhat {GPH_VERSION}', log=logfile)
log_message(f'Contest name: {title}', log=logfile)

# Load master_df if it exists as a file, otherwise start with an empty df as master_df.
if os.path.exists(MASTER_DF_NAME):
    master_df = pd.read_csv(MASTER_DF_NAME)
else:
    master_df = pd.DataFrame(columns=master_colnames)

# Run the start of contest procedure and create the initial contest dataframe.
contest_df = update_entry(group, mode, target, 'start', update_number,
                          master_df, logfile, datafile, contest_id)

n_users = len(contest_df.index)

# Make .txt file of everyone's starting score to send to Discord
fname = datafile[:-4] + '-starting-scores.txt'
with open(fname, 'w') as file:
    file.write(f'{title} starting scores\n---------------------------------\n')
    file.write(f'RSN:                      {units:>6}\n')
    for i in range(len(contest_df.index)):
        rsn = contest_df.at[i, 'RSN']
        score = contest_df.at[i, 'Current']
        file.write(f'{rsn:<12}        {score:>12}\n')

msg += f'{n_users} players are being tracked!\n'
log_message(f'Competition started successfully. Tracking {n_users} '
            f'members.', log=logfile)

# Create an array of contest settings to save and then append it to datafile
contest_settings = [contest_id, mode, target, threshold, units, group, top_n, winners,
                    raffle_mode, raffle_winners, silent, start, end, interval,
                    0]
with open(datafile, 'a') as file:
    file.write(str(contest_settings))

# TODO create cron jobs via python-crontab

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a start of contest message and the list of players' starting scores as a Discord
# message via a webhook.
if not (silent | quiet):
    wh = WebhookHandler()
    wh.send_file(msg, filename=fname)

# Remove the file listing the starting scores
os.remove(fname)
