import random
import argparse
from gph_config import *
from data_updater import *
from ast import literal_eval
from gph_logging import log_message
from webhook_handler import WebhookHandler

parser = argparse.ArgumentParser()
parser.add_argument('contest_id', type=str, help='Unique contest identifier.')
parser.add_argument('title', type=str, help='Title of the contest.')
parser.add_argument('--datafile', type=str, help='File name of where to save contest data, excluding the extension.')
parser.add_argument('--logfile', type=str, help='File name of where the logs will be saved, excluding the extension.')

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

log_message(f'Running final update for contest {title}.', log=logfile)


# Get list of settings from the footer of the CSV
with open(datafile, 'rb') as f:
    # Get footer from our data file
    footer = f.readlines()[-1]
    footer = footer.decode('utf-8)')

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

master_df = pd.read_csv(MASTER_DF_NAME)

master_df, contest_df = update_entry(group, mode, target, 'end', update_number,
                                     master_df, logfile, datafile)

msg = f'{title} winners:\n'

win_emoji = [':first_place:', ':second_place:', ':third_place:']

for i in range(winners):
    rsn = contest_df.at[i, 'RSN']
    # Handle case in which there are more winners than we have emoji
    if i < 3:
        msg += f'{win_emoji[i]}: {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'
    else:
        msg += f' {i+1}) : {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'

# TODO Right around here is where I need to implement the progress graphing

# TODO implement the file of everyone with nonzero gain

if raffle_mode == 'classic':
    participants = set()

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

        msg += 'There were enough prizes allotted for everyone listed above as a participant to get one!\n'
    else:
        msg += '\nThe winners of the participation prizes are:\n'

        r_winners = sorted(random.sample(par_srtd, raffle_winners))

        for w in r_winners:
            msg += w + '\n'

elif raffle_mode == 'top_participants':
    participants = set()

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

contest_df.to_csv('final-' + datafile, index=False)
master_df.to_csv(MASTER_DF_NAME, index=False)

log_message('Winners selected and raffle prize drawn.', log=logfile)

if not silent:
    wh = WebhookHandler()
    # TODO change this to wh.send_file(msg, filename) once progress file
    # TODO and progress graph are implemented
    wh.send_message(msg)
