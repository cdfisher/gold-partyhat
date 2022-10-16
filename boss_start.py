"""boss_start.py
Script to start tracking group members for a bossing-based competition.
"""
import discord_integration

from data_updater import update_kc
from gph_config import *
from gph_logging import log_message

msg = 'Running {} {}\n'.format(BOT_NAME, GPH_VERSION)
log_message('Starting competition for boss: {} running Gold '
            'Partyhat {}'.format(BOSS, GPH_VERSION))
log_message('Competition name: {}'.format(CONTEST_NAME))

df = update_kc(GROUP_FILE, BOSS, 'start')

msg += '{} has begun. Get {:,} KC to be eligible for the ' \
       'participation raffle!\n'.format(CONTEST_NAME, THRESHOLD)

n_users = len(df.index)
msg += '{} members are being tracked!\n'.format(n_users)
log_message('Competition started successfully. Tracking {}'
            ' members'.format(n_users))

discord_integration.send_message(msg)
