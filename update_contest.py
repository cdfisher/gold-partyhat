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

log_message(f'Updating contest {title}.', log=logfile)


# Get list of settings from the footer of the CSV
with open(datafile, 'rb') as f:
    # Get footer from our data file
    footer = f.readlines()[-1]
    footer = footer.decode('utf-8')

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

master_df, contest_df = update_entry(group, mode, target, 'update', update_number, master_df, logfile, datafile)

participants = set()

msg = f'{title} top {top_n} (so far)\n'

# TODO Right around here is where I need to implement the progress graphing

# TODO implement the file of everyone with nonzero gain
for i in range(top_n):
    rsn = contest_df.at[i, 'RSN']

    line = f'{i+1}) {rsn} {units} gained: {contest_df.at[i, "Gained"]:,}\n'
    if contest_df.at[i, 'Gained'] >= threshold:
        participants.add(rsn)
    msg += line + '\n'

for i in range(top_n, len(contest_df.index)):
    gained = contest_df.at[i, 'Gained']
    if gained >= threshold:
        rsn = contest_df.at[i, 'RSN']
        participants.add(rsn)
    else:
        break

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

contest_df.to_csv(datafile, index=False)
master_df.to_csv(MASTER_DF_NAME, index=False)

contest_settings = [contest_id, mode, target, threshold, units, group, top_n, winners,
                    raffle_mode, raffle_winners, silent, start, end, interval,
                    update_number]
with open(datafile, 'a') as file:
    file.write(str(contest_settings))

log_message('Contest successfully updated.', log=logfile)

if not silent:
    wh = WebhookHandler()
    # TODO change this to wh.send_file(msg, filename) once progress file
    # TODO and progress graph are implemented
    wh.send_message(msg)
