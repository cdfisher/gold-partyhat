"""sample_gph_constants.py
Contains constants needed by the bot.

Add values to WEBHOOK, TEST_WEBHOOK (if desired) and change BOT_NAME
and the values listed under Bot Configuration as desired.
Then rename file to 'gph_constants.py' before running.
"""

# ---------------Bot info---------------
# Version number for logging purposes (NYI)
GPH_VERSION = 'v0.1 alpha'
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
# Name to print on contest start/update/end and in logs (logs NYI)
CONTEST_NAME = 'Sample Runecraft skilling contest'
FILE_NAME = 'runecraft-sample-contest'
# Skill to use for contest
SKILL = 'runecraft'