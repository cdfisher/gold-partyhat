"""update_contest.py
Script to update group members' progress in a skill-, boss-, or activity-based
competition.
Additionally, updates a master dataframe that tracks all entries on each user's highscores page.

@:arg contest_id: str 8 character code used as a contest identifier. Not yet used, but implemented
for use with a planned future feature.
@:arg title: str The name of the contest.
@:arg --raffle_winners. int Updates the number of participation prizes available if different from what was
given at contest start.
@:arg --datafile: str. Optional flag to set the name of the file where contest data is stored, not including a file
extension.  Defaults to title.lower.replace(' ', '-')
@:arg --logfile: str. Optional flag to set the name of the file where log messages are stored, not including a file
extension.  Defaults to (title.lower.replace(' ', '-') + '-log')
@:arg --silent, -s: bool Optional argument to disable sending of messages to Discord when running contest
scripts for the duration of the contest. Defaults to False
@:arg --quiet, -q: bool Runs script without sending messages to Discord, but does not stop other updates run for
this contest from sending messages. Defaults to False


Example call for a contest:

"python update_contest.py 'CFF965D0' 'Attack test contest'"
"""
import argparse
import matplotlib.pyplot as plt
from data_updater import *
from os import remove
from time import sleep
from ast import literal_eval
from gph_logging import log_message
from webhook_handler import WebhookHandler

# Establish and parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('contest_id', type=str, help='Unique contest identifier.')
parser.add_argument('title', type=str, help='Title of the contest.')
parser.add_argument('--raffle_winners', type=int, help='Number of participation prizes available.')
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
raffle_winners = args.raffle_winners
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

log_message(f'Updating contest {title}, contest ID: {contest_id}.', log=logfile)

# Get list of settings from the footer of the CSV
with open(datafile, 'rb') as f:
    # Get footer from data file
    footer = f.readlines()[-1]
    footer = footer.decode('utf-8')

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
if raffle_winners is None:
    raffle_winners = int(settings[9])
if not silent:
    silent = bool(settings[10])
start = str(settings[11])
end = str(settings[12])
interval = int(settings[13])
update_number = int(settings[14])
n_participants = int(settings[15])
dynamic_prizes = bool(settings[16])

update_number += 1

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
        row = master_df.loc[(master_df['RSN'] == rsn) & (master_df['Update number'] == j) &
                            (master_df['Update source'] == contest_id)]
        player_data.append(row.iloc[0][target])
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
    plotname = f'{title} top {top_n} progress'
    plt.xticks(update_list)
    plt.xlabel('Update number')
    plt.ylabel(f'{units} gained')
    plt.title(plotname)
    plt.legend(facecolor='#36393F', labelcolor='#99AAB5')

    # Save plot to a file so it can be sent to Discord
    plotfile = plotname.replace(' ', '-') + f'-update-{update_number}.png'
    plotfile = plotfile.lower()
    plt.tight_layout()
    plt.savefig(plotfile)

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

# Create an array of contest settings to save and then append it to datafile
contest_settings = [contest_id, mode, target, threshold, units, group, top_n, winners,
                    raffle_mode, raffle_winners, silent, start, end, interval,
                    update_number, n_participants, dynamic_prizes]
with open(datafile, 'a') as file:
    file.write(str(contest_settings))

log_message(f'Contest {contest_id} successfully updated.', log=logfile)

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
        sleep(0.25)
        wh.add_file(pf, plotfile)
        wh.send_file(msg, filename=textfile)

# Remove the text file with everyone's progress and the plot image after sending them to
# Discord
remove(textfile)
remove(plotfile)
