"""skill_end.py
Script to generate the final standings for an XP-based competition. Sends
a message listing the winners, all players that reached a pre-set
threshold (set as THRESHOLD in gph_config.py), and randomly selects
winners for participation prizes.
"""
import discord_integration
import random

from data_updater import update_xp
from gph_config import *
from gph_logging import log_message

log_message('Running final update for contest: {}'.format(CONTEST_NAME))

df = update_xp(FILE_NAME + '.csv', SKILL, 'end')

df.to_csv('final-' + FILE_NAME + '.csv', index=False)

msg = '{} winners:\n'.format(CONTEST_NAME)

win_emoji = [':first_place:', ':second_place:', ':third_place:']

for i in range(WINNERS):
    rsn = df.at[i, 'RSN']
    line = '{}: {} XP gained: {:,}\n'.format(win_emoji[i], rsn, df.at[i, 'Gained'])

participants = set()

for i in range(WINNERS, len(df.index)):
    gained = df.at[i, 'Gained']
    if gained >= THRESHOLD:
        rsn = df.at[i, 'RSN']
        participants.add(rsn)
    else:
        break

line = '\n{} have met the participation threshold for a prize so ' \
           'far!\n'.format(len(participants))

msg += line

# TODO: Remove after testing. Pads participants list in the case there
# TODO: are fewer players on the participants list than winners of
# TODO: the participation raffle. Will be handled more cleanly.
if len(participants) < RAFFLE_WINNERS:
    participants.add('A')
    participants.add('B')
    participants.add('C')
    participants.add('D')
    participants.add('E')

par_srtd = sorted(participants)

for x in par_srtd:
    msg += x + '\n'

msg += '\nThe winners of the participation prizes are:\n'

winners = sorted(random.sample(participants, RAFFLE_WINNERS))

for w in winners:
    msg += w + '\n'

log_message('Winners selected and raffle prize drawn.')

discord_integration.send_message(msg)
