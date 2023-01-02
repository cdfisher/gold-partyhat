"""update_master_dataframe.py

Script to update master_dataframe.csv for use with weekly and monthly
top skilling and bossing contests.

@:arg source_id: str, used by the calling cron job/bash script to note which updates
to the master dataframe are relevant for the purposes of this script.
@:arg group: str The name of the text file listing group members to track, excluding
the file extension.
@:arg --update_number: int, used to note how many times the source has called for an update to be
run on the master dataframe.
"""

import os
import argparse
from data_updater import *
from gph_config import LOG_NAME
from gph_logging import log_message

parser = argparse.ArgumentParser()
parser.add_argument('source_id', type=str, help='Source calling update to master dataframe.')
parser.add_argument('group', type=str, help='Name of the text file where group members are '
                                            'listed, excluding the file extension.')
parser.add_argument('--update_number', '-u', nargs='?', type=int, default=0,
                    help='Number of times source has called an update. Default is 0.')

args = parser.parse_args()
source_id = args.source_id
group = args.group
update_number = args.update_number

log_message(f'Updating master dataframe from source {source_id}', log=LOG_NAME)

# Load master_df if it exists as a file, otherwise start with an empty df as master_df.
if os.path.exists(MASTER_DF_NAME):
    master_df = pd.read_csv(MASTER_DF_NAME)
else:
    master_df = pd.DataFrame(columns=master_colnames)

with open(group + '.txt') as file:
    users = file.readlines()
    users = [line.rstrip() for line in users]
    for rsn in users:
        # Fetch Highscores object for user 'rsn'
        try:
            usr = hs.get_user(rsn)

        # If user is not found on the highscores, log this and continue
        except ValueError:
            log_message(f'User {rsn} not found on highscores', log=LOG_NAME)
            continue

        # Append a row for user in master dataframe
        hs_entries = hs.get_all_entries(usr)
        now = datetime.now()
        timestamp = now.strftime('[%d %b %Y - %H:%M:%S]')
        entry_array = [timestamp, update_number, source_id, rsn] + hs_entries
        master_df.loc[len(
            master_df)] = entry_array

    master_df.to_csv(MASTER_DF_NAME, index=False)

log_message(f'Master dataframe successfully updated from source {source_id}', log=LOG_NAME)
