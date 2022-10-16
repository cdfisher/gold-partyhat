"""data_updater.py
On start, loads player list from a file (currently a .txt, will be transistioning
over to a .csv), and loads the highscores entry relevant to the competition into
a pandas dataframe.

On update/end, loads from CSV and updates entries, as well as computing each
player's competition progress.
"""
import hs_wrapper as hs
import pandas as pd

from gph_config import *
from gph_logging import log_message


def update_xp(infile, skill, mode):
    """ Fetches XP values from Highscores and updates the dataframe of these values

    :param infile: File used as input. For mode='start', this expects a .txt
    with one username per line. For mode='update' and mode='end', expects a
    CSV representation of a dataframe with columns {'RSN', 'Start', 'Current,
    'Gained'}
    :param skill: Str of the skill we're checking in the contest.
    :param mode: {
                'start': Takes list of group members and creates an initial
    listing of their starting XP values, then exports the results as a CSV.
                  'update': Loads CSV of rankings to dataframe, updates current XP and
    calculates gains, then reorders by rank and returns the dataframe.
                  'end': Loads CSV of rankings to dataframe, updates current XP and
    calculates gains, then reorders by rank and returns the dataframe.}
    :return: Pandas dataframe to be exported by the calling function, potentially
    after further manipulation.
    """
    if mode == 'start':
        # Expect infile to be user list and make array of users
        # TODO: Replace this with CSV handling to be able to use files direct
        # TODO: from the Clanmate Exporter plugin.

        with open(infile) as file:
            users = file.readlines()
            users = [line.rstrip() for line in users]

        # Create dataframe with each user's RSN and starting XP
        df = pd.DataFrame(columns=['RSN', 'Start', 'Current', 'Gained'])
        for rsn in users:
            try:
                usr = hs.get_user(rsn)

            # In the case that there is no highscores listing for user, skip them.
            except ValueError:
                log_message('User {} not found on highscores.'.format(rsn))
                continue
            score = int(hs.query_skill_xp(usr, skill))

            # For players found in highscores that aren't on hs for skill, change
            # score from -1 to 0
            if score < 0:
                score = 0

            # Add user record to dataframe
            df.loc[len(df.index)] = [rsn, score, score, 0]

        # Export dataframe to file
        df.to_csv(FILE_NAME + '.csv', index=False)

        return df

    elif mode == 'update':
        # Expect infile to be CSV of rankings and load into df

        # TODO: Once 'last updated' functionality is added, add parameter skipfooter=1
        df = pd.read_csv(infile)

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If we get a ValueError for a user already in df, they've probably
                # changed their name.
                log_message('User {} not found! Potential name change detected!'.format(rsn))
                continue

            prev = int(df.at[i, 'Start'])
            score = hs.query_skill_xp(usr, skill)

            # Preserves manual edits to starting values in the case that starting
            # score was too low to be listed on hiscores.

            # TODO Adjust this value to work for XP hiscores
            if score < 2411:
                score = prev
            gained = int(score) - int(prev)

            # Update DataFrame row with these new values
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

        # reorder rows by value in 'Gained' and update indices
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return df

    elif mode == 'end':
        # Expect infile to be CSV of rankings and load into df

        # TODO: Once 'last updated' functionality is added, add parameter skipfooter=1
        df = pd.read_csv(infile)

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If we get a ValueError for a user already in df, they've probably
                # changed their name.
                log_message('User {} not found! Potential name change detected!'.format(rsn))
                continue

            prev = int(df.at[i, 'Start'])
            score = hs.query_skill_xp(usr, skill)

            # Preserves manual edits to starting values in the case that starting
            # score was too low to be listed on highscores.

            # TODO Adjust this value to work for XP highscores
            if score < 2411:
                score = prev
            gained = int(score) - int(prev)

            # Update DataFrame row with these new values
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

        # reorder rows by value in 'Gained' and update indices
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return df

    else:
        # mode not recognized or unsupported
        log_message('Mode {} not recognized or not supported!'.format(mode))


def update_kc(infile, boss, mode):
    """ Fetches KC values from Highscores and updates the dataframe of these values

    :param infile: File used as input. For mode='start', this expects a .txt
    with one username per line. For mode='update' and mode='end', expects a
    CSV representation of a dataframe with columns {'RSN', 'Start', 'Current,
    'Gained'}
    :param boss: Str of the boss we're checking in the contest.
    :param mode: {'start': Takes list of group members and creates an initial
    listing of their starting KC values, then exports the results as a CSV.
                  'update': Loads CSV of rankings to dataframe, updates current KC and
    calculates gains, then reorders by rank and returns the dataframe.
                  'end': Loads CSV of rankings to dataframe, updates current KC and
    calculates gains, then reorders by rank and returns the dataframe.}
                    }
    :return: Pandas dataframe to be exported by the calling function, potentially
    after further manipulation.
    """
    if mode == 'start':
        # Expect infile to be user list and make array of users
        # TODO: Replace this with CSV handling to be able to use files direct
        # TODO: from the Clanmate Exporter plugin.

        with open(infile) as file:
            users = file.readlines()
            users = [line.rstrip() for line in users]

        # Create dataframe with each user's RSN and starting KC
        df = pd.DataFrame(columns=['RSN', 'Start', 'Current', 'Gained'])
        for rsn in users:
            try:
                usr = hs.get_user(rsn)

            # In the case that there is no highscores listing for user, skip them.
            except ValueError:
                log_message('User {} not found on highscores.'.format(rsn))
                continue
            score = hs.query_boss_kc(usr, boss)

            # For players found in highscores that aren't on hs for boss, change
            # score from -1 to 0
            if score < 0:
                score = 0

            # Add user record to dataframe
            df.loc[len(df.index)] = [rsn, score, score, 0]

        # Export dataframe to file
        df.to_csv(FILE_NAME + '.csv', index=False)

        return df

    elif mode == 'update':
        # Expect infile to be CSV of rankings and load into df

        # TODO: Once 'last updated' functionality is added, add parameter skipfooter=1
        df = pd.read_csv(infile)

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If we get a ValueError for a user already in df, they've probably
                # changed their name.
                log_message('User {} not found! Potential name change detected!'.format(rsn))
                continue

            prev = int(df.at[i, 'Start'])
            score = hs.query_boss_kc(usr, boss)

            # Preserves manual edits to starting values in the case that starting
            # score was too low to be listed on hiscores.
            if score < 50:
                score = prev
            gained = int(score) - int(prev)

            # Update DataFrame row with these new values
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

        # reorder rows by value in 'Gained' and update indices
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return df

    elif mode == 'end':
        # Expect infile to be CSV of rankings and load into df

        # TODO: Once 'last updated' functionality is added, add parameter skipfooter=1
        df = pd.read_csv(infile)

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                # If we get a ValueError for a user already in df, they've probably
                # changed their name.
                log_message('User {} not found! Potential name change detected!'.format(rsn))
                continue

            prev = int(df.at[i, 'Start'])
            score = hs.query_boss_kc(usr, boss)

            # Preserves manual edits to starting values in the case that starting
            # score was too low to be listed on highscores.
            if score < 50:
                score = prev
            gained = int(score) - int(prev)

            # Update DataFrame row with these new values
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

        # reorder rows by value in 'Gained' and update indices
        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return df

    else:
        # mode not recognized or unsupported
        log_message('Mode {} not recognized or not supported!'.format(mode))
