"""sample_gph_config.py
Contains constants needed by the bot.

Add values to WEBHOOK, TEST_WEBHOOK (if desired) and change BOT_NAME
and the values listed under Bot Configuration as desired.
Then rename file to 'gph_config.py' before running.
"""

# ---------------Bot info---------------
# Version number for logging purposes
GPH_VERSION = 'v0.4.1 beta'
# Bot name to include in JSON payload
BOT_NAME = 'Gold Partyhat'

# ---------Discord integration----------
# Used to configure the bot's Discord integration
# Toggle between test and primary Discord connections
TEST_MODE = 0
# Live server webhook
WEBHOOK = ''
# Test server webhook
TEST_WEBHOOK = ''

# ----------Bot Configuration-----------
# Constants for use by the gold-partyhat bot.
# Parameters are adjustable since things get changed up a bit from
# contest to contest.
# Raw file with output from the Clanmate Export Runelite plugin
# For group_setup.py (NYI)
RAW_GROUP_FILE = 'raw-group.txt'
# File from which to source group members
GROUP_FILE = 'group.txt'
# Number of top participants to print when updating scores
TOP_N = 5
# KC/XP required to be eligible for a participation prize
THRESHOLD = 500000
# Number of winners of contest that receive prizes
WINNERS = 3
# Number of players to select as winners of participation raffle
RAFFLE_WINNERS = 1
# Mode to use for drawing participation prizes {'classic', 'top_participants'}
RAFFLE_MODE = 'top_participants'
# Number of participants to include in raffle if mode = 'top_participants'
N_PARTICIPANTS = 10
# Name to print on contest start/update/end and in logs (logs NYI)
CONTEST_NAME = 'Sample Runecraft skilling contest'
# Name to use for data CSV file
FILE_NAME = 'runecraft-sample-contest'
# Skill to use for contest
SKILL = 'runecraft'
# Boss to use for bossing contests
BOSS = 'tempoross'
# File name to use for log file
LOG_NAME = 'gph-log.txt'
# File name for the master dataframe
MASTER_DF_NAME = 'master_dataframe.csv'
# Link to default bot avatar
AVATAR_URL = 'https://github.com/cdfisher/gold-partyhat/blob/master/resources/icon.png?raw=true'
