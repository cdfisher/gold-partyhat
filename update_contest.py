"""update_contest.py
Script to update group members' progress in a skill-, boss-, or activity-based
competition.
Additionally, updates a master dataframe that tracks all entries on each user's highscores page.

@:arg contest_id: str 8 character code used as a contest identifier. Not yet used, but implemented
for use with a planned future feature.
@:arg title: str The name of the contest.
@:arg --datafile: str. Optional flag to set the name of the file where contest data is stored, not including a file
extension.  Defaults to title.lower.replace(' ', '-')
@:arg --logfile: str. Optional flag to set the name of the file where log messages are stored, not including a file
extension.  Defaults to (title.lower.replace(' ', '-') + '-log')

Example call for a contest:

"python update_contest.py 'CFF965D0' 'Attack test contest'"
"""
import argparse
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

log_message(f'Updating contest {title}.', log=logfile)

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
raffle_winners = int(settings[9])
silent = bool(settings[10])
start = str(settings[11])
end = str(settings[12])
interval = int(settings[13])
update_number = int(settings[14])

update_number += 1

# Load master dataframe from file
master_df = pd.read_csv(MASTER_DF_NAME)

# Run the contest update procedure and make copies of both dataframes
master_df, contest_df = update_entry(group, mode, target, 'update', update_number, master_df, logfile, datafile)

participants = set()

msg = f'{title} top {top_n} (so far)\n'

# TODO Implement top_n progress graphing

# Make a list of the top_n participants
for i in range(top_n):
    rsn = contest_df.at[i, 'RSN']

    line = f'{i+1}) {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'
    if contest_df.at[i, 'Gained'] >= threshold:
        participants.add(rsn)
    msg += line + '\n'

# Make a list of all participants outside the top_n who still meet the
# threshold for participation.
for i in range(top_n, len(contest_df.index)):
    gained = contest_df.at[i, 'Gained']
    if gained >= threshold:
        rsn = contest_df.at[i, 'RSN']
        participants.add(rsn)
    else:
        break

# Make file listing the ranks of everyone who has increased
# their score since the start of the contest.
fname = datafile[:-4] + f'-update-{update_number}-gains.txt'
with open(fname, 'w') as file:
    file.write(f'{title} progress update #{update_number}\n'
               f'------------------------------------------\n')
    file.write(f'Rank: RSN:            {units:>6} gained\n')
    for i in range(len(contest_df.index)):
        rsn = contest_df.at[i, 'RSN']
        gain = contest_df.at[i, 'Gained']
        if gain <= 0:
            break
        file.write(f'{i+1:>3})  {rsn:<12}     {gain:>12}\n')

log_message(f'Progress file {fname} created successfully.', log=logfile)

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
                    update_number]
with open(datafile, 'a') as file:
    file.write(str(contest_settings))

log_message('Contest successfully updated.', log=logfile)

# If the --silent flag was used, don't send anything to Discord. Otherwise, send
# a list of the top_n and the list of players' progress as a Discord
# message via a webhook.
if not silent:
    wh = WebhookHandler()
    wh.send_file(msg, filename=fname)


# Remove the text file with everyone's progress
remove(fname)
