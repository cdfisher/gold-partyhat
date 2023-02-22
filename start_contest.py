"""start_contest.py
Script to start tracking group members for a skill-, boss-, or activity-based competition.
Also updates a master dataframe that tracks all entries on each user's highscores page.

All arguments other than contest_id are optional and are used to override existing settings.
To add a new contest, first run setup_contest.py.

@:arg contest_id: str Identifier used to look up contest settings in contest-table.txt
@:arg --threshold: int The minimum increase in score a user needs to gain during the contest in order to be
considered a participant at the end. Default value: 100
@:arg --top_n: int The number of top participants to list when running updates. Default value: 5
@:arg --winners: int The number of contest winners. Default value: 3
@:arg --raffle_winners: int The number of participation prizes available. Default value: 3
@:arg --participants: int The number of top participants to include in the end of contest raffle
if raffle_mode = 'top_participants'.
@:arg --silent, -s: bool Optional argument to disable sending of messages to Discord when running contest
scripts for the duration of the contest. Defaults to False
@:arg --quiet, -q: bool Runs script without sending messages to Discord, but does not stop other updates run for
this contest from sending messages. Defaults to False

Example call for a contest:

"python start_contest.py '241a5306'"
"""

import os
import argparse
from time import sleep
from contests import *
from data_updater import *
from gph_utils.gph_logging import log_message
from webhook_handler import WebhookHandler

# Establish and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('contest_id', type=str, help='Unique contest identifier.')
parser.add_argument('--threshold', type=int, help='The amount of XP, KC, or score needed '
                                                  'to be counted as a participant.')
parser.add_argument('--top_n', type=int, help='The number of top participants to list when '
                                              'updating the contest.')
parser.add_argument('--winners', type=int, help='The number of contest winners.')
parser.add_argument('--raffle_winners', type=int, help='The number of participation prizes'
                                                       ' available.')
parser.add_argument('--participants', type=int, help='The number of participants to include'
                                                     ' in the end of contest raffle if '
                                                     'raffle_mode = "top_participants"')
parser.add_argument('-s', '--silent', help='Runs script without sending messages to Discord,'
                                           ' and persists for the whole contest.',
                    action='store_true')
parser.add_argument('-q', '--quiet', help='Runs script without sending messages to Discord,'
                                          ' but does not stop other updates run for this '
                                          'contest from sending messages.',
                    action='store_true')

# Get contest ID to fetch contest from contest table file
args = parser.parse_args()
contest_id = args.contest_id

# Load contest table from file
with open('contest-table.txt', 'rb') as infile:
    indata = infile.read()

indata = eval(indata)
contest_table = ContestTable(indata)
contest = contest_table.get_contest(contest_id)

# Fetch contest vars from settings
(contest_id, title, mode, target, threshold, units, group, top_n, winners, raffle_mode,
 raffle_winners, silent, start, end, interval, update_number, n_participants,
 dynamic_prizes, datafile, logfile, multi_targets) = contest.get_all_data()

# Parse command line arguments to override stored contest settings if used
if args.threshold is not None:
    threshold = args.threshold
    contest.update_entry('threshold', threshold)
if args.top_n is not None:
    top_n = args.top_n
    contest.update_entry('top_n', top_n)
if args.winners is not None:
    winners = args.winners
    contest.update_entry('winners', winners)
if args.raffle_winners is not None:
    raffle_winners = args.raffle_winners
    contest.update_entry('raffle_winners', raffle_winners)
if args.participants is not None:
    n_participants = args.participants
    contest.update_entry('n_participants', n_participants)
silent = args.silent
contest.update_entry('silent', silent)
quiet = args.quiet

# Log start of contest
log_message(f'Starting competition for {mode} {target}, running Gold '
            f'Partyhat {GPH_VERSION}', log=logfile)
log_message(f'Contest name: {title}, contest ID: {contest_id}', log=logfile)

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
        file.write(f'{rsn:<12}        {score:>12,}\n')

log_message(f'Competition started successfully. Tracking {n_users} '
            f'members.', log=logfile)

# Write contest table to file to update any changed settings
contest_table.to_file('contest-table')

embed = [
    {
        "title": f"Running {BOT_NAME} {GPH_VERSION}",
        "color": 16768768,
        "description": f"{title} has begun. Get {threshold:,} {units} to be eligible for the "
                       f"participation raffle!\n\n{n_users} players are being tracked.",
        "fields": [
            {
                "name": "Contest ID:",
                "value": f'{contest_id}',
                "inline": "false"
            }
        ]
    }
]

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a start of contest message and the list of players' starting scores as a Discord
# message via a webhook.
if not (silent | quiet):
    wh = WebhookHandler()
    msg = ''
    wh.send_embed(msg, embeds=embed)
    # Small delay to let the embed request arrive before the files
    # Minor workaround for now
    sleep(0.4)
    wh.send_file(msg, filename=fname)

# Remove the file listing the starting scores
os.remove(fname)
