"""sample_gph_config.py
Contains constants needed by the bot.

Add values to WEBHOOK, TEST_WEBHOOK (if desired) and change BOT_NAME
and the values listed under Bot Configuration as desired.
Then rename file to 'gph_config.py' before running.
"""

# ---------------Bot info---------------
# Version number for logging purposes
GPH_VERSION = 'v0.5 beta'
# Bot name to include in JSON payload
BOT_NAME = 'Gold Partyhat'

# ---------Discord integration----------
# Used to configure the bot's Discord integration
# Toggle between test and primary Discord connections
TEST_MODE = 0
# Live server webhook
WEBHOOK = ''
# Separate webhook for weekly/monthly top contests. Set = WEBHOOK if sending to the same channel as the regular
# contest updates.
TOP_PLAYERS_WEBHOOK = ''
# Test server webhook
TEST_WEBHOOK = ''

# ----------Bot Configuration-----------
# Constants for use by the gold-partyhat bot.
# Parameters are adjustable since things get changed up a bit from
# Number of top participants to print when updating scores
TOP_N = 5
# KC/XP required to be eligible for a participation prize
THRESHOLD = 500000
# Number of winners of contest that receive prizes
WINNERS = 3
# Number of participants to include in raffle if mode = 'top_participants'
N_PARTICIPANTS = 10
# File name to use for log file
LOG_NAME = 'gph-log.txt'
# File name for the master dataframe
MASTER_DF_NAME = 'master_dataframe.csv'
# File containing a dictionary of rsns and account type
IRON_DICT_NAME = 'ironmen_dictionary.txt'
# Link to default bot avatar
AVATAR_URL = 'https://github.com/cdfisher/gold-partyhat/blob/master/resources/icon.png?raw=true'
