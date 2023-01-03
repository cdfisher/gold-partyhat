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
from data_updater import *
from gph_config import LOG_NAME
from gph_logging import log_message
from webhook_handler import WebhookHandler

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

if os.path.exists(IRON_DICT_NAME):
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
            # kc_diff_list[i] = kc_end_list[i] - kc_start_list[i]
            kc_gained_list.append(float(end_list[i] - start_list[i]))

        # From array of KC gained, calculate EHB
        # TODO add an optional argument is_iron to here so we can speed things up
        if rsn in iron_dict:
            is_ironman = iron_dict[rsn]
        else:
            is_ironman = hs.is_iron(rsn)
            iron_dict[rsn] = is_ironman
        ehb_gained = hs.calc_ehb_from_list(rsn, kc_gained_list, is_ironman=is_ironman)

        # add [RSN, delta_overall] to a DataFrame gains_df
        gains_df.loc[len(gains_df)] = [rsn, xp_gained, ehb_gained]
    # Otherwise there's an error to handle here
    else:
        log_message(f'Insufficient data available for player {rsn}.', log=LOG_NAME)
        continue

with open(IRON_DICT_NAME, 'w') as iron_file:
    iron_file.write(str(iron_dict))

# sort gains_df by delta_overall
gains_df = gains_df.sort_values(by=['XP gained'], ascending=False).reset_index(drop=True)

msg = ''
time_period_number = source_id[-4:-2]
if time_period_number[1] == '1':
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

msg += f'Top XP gained for the {ordinal_time_period} {period} of {year}\n'

# TODO Change this over to send via embeds

# Add top 3 to message
for i in range(3):
    msg += f'#{i + 1}) {gains_df.at[i, "RSN"]} XP gained: {gains_df.at[i, "XP gained"]}\n'

# sort gains_df by delta_EHB
gains_df = gains_df.sort_values(by=['EHB gained'], ascending=False).reset_index(drop=True)
# Add top 3 to message
msg += f'Top EHB gained for the {ordinal_time_period} {period} of {year}\n'

# TODO Change this over to send via embeds

# Add top 3 to message
for i in range(3):
    msg += f'#{i + 1}) {gains_df.at[i, "RSN"]} EHB gained: {gains_df.at[i, "EHB gained"]}\n'
# Send message
wh = WebhookHandler()
wh.send_message(msg)
log_message(f'Done running top_players.py for source id: {source_id}', log=LOG_NAME)
