"""end_contest.py
Script to generate the final standings for an Old School Runescape
contest. Sends a message listing the winera and all players who
reached a set threshold for participation and selects winners to
receive participation prizes
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

"python end_contest.py '241a5306'"
"""

import random
import argparse
import matplotlib.pyplot as plt
from time import sleep
from data_updater import *
from os import remove
from math import floor
from contests import *
from gph_logging import log_message
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

# Assign variables from args and use defaults if no value given
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

log_message(f'Running final update for contest {title}, contest ID: {contest_id}.', log=logfile)

update_number += 1
contest.update_entry('update_number', update_number)

# Load master dataframe from file
master_df = pd.read_csv(MASTER_DF_NAME)

# Run the contest update procedure and make copies of both dataframes
master_df, contest_df = update_entry(group, mode, target, 'end', update_number,
                                     master_df, logfile, datafile, contest_id)

msg = ''

fields = []

win_emoji = [':first_place:', ':second_place:', ':third_place:']

for i in range(winners):
    rsn = contest_df.at[i, 'RSN']
    # Handle case in which there are more winners than we have emoji
    if i < 3:
        fields.append({
            "name": f"{win_emoji[i]}: {rsn}",
            "value": f'{contest_df.at[i, "Gained"]:,} {units} gained',
            "inline": 'false'
        })
    else:
        fields.append({
            "name": f"{i + 1}) {rsn}",
            "value": f'{contest_df.at[i, "Gained"]:,} {units} gained',
            "inline": 'false'
        })

embed = [
    {
        "title": f"{title} winners",
        "color": 16768768,
        "description": f"",
        "fields": fields

    }
]

# TODO look into generating the text file and graph_data simultaneously
# Create graph showing the progress of the winners to send in Discord

# Collect data on the progress of the winners in a 2D list
ranked_users = []
graph_data = [ranked_users]
for i in range(winners):
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

# Set up Pyplot to customize the appearance of the graph
text_color = '#99AAB5'
bg_color = '#333333'
plot_markers = ['o', '^', 's', 'X', 'D', 'v', '*', 'p']

with plt.rc_context({'axes.spines.right': False, 'axes.spines.top': False, 'axes.facecolor': bg_color,
                     'axes.edgecolor': text_color, 'axes.labelcolor': text_color, 'axes.titlecolor': text_color,
                     'xtick.color': text_color, 'ytick.color': text_color, 'legend.edgecolor': text_color,
                     'legend.fancybox': True, 'figure.facecolor': bg_color, 'figure.edgecolor': text_color,
                     'figure.titlesize': 'large'}):
    # Add lines for each of the top_n to the graph
    for i in range(len(graph_data[0])):
        plt.plot(update_list, graph_data[i + 1], label=graph_data[0][i], marker=plot_markers[i])

    # More plot setup
    plotname = f'{title} winners progress'
    plt.xticks(update_list)
    plt.xlabel('Update number')
    plt.ylabel(f'{units} gained')
    plt.title(plotname)
    plt.legend(facecolor='#36393F', labelcolor='#99AAB5')

    # Save plot to a file so it can be sent to Discord
    plotfile = plotname.replace(' ', '-') + f'-winner-progress.png'
    plotfile = plotfile.lower()
    plt.tight_layout()
    plt.savefig(plotfile)

# TODO Look into consolidating this section since there's a lot of shared code between modes
if raffle_mode == 'classic':
    # Use the original raffle mode in which any player reaching
    # the participation threshold was eligible to win the raffle.
    participants = set()

    # Add all participants who didn't win one of the main prizes to a set.
    for i in range(winners, len(contest_df.index)):
        gained = contest_df.at[i, 'Gained']
        if gained >= threshold:
            rsn = contest_df.at[i, 'RSN']
            participants.add(rsn)
        else:
            break

    line = f'\n{len(participants)} have met the participation threshold for a prize!\n'
    msg += line

    par_srtd = sorted(list(participants))

    for x in par_srtd:
        msg += x + '\n'

    # If using dynamic prize count, determine the number of prizes to award
    if dynamic_prizes:
        raffle_winners = 3 + floor(len(par_srtd) / 10)

    if len(par_srtd) <= raffle_winners:
        # If there are fewer participants than prize packages, everyone that reached the threshold gets one
        msg += 'There were enough prizes allotted for everyone listed above as a participant to get one!\n'
    else:
        # Otherwise draw prizes as normal
        msg += '\nThe winners of the participation prizes are:\n'

        r_winners = sorted(random.sample(par_srtd, raffle_winners))

        for w in r_winners:
            msg += w + '\n'

elif raffle_mode == 'top_participants':
    # Use raffle mode in which only the top n_participants who reached
    # the participation threshold but didn't win one of the main prizes
    # are eligible to win a raffle prize
    participants = set()

    # Make a set of everyone eligible for a prize
    for i in range(winners, winners + n_participants):
        gained = contest_df.at[i, 'Gained']
        if gained >= threshold:
            rsn = contest_df.at[i, 'RSN']
            participants.add(rsn)
        else:
            break

    line = f'\nHere are the top {len(participants)} who have met the participation ' \
           f'threshold of {threshold:,} {units} and are in the running for a participation ' \
           f'prize!\n'

    msg += line
    par_srtd = sorted(list(participants))
    for x in par_srtd:
        msg += x + '\n'

    if len(par_srtd) <= raffle_winners:
        # If there are fewer participants than prize packages, everyone that reached the threshold gets one
        msg += 'There were enough prizes allotted for everyone listed above as a participant to get one!\n'
    else:
        # Otherwise draw prizes as normal
        msg += '\nThe winners of the participation prizes are:\n'
        r_winners = sorted(random.sample(par_srtd, raffle_winners))
        for w in r_winners:
            msg += w + '\n'

else:
    # Raffle mode not supported
    log_message(f'Raffle mode \'{raffle_mode}\' not supported.\n', log=logfile)

# Make file listing the ranks of everyone who has increased
# their score since the start of the contest.
textfile = datafile[:-4] + f'-final-ranks.txt'
with open(textfile, 'w') as file:
    file.write(f'{title} final ranks\n'
               f'------------------------------------------\n')
    file.write(f'Rank: RSN:            {units:>6} gained\n')
    for i in range(len(contest_df.index)):
        rsn = contest_df.at[i, 'RSN']
        gain = contest_df.at[i, 'Gained']
        if gain <= 0:
            break
        file.write(f'{i + 1:>3})  {rsn:<12}     {gain:>12,}\n')

log_message(f'Ranking file {textfile} created successfully.', log=logfile)

# Save contest data to a separate, final file and
# Write master_df to CSV
contest_df.to_csv('final-' + datafile, index=False)
master_df.to_csv(MASTER_DF_NAME, index=False)

log_message(f'Winners selected and raffle prize drawn for contest ID {contest_id}', log=logfile)

# Write contest table to file to update any changed settings
contest_table.to_file('contest-table')

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a list of contest and raffle winners,  the list of players' final ranks, and the
# graph of the winners' progress as a Discord message via a webhook.
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

# Remove the text file with everyone's rankings and the graph of the winners' progress
# after sending them to Discord
remove(textfile)
remove(plotfile)
