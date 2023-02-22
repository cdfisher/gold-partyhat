"""gph_config.py
Settings to be used by the Gold Partyhat bot
"""

# ---------------Bot info---------------
# Version number for logging purposes
GPH_VERSION = 'v0.6 beta'
# Bot name to include in JSON payload
BOT_NAME = 'Gold Partyhat'

# ---------Discord integration----------
# Used to configure the bot's Discord integration
# Toggle between test and primary Discord connections
TEST_MODE = 1

# ----------Bot Configuration-----------
# Constants for use by the gold-partyhat bot.
# Parameters are adjustable since things get changed up a bit from
# contest to contest. Many of these are included as default values and can
# be overridden by optional command line arguments for setup_contest.py,
# start_contest.py, update_contest.py, and end_contest.py
# Number of top participants to print when updating scores
TOP_N = 5
# KC/XP required to be eligible for a participation prize
THRESHOLD = 50
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
AVATAR_URL = 'https://github.com/cdfisher/gold-partyhat/blob/master/resources/icon.png?raw=true'
