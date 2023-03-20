"""top_players.py
Script to calculate the top players for XP gained and efficient hours bossed (EHB)
in a given time period.

@:arg source_id: str, used by the calling cron job/bash script to note which updates
to the master dataframe are relevant for the purposes of this script.
@:arg period: str used to mark the time period the script is looking at,
for example 'week', 'month', etc. Just used for text purposes and does not affect the
calculation
"""

import os
import argparse
from dotenv import load_dotenv
from data_updater import *
from gph_utils.gph_config import LOG_NAME
from gph_utils.gph_logging import log_message
from webhook_handler import WebhookHandler

load_dotenv()

if TEST_MODE:
    update_webhook = os.getenv('TEST_WEBHOOK')
else:
    update_webhook = os.getenv('TOP_PLAYERS_WEBHOOK')

parser = argparse.ArgumentParser()
parser.add_argument('source_id', type=str, help='Contest identifier.')
parser.add_argument('period', type=str, help='Period of time to look at')

args = parser.parse_args()
source_id = args.source_id
period = args.period

log_message(f'Running top_players.py for end of {period}, source id {source_id}', log=LOG_NAME)

# Load master_df if it exists as a file, otherwise raise an exception.
if os.path.exists(MASTER_DF_NAME):
    master_df = pd.read_csv(MASTER_DF_NAME)
else:
    log_message(f'Master dataframe file {MASTER_DF_NAME} not found by top_players.py!', log=LOG_NAME)
    raise FileNotFoundError(f'Master dataframe file \'{MASTER_DF_NAME}\' not found!')

# If a file caching iron/main status exists, open it and read as a dict. Otherwise create it as an empty file.
if os.path.exists(IRON_DICT_NAME) and os.path.getsize(IRON_DICT_NAME) != 0:
    with open(IRON_DICT_NAME, 'r') as iron_file:
        iron_dict = eval(iron_file.read())
else:

    iron_file = open(IRON_DICT_NAME, 'w')
    iron_file.close()
    iron_dict = dict()


# Get maximum value of update_number in master_df for rows where 'Update source' is source_id
time_df = master_df.loc[(master_df['Update source'] == source_id)].reset_index(drop=True)
last_update = time_df.max()['Update number']

gains_df = pd.DataFrame(columns=['RSN', 'XP gained', 'EHB gained'])

rsn_array = time_df['RSN'].unique()
# for each value of rsn in rows with last_update, source_id:
for rsn in rsn_array:
    # if rows exist with (rsn, update=0) and (rsn, last_update) pairs:
    if (((time_df['RSN'] == rsn) & (time_df['Update number'] == 0)).any() &
            ((time_df['RSN'] == rsn) & (time_df['Update number'] == last_update)).any()):
        # get overall xp gain
        start_xp_idx = time_df[(time_df['RSN'] == rsn) & (time_df['Update number'] == 0)].first_valid_index()
        end_xp_idx = time_df[(time_df['RSN'] == rsn) & (time_df['Update number'] == last_update)].first_valid_index()
        xp_gained = time_df.at[end_xp_idx, 'overall'] - time_df.at[start_xp_idx, 'overall']

        # Get list of boss KC at start of time period
        start_list = (time_df.iloc[start_xp_idx].loc['abyssal_sire':'zulrah']).tolist()
        # Get list of boss KC at end of time period
        end_list = (time_df.iloc[end_xp_idx].loc['abyssal_sire':'zulrah']).tolist()

        kc_gained_list = []

        # Calculate KC gained for each boss
        for i in range(len(start_list)):
            kc_gained_list.append(float(end_list[i] - start_list[i]))

        # From array of KC gained, calculate EHB

        # Check cached list of iron/main status to speed things up immensely.
        if rsn in iron_dict:
            is_ironman = iron_dict[rsn]
        else:
            is_ironman = hs.is_iron(rsn)
            iron_dict[rsn] = is_ironman
        ehb_gained = hs.calc_ehb_from_list(rsn, kc_gained_list, is_ironman=is_ironman)

        # add [RSN, delta_overall, delta_ehb] to a DataFrame gains_df
        gains_df.loc[len(gains_df)] = [rsn, xp_gained, ehb_gained]
    # Otherwise there's an error to handle here
    else:
        log_message(f'Insufficient data available for player {rsn}.', log=LOG_NAME)
        continue

with open(IRON_DICT_NAME, 'w') as iron_file:
    iron_file.write(str(iron_dict))

# sort gains dataframe by XP gained
gains_df = gains_df.sort_values(by=['XP gained'], ascending=False).reset_index(drop=True)

time_period_number = source_id[-4:-2]
if time_period_number[1] == '1':
    if time_period_number[0] == '1':
        suffix = 'th'
    else:
        suffix = 'st'
elif time_period_number[1] == '2':
    suffix = 'nd'
elif time_period_number[1] == '3':
    suffix = 'rd'
else:
    suffix = 'th'
if str(time_period_number)[0] == '0':
    time_period_number = str(time_period_number)[1:]
ordinal_time_period = time_period_number + suffix

year = '20' + source_id[-2:]

top_by_xp = []
# Get top 3 players and their XP gained
for i in range(3):
    top_by_xp.append([gains_df.at[i, "RSN"], gains_df.at[i, "XP gained"]])

# sort gains dataframe by EHB gained
gains_df = gains_df.sort_values(by=['EHB gained'], ascending=False).reset_index(drop=True)

top_by_ehb = []
# Get top 3 players and their EHB gained
for i in range(3):
    top_by_ehb.append([gains_df.at[i, "RSN"], gains_df.at[i, "EHB gained"]])


months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September,' 'October', 'November', 'December']
if period == 'month' and ((int(time_period_number) >= 1) and (int(time_period_number) < 13)):
    time_period = months[int(time_period_number) - 1]
else:
    time_period = f'the {ordinal_time_period} {period} of'

# Build embeds
embeds = [
        {
            "title": f"Top XP gained for {time_period} {year}",
            "fields": [
                {
                    "name": f":first_place:: {top_by_xp[0][0]}",
                    "value": f"{top_by_xp[0][1]:,} XP gained",
                    "inline": "false"
                },
                {
                    "name": f":second_place:: {top_by_xp[1][0]}",
                    "value": f"{top_by_xp[1][1]:,} XP gained",
                    "inline": "false"
                },
                {
                    "name": f":third_place:: {top_by_xp[2][0]}",
                    "value": f"{top_by_xp[2][1]:,} XP gained",
                    "inline": "false"
                }
            ],
            "color": 6655
        },
        {
            "title": f"Top EHB gained for {time_period} {year}",
            "color": 16714507,
            "fields": [
                {
                    "name": f":first_place:: {top_by_ehb[0][0]}",
                    "value": f"{top_by_ehb[0][1]} efficient hours bossed",
                    "inline": "false"
                },
                {
                    "name": f":second_place:: {top_by_ehb[1][0]}",
                    "value": f"{top_by_ehb[1][1]} efficient hours bossed",
                    "inline": "false"
                },
                {
                    "name": f":third_place:: {top_by_ehb[2][0]}",
                    "value": f"{top_by_ehb[2][1]} efficient hours bossed",
                    "inline": "false"
                }
            ]
        }
    ]

# Send message
wh = WebhookHandler(hook_url=update_webhook)
wh.send_embed('', embeds=embeds)
log_message(f'Done running top_players.py for source id: {source_id}', log=LOG_NAME)
