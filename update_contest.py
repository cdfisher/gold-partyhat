"""update_contest.py
Script to update group members' progress in a skill-, boss-, or activity-based
competition.
Additionally, updates a master dataframe that tracks all entries on each user's highscores page.

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

"python update_contest.py '241a5306'"
"""

import argparse

from os import remove
from time import sleep
from contests import *
from data_updater import *
from gph_logging import log_message
from gph_graphing import make_graph
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
                                           ' and persists for the whole contest.', action='store_true')
parser.add_argument('-q', '--quiet', help='Runs script without sending messages to Discord, but does not stop '
                                          'other updates run for this contest from sending messages.',
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

log_message(f'Updating contest {title}, contest ID: {contest_id}.', log=logfile)

update_number += 1
contest.update_entry('update_number', update_number)

# Load master dataframe from file
master_df = pd.read_csv(MASTER_DF_NAME)

# Run the contest update procedure and make copies of both dataframes
master_df, contest_df = update_entry(group, mode, target, 'update', update_number, master_df, logfile,
                                     datafile, contest_id)

participants = set()

msg = ''
fields = []

# TODO See if I can partially wrap creation of the progress file
# TODO into these next two loops
# TODO See if I can wrap creation of graph_data into this chunk of code
# Make a list of the top_n participants
for i in range(top_n):
    rsn = contest_df.at[i, 'RSN']

    if contest_df.at[i, 'Gained'] >= threshold:
        participants.add(rsn)
    fields.append({
        "name": f"{i + 1}) {rsn}",
        "value": f'{contest_df.at[i, "Gained"]:,} {units} gained',
        "inline": 'false'
    })

embed = [
    {
        "title": f"{title} top {top_n} (so far)",
        "color": 16768768,
        "description": f"",
        "fields": fields

    }
]

# Make a list of all participants outside the top_n who still meet the
# threshold for participation.
for i in range(top_n, len(contest_df.index)):
    gained = contest_df.at[i, 'Gained']
    if gained >= threshold:
        rsn = contest_df.at[i, 'RSN']
        participants.add(rsn)
    else:
        break

# Create progress graph to send in Discord

# Collect data on the progress of the top_n in a 2D list
ranked_users = []
graph_data = [ranked_users]
for i in range(top_n):
    rsn = contest_df.at[i, 'RSN']
    ranked_users.append(rsn)
    player_data = []
    for j in range(update_number + 1):
        try:
            row = master_df.loc[(master_df['RSN'] == rsn) & (master_df['Update number'] == j) &
                                (master_df['Update source'] == contest_id)]
            player_data.append(row.iloc[0][target])
        except IndexError:
            log_message(f'Index error encountered while graphing {rsn} at index {j}')
            continue

        except (KeyError, ValueError):
            # Possibly encountered if a player changes names partway through a contest.
            # TODO handle this a little more robustly
            log_message(f'A data error was encountered for user {rsn} at update #{j}.\n'
                        f'This may be the result of a name change.')
            continue

    start_value = player_data[0]
    for k in range(len(player_data)):
        player_data[k] = player_data[k] - start_value
    graph_data.append(player_data)
graph_data[0] = ranked_users

update_list = []
for i in range(update_number + 1):
    update_list.append(i)

# get name of plotfile
plotname = f'{title} top {top_n} progress'
plotfile = plotname.replace(' ', '-') + f'-update-{update_number}.png'
plotfile = plotfile.lower()

make_graph(graph_data, update_list, units, plotname, plotfile)

# Make file listing the ranks of everyone who has increased
# their score since the start of the contest.
textfile = datafile[:-4] + f'-update-{update_number}-gains.txt'
with open(textfile, 'w') as file:
    file.write(f'{title} progress update #{update_number}\n'
               f'------------------------------------------\n')
    file.write(f'Rank: RSN:            {units:>6} gained\n')
    for i in range(len(contest_df.index)):
        rsn = contest_df.at[i, 'RSN']
        gain = contest_df.at[i, 'Gained']
        if gain <= 0:
            break
        file.write(f'{i + 1:>3})  {rsn:<12}     {gain:>12,}\n')

log_message(f'Progress file {textfile} created successfully.', log=logfile)

# List participants who have reached the contest threshold
par_len = len(participants)
if par_len == 0:
    line = '\nNobody has met the participation threshold for a prize so ' \
           'far! Can you be the first?\n'
elif par_len == 1:
    line = '\nOnly one player has met the participation threshold for a prize so ' \
           'far!\n'
else:
    line = f'\n{par_len} have met the participation threshold for a prize so ' \
           'far!\n'

msg += line
par_srtd = sorted(participants)

for x in par_srtd:
    msg += x + '\n'

# Save dataframes to file
contest_df.to_csv(datafile, index=False)
master_df.to_csv(MASTER_DF_NAME, index=False)

log_message(f'Contest {contest_id} successfully updated.', log=logfile)

# Write contest table to file to update any changed settings
contest_table.to_file('contest-table')

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a list of the top_n and the list of players' progress as a Discord
# message via a webhook.
if not (silent | quiet):
    wh = WebhookHandler()

    # Using with resolves an issue where the files sent to Discord using add_file() could not be removed
    with open(plotfile, 'rb') as pf:
        wh.send_embed('', embeds=embed)
        # Small delay to let the embed request arrive before the files
        # Minor workaround for now
        sleep(0.4)
        wh.add_file(pf, plotfile)
        wh.send_file(msg, filename=textfile)

# Remove the text file with everyone's progress and the plot image after sending them to
# Discord
remove(textfile)
remove(plotfile)
