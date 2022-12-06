import os
import argparse
from hashlib import sha1
from gph_config import *
from data_updater import *
from gph_logging import log_message
from webhook_handler import WebhookHandler

parser = argparse.ArgumentParser()
parser.add_argument('mode', type=str, choices=['skill', 'boss', 'activity'], help='Whether to track a skill, '
                                                                                  'a boss, or an activity.')
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
parser.add_argument('-s', '--silent', help='Runs script without sending messages to Discord', action='store_true')

args = parser.parse_args()
mode = args.mode
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

contest_id = str(sha1((mode + target + title + start + end).encode('utf-8')))[-9:-1]

units = ''

update_number = 0

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

msg = f'Running {BOT_NAME} {GPH_VERSION}\n'
log_message(f'Starting competition for {mode} {target}, running Gold '
            f'Partyhat {GPH_VERSION}', log=logfile)
log_message(f'Contest name: {title}', log=logfile)

# load master_df if it exists, otherwise start with an empty df as master_df
if os.path.exists(MASTER_DF_NAME):
    master_df = pd.read_csv(MASTER_DF_NAME)
else:
    master_df = pd.DataFrame(columns=master_colnames)

# Run standard contest start procedure, saving each set of HS to master_df,
# and saving the relevant values to contest df

contest_df = update_entry(group, mode, target, 'start', update_number,
                          master_df, logfile, datafile)

n_users = len(contest_df.index)

# Make file of everyone's starting score
fname = datafile[:-4] + '-starting-scores.txt'
with open(fname, 'w') as file:
    file.write(f'{title} starting scores\n---------------------------------\n')
    file.write(f'RSN:                   {units}\n')
    for i in range(len(contest_df.index)):
        rsn = contest_df.at[i, 'RSN']
        score = contest_df.at[i, 'Current']
        file.write(f'{rsn:<12} {score:>12}\n')

msg += f'{n_users} players are being tracked!\n'
log_message(f'Competition started successfully. Tracking {n_users} '
            f'members.', log=logfile)

# make contest_settings array
# append contest_settings to datafile
contest_settings = [contest_id, mode, target, threshold, units, group, top_n, winners,
                    raffle_mode, raffle_winners, silent, start, end, interval,
                    0]
with open(datafile, 'a') as file:
    file.write(str(contest_settings))

# TODO implement python-crontab stuff here

if not silent:
    wh = WebhookHandler()
    wh.send_file(msg, filename=fname)
