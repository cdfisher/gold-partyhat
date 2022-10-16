"""boss_update.py
Script to update the standings for a bossing-based competition and send
a message listing the top participants at the time of update.
"""
import discord_integration

from data_updater import update_kc
from gph_config import *
from gph_logging import log_message

log_message('Updating contest: {}'.format(CONTEST_NAME))

df = update_kc(FILE_NAME + '.csv', BOSS, 'update')

participants = set()

msg = CONTEST_NAME + ' Top {} (so far):\n'.format(TOP_N)

for i in range(TOP_N):
    rsn = df.at[i, 'RSN']

    line = '{}) {} KC gained: {:,}\n'.format(i+1, rsn, df.at[i, 'Gained'])
    if df.at[i, 'Gained'] >= THRESHOLD:
        participants.add(rsn)
    msg += line + '\n'

for i in range(TOP_N, len(df.index)):
    gained = df.at[i, 'Gained']
    if gained >= THRESHOLD:
        rsn = df.at[i, 'RSN']
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
    line = '\n{} have met the participation threshold for a prize so ' \
           'far!\n'.format(len(participants))

msg += line

par_srtd = sorted(participants)

for x in par_srtd:
    msg += x + '\n'

df.to_csv(FILE_NAME + '.csv', index=False)

# TODO: Append one last line with the timestamp that this was
# TODO: run to the csv file. Then we can set up the "last updated"
# TODO: functionality.

log_message('Contest successfully updated.')

discord_integration.send_message(msg)
