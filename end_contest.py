"""end_contest.py
Script to generate the final standings for an Old School Runescape
contest. Sends a message listing the winera and all players who
reached a set threshold for participation and selects winners to
receive participation prizes
Additionally, updates a master dataframe that tracks all entries on each user's highscores page.

@:arg contest_id: str 8 character code used as a contest identifier. Not yet used, but implemented
for use with a planned future feature.
@:arg title: str The name of the contest.
@:arg --datafile: str. Optional flag to set the name of the file where contest data is stored, not including a file
extension.  Defaults to title.lower.replace(' ', '-')
@:arg --logfile: str. Optional flag to set the name of the file where log messages are stored, not including a file
extension.  Defaults to (title.lower.replace(' ', '-') + '-log')
@:arg --silent, -s: bool Optional argument to disable sending of messages to Discord when running contest
scripts for the duration of the contest. Defaults to False
@:arg --quiet, -q: bool Runs script without sending messages to Discord, but does not stop other updates run for
this contest from sending messages. Defaults to False


Example call for a contest:

"python end_contest.py 'CFF965D0' 'Attack test contest'"
"""
import random
import argparse
import matplotlib.pyplot as plt
from gph_config import *
from data_updater import *
from os import remove
from ast import literal_eval
from gph_logging import log_message
from webhook_handler import WebhookHandler

# Establish and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('contest_id', type=str, help='Unique contest identifier.')
parser.add_argument('title', type=str, help='Title of the contest.')
parser.add_argument('--datafile', type=str, help='File name of where to save contest data, excluding the extension.')
parser.add_argument('--logfile', type=str, help='File name of where the logs will be saved, excluding the extension.')
parser.add_argument('-s', '--silent', help='Runs script without sending messages to Discord,'
                                           ' and persists for the whole contest.', action='store_true')
parser.add_argument('-q', '--quiet', help='Runs script without sending messages to Discord, but does not stop '
                                          'other updates run for this contest from sending messages.',
                    action='store_true')

# Assign variables from args and use defaults if no value given
args = parser.parse_args()
contest_id = args.contest_id
title = args.title
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
silent = args.silent
quiet = args.quiet

log_message(f'Running final update for contest {title}.', log=logfile)


# Get list of settings from the footer of the CSV
with open(datafile, 'rb') as f:
    # Get footer from data file
    footer = f.readlines()[-1]
    footer = footer.decode('utf-8)')

# Parse the contest settings into an array
settings = literal_eval(footer)

# Unpack settings and cast them to the correct types
contest_id = str(settings[0])
mode = str(settings[1])
target = str(settings[2])
threshold = int(settings[3])
units = str(settings[4])
group = str(settings[5])
top_n = int(settings[6])
winners = int(settings[7])
raffle_mode = str(settings[8])
raffle_winners = int(settings[9])
if not silent:
    silent = bool(settings[10])
start = str(settings[11])
end = str(settings[12])
interval = int(settings[13])
update_number = int(settings[14])

update_number += 1

# Load master dataframe from file
master_df = pd.read_csv(MASTER_DF_NAME)

# Run the contest update procedure and make copies of both dataframes
master_df, contest_df = update_entry(group, mode, target, 'end', update_number,
                                     master_df, logfile, datafile, contest_id)

msg = f'{title} winners:\n'

win_emoji = [':first_place:', ':second_place:', ':third_place:']

for i in range(winners):
    rsn = contest_df.at[i, 'RSN']
    # Handle case in which there are more winners than we have emoji
    if i < 3:
        msg += f'{win_emoji[i]}: {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'
    else:
        msg += f' {i+1}) : {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'


# TODO look into generating the text file and graph_data simultaneously
# Create graph showing the progress of the winners to send in Discord

# Collect data on the progress of the winners in a 2D list
ranked_users = []
graph_data = [ranked_users]
for i in range(winners):
    rsn = contest_df.at[i, 'RSN']
    ranked_users.append(rsn)
    player_data = []
    for j in range(update_number+1):
        row = master_df.loc[(master_df['RSN'] == rsn) & (master_df['Update number'] == j) &
                            (master_df['Update source'] == contest_id)]
        player_data.append(row.iloc[0]['overall'])
    start_value = player_data[0]
    for k in range(len(player_data)):
        player_data[k] = player_data[k] - start_value
    graph_data.append(player_data)
graph_data[0] = ranked_users

update_list = []
for i in range(update_number+1):
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
        plt.plot(update_list, graph_data[i+1], label=graph_data[0][i], marker=plot_markers[i])

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
    # TODO incorporate N_PARTICIPANTS into arguments/contest_settings
    for i in range(winners, winners+N_PARTICIPANTS):
        gained = contest_df.at[i, 'Gained']
        if gained >= threshold:
            rsn = contest_df.at[i, 'RSN']
            participants.add(rsn)
        else:
            break

    line = f'\nHere are the top {len(participants)} who have met the participation ' \
           f'threshold of {threshold} {units} and are in the running for a participation ' \
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
        file.write(f'{i+1:>3})  {rsn:<12}     {gain:>12}\n')

log_message(f'Ranking file {textfile} created successfully.', log=logfile)

# Save contest data to a separate, final file and
# Write master_df to CSV
contest_df.to_csv('final-' + datafile, index=False)
master_df.to_csv(MASTER_DF_NAME, index=False)

log_message('Winners selected and raffle prize drawn.', log=logfile)

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a list of contest and raffle winners,  the list of players' final ranks, and the
# graph of the winners' progress as a Discord message via a webhook.
if not (silent | quiet):
    wh = WebhookHandler()

    # Using with resolves an issue where the files sent to Discord using add_file() could not be removed
    with open(plotfile, 'rb') as pf:
        wh.add_file(pf, plotfile)
        wh.send_file(msg, filename=textfile)

# Remove the text file with everyone's rankings and the graph of the winners' progress
# after sending them to Discord
remove(textfile)
remove(plotfile)
