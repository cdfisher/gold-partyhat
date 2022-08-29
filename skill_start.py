"""skill_start.py
Script to start tracking group members for an XP-based competition.
"""
import discord_integration

from data_updater import update_xp
from gph_config import *
from gph_logging import log_message

msg = 'Running gold-partyhat ' + GPH_VERSION + '\n'
log_message('Starting competition for skill: ' + SKILL +
            ' running Gold Partyhat ' + GPH_VERSION)

df = update_xp(GROUP_FILE, SKILL, 'start')

msg += '{} has begun. Get {:,} XP to be eligible for the ' \
       'participation raffle!\n'.format(CONTEST_NAME, THRESHOLD)

n_users = len(df.index)
msg += str(n_users) + ' members are being tracked!\n'
log_message('Competition started successfully. Tracking ' + str(n_users) +
            ' members')

discord_integration.send_message(msg)
