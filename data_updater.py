"""data_updater.py
On start, loads player list from a file (currently a .txt, will be transistioning
over to a .csv), and loads the highscores entry relevant to the competition into
a Pandas DataFrame. Appends a row for that user to a master dataframe that persists
between contests.

On update/end, loads from CSV and updates entries, as well as computing each
player's competition progress. Additionally, appends a row to the master dataframe.
"""
import hs_wrapper as hs
import pandas as pd

from datetime import *
from gph_utils.gph_config import *
from gph_utils.gph_logging import log_message


"""Used for updating the master_dataframe"""
master_colnames = ['Timestamp', 'Update number', 'Update source', 'RSN'] + hs.SKILLS + hs.ACTIVITIES + hs.BOSSES


def update_entry(infile: str, game_mode: str, target: str, update_mode: str,
                 update_number: int, master_dataframe: pd.DataFrame, logfile: str,
                 contest_datafile: str, source_id: str):
    """Creates and updates both contest and master dataframes

    :param infile: str: filename of a .txt file listing the players to track with the contest.
    Only used when update_mode == 'start'. Otherwise can just be passed an empty string.
    :param game_mode: str in {'skill', 'boss', 'activity'} denoting the type of target to
    track.
    :param target: str in hs.SKILLS, hs.BOSSES or hs.ACTIVITIES denoting the specific target
    to track.
    :param update_mode: str in {'start', 'update', 'end'} denoting which contest script is
    calling the update, as this affects behavior.
    :param update_number: int denoting the number of times the contest has been updated. Used
    to mark rows in master_dataframe (multiple rows with the same RSN value may have the same
    value in the 'Update Number' column. This is okay since it's used relative to a contest
    and not in any absolute context.
    :param master_dataframe: pd.DataFrame containing a master record of each player in infile's
    HS pages over time.
    :param logfile: str denoting where to write log messages.
    :param contest_datafile: str denoting the .csv file where the contest_dataframe is saved.
    :param source_id: str identifying the source calling the master dataframe to be updated. In most cases,
    this will be a contest_id
    :return: pd.DataFrame df: the contest_dataframe
    """
    if update_mode == 'start':
        # Expects infile to be a list of users. Parses that list and copies to an array
        with open(infile) as file:
            users = file.readlines()
            users = [line.rstrip() for line in users]

            # Create contest_dataframe with each user's RSN and starting scores
            df = pd.DataFrame(columns=['RSN', 'Start', 'Current', 'Gained'])
            for rsn in users:
                # Fetch Highscores object for user 'rsn'
                try:
                    usr = hs.get_user(rsn)

                # If user is not found on the highscores, log this and continue
                except ValueError:
                    log_message(f'User {rsn} not found on highscores', logfile)
                    continue

                # Queries user's highscores entry for target
                if game_mode == 'skill':
                    score = int(hs.query_skill_xp(usr, target))
                elif game_mode == 'activity':
                    score = int(hs.query_activity_score(usr, target))
                elif game_mode == 'boss':
                    score = int(hs.query_boss_kc(usr, target))
                else:
                    log_message(f'Target {target} not recognized', logfile)

                # If a player is listed on the highscores but does not have an entry for
                # target, set their score from -1 to 0
                if score < 0:
                    score = 0

                # Add user record to contest dataframe
                df.loc[len(df.index)] = [rsn, score, score, 0]

                # Append a row for user in master dataframe
                hs_entries = hs.get_all_entries(usr)
                now = datetime.now()
                timestamp = now.strftime('[%d %b %Y - %H:%M:%S]')
                entry_array = [timestamp, update_number, source_id, rsn] + hs_entries
                try:
                    master_dataframe.loc[len(
                        master_dataframe)] = entry_array
                except ValueError as err:
                    log_message(f'Data error {err} occurred while adding row for {rsn} to master dataframe.')
                    continue

            # Export both dataframes to .csv files
            master_dataframe.to_csv(MASTER_DF_NAME, index=False)
            df.to_csv(contest_datafile, index=False)

            # return a pd.DataFrame for contest dataframe so the contest start script
            # can then utilise that information.
            return df

    elif update_mode == 'update':
        # Read contest_dataframe from file
        df = pd.read_csv(contest_datafile, skipfooter=1, engine='python')

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If a RSN that's already in the contest dataframe isn't found, they likely
                # changes their name, so flag this in the log so their new name can be
                # edited into the datafile
                log_message(f'User {rsn} not found! Potential name change detected!',
                            log=logfile)
                continue

            # This line is mostly just present to prevent an IDE warning since
            # if score is not defined below, the update can't run
            score = 0

            # Queries user's highscores entry for target
            prev = int(df.at[i, 'Start'])
            if game_mode == 'skill':
                score = int(hs.query_skill_xp(usr, target))
            elif game_mode == 'activity':
                score = int(hs.query_activity_score(usr, target))
            elif game_mode == 'boss':
                score = int(hs.query_boss_kc(usr, target))
            else:
                log_message(f'Target {target} not recognized', log=logfile)

            # Preserve any manual edits made to the contest data in the case that a user's
            # score was too low to appear on the highscores
            if score < prev:
                score = prev

            # Calculate user's progress and update their row in the contest dataframe
            gained = int(score) - int(prev)
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

            # Append a row for user in master dataframe with their updated highscores entries
            hs_entries = hs.get_all_entries(usr)
            now = datetime.now()
            timestamp = now.strftime('[%d %b %Y - %H:%M:%S]')
            entry_array = [timestamp, update_number, source_id, rsn] + hs_entries
            master_dataframe.loc[len(
                master_dataframe)] = entry_array

        # Rank the rows in contest dataframe and reset indices.
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        # Pass pd.DataFrames for master dataframe and contest dataframe back to the contest
        # update script.
        return master_dataframe, df

    elif update_mode == 'end':
        # Read contest dataframe from file
        df = pd.read_csv(contest_datafile, skipfooter=1, engine='python')

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If a RSN that's already in the contest dataframe isn't found, they likely
                # changes their name, so flag this in the log so their new name can be
                # edited into the datafile
                log_message(f'User {rsn} not found! Potential name change detected!',
                            log=logfile)
                continue

            # This line is mostly just present to prevent an IDE warning since
            # if score is not defined below, the update can't run
            score = 0

            # Queries user's highscores entry for target
            prev = int(df.at[i, 'Start'])
            if game_mode == 'skill':
                score = int(hs.query_skill_xp(usr, target))
            elif game_mode == 'activity':
                score = int(hs.query_activity_score(usr, target))
            elif game_mode == 'boss':
                score = int(hs.query_boss_kc(usr, target))
            else:
                log_message(f'Target {target} not recognized', log=logfile)

            # Preserve any manual edits made to the contest data in the case that a user's
            # score was too low to appear on the highscores
            if score < 50:
                score = prev

            # Calculate user's progress and update their row in the contest dataframe
            gained = int(score) - int(prev)
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

            # Append a row for user in master dataframe with their updated highscores entries
            hs_entries = hs.get_all_entries(usr)
            now = datetime.now()
            timestamp = now.strftime('[%d %b %Y - %H:%M:%S]')
            entry_array = [timestamp, update_number, source_id, rsn] + hs_entries
            master_dataframe.loc[len(
                master_dataframe)] = entry_array

        # Rank the rows in contest dataframe and reset indices.
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        # Pass pd.DataFrames for master dataframe and contest dataframe back to the contest
        # update script.
        return master_dataframe, df

    else:
        log_message(f'Update mode "{update_mode}" not recognized', log=logfile)
