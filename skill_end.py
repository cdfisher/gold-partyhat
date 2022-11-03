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

log_message('Running final update for contest: ' + CONTEST_NAME)

df = update_xp(FILE_NAME + '.csv', SKILL, 'end')

df.to_csv('final-' + FILE_NAME + '.csv', index=False)

msg = CONTEST_NAME + ' winners:\n'

win_emoji = [':first_place:', ':second_place:', ':third_place:']

for i in range(WINNERS):
    rsn = df.at[i, 'RSN']
    # Handle case in which there are more winners than we have emoji
    if i < 3:
        msg += '{}: {} XP gained: {:,}\n'.format(win_emoji[i], rsn, df.at[i, 'Gained'])
    else:
        msg += ' {}) : {} XP gained: {:,}\n'.format(i+1, rsn, df.at[i, 'Gained'])

if RAFFLE_MODE == 'classic':
    participants = set()

    for i in range(WINNERS, len(df.index)):
        gained = df.at[i, 'Gained']
        if gained >= THRESHOLD:
            rsn = df.at[i, 'RSN']
            participants.add(rsn)
        else:
            break

    line = '\n{} have met the participation threshold for a prize!\n'.format(str(len(participants)))

    msg += line

    par_srtd = sorted(list(participants))

    for x in par_srtd:
        msg += x + '\n'

    if len(par_srtd) <= RAFFLE_WINNERS:
        # If there are fewer participants than prize packages, everyone that reached the threshold gets one
        msg += 'There were enough prizes allotted for everyone listed above as a participant to get one!\n'
    else:
        # Otherwise draw prizes as normal
        msg += '\nThe winners of the participation prizes are:\n'

        winners = sorted(random.sample(par_srtd, RAFFLE_WINNERS))

        for w in winners:
            msg += w + '\n'

elif RAFFLE_MODE == 'top_participants':
    participants = set()

    for i in range(WINNERS, WINNERS+N_PARTICIPANTS):
        gained = df.at[i, 'Gained']
        if gained >= THRESHOLD:
            rsn = df.at[i, 'RSN']
            participants.add(rsn)
        else:
            break

    line = '\n{} have met the participation threshold of {} XP and are in the running ' \
           'for a participation prize!\n'.format(str(len(participants)), THRESHOLD)

    msg += line

    par_srtd = sorted(list(participants))

    for x in par_srtd:
        msg += x + '\n'

    if len(par_srtd) <= RAFFLE_WINNERS:
        # If there are fewer participants than prize packages, everyone that reached the threshold gets one
        msg += 'There were enough prizes allotted for everyone listed above as a participant to get one!\n'
    else:
        # Otherwise draw prizes as normal
        msg += '\nThe winners of the participation prizes are:\n'

        winners = sorted(random.sample(par_srtd, RAFFLE_WINNERS))

        for w in winners:
            msg += w + '\n'

else:
    # Mode not supported
    log_message('Mode \'{}\' not supported.\n'.format(RAFFLE_MODE))

log_message('Winners selected and raffle prize drawn.')

discord_integration.send_message(msg)
