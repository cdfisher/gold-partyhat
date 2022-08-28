"""skill_start.py
Script to start tracking group members for an XP-based competition.
"""
import discord_integration

from data_updater import update_xp
from gph_config import *

# TODO change back to group.txt
df = update_xp(GROUP_FILE, SKILL, 'start')

msg = 'Running gold-partyhat ' + GPH_VERSION + '\n'

msg += CONTEST_NAME + ' has begun. Get ' + str(THRESHOLD) + ' XP to be ' \
                            'eligible to win the participation raffle!\n'

n_users = len(df.index)
msg += str(n_users) + ' members are being tracked!\n'

discord_integration.send_message(msg)
