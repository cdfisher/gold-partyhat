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

master_colnames = ['Timestamp', 'Update number', 'RSN', 'overall', 'attack', 'defence', 'strength', 'hitpoints',
                   'ranged', 'prayer', 'magic', 'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking',
                   'crafting', 'smithing', 'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming',
                   'runecraft',
                   'hunter', 'construction', 'league_points', 'bounty_hunter_hunter', 'bounty_hunter_rogue',
                   'clue_scrolls_all', 'clue_scrolls_beginner', 'clue_scrolls_easy', 'clue_scrolls_medium',
                   'clue_scrolls_hard', 'clue_scrolls_elite', 'clue_scrolls_master', 'lms_rank', 'pvp_arena_rank',
                   'soul_wars_zeal', 'rifts_closed', 'abyssal_sire', 'alchemical_hydra', 'barrows_chests', 'bryophyta',
                   'callisto', 'cerberus', 'chambers_of_xeric', 'chambers_of_xeric_challenge_mode', 'chaos_elemental',
                   'chaos_fanatic', 'commander_zilyana', 'corporeal_beast', 'crazy_archaeologist', 'dagannoth_prime',
                   'dagannoth_rex', 'dagannoth_supreme', 'deranged_archaeologist', 'general_graardor', 'giant_mole',
                   'grotesque_guardians', 'hespori', 'kalphite_queen', 'king_black_dragon', 'kraken', 'kree_arra',
                   'kril_tsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanis_nightmare', 'obor', 'sarachnis', 'scorpia',
                   'skotizo', 'tempoross', 'the_gauntlet', 'the_corrupted_gauntlet', 'theatre_of_blood',
                   'theatre_of_blood_hard_mode', 'thermonuclear_smoke_devil', 'tombs_of_amascut',
                   'tombs_of_amascut_expert_mode', 'tzkal_zuk', 'tztok_jad', 'venenatis', 'vet_ion', 'vorkath',
                   'wintertodt', 'zalcano', 'zulrah']


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


def update_entry(infile: str, game_mode: str, target: str, update_mode: str,
                 update_number: int, master_dataframe: pd.DataFrame, logfile: str,
                 contest_datafile: str):
    if update_mode == 'start':
        with open(infile) as file:
            users = file.readlines()
            users = [line.rstrip() for line in users]

            # create contest_dataframe with each user's RSN and starting scores
            df = pd.DataFrame(columns=['RSN', 'Start', 'Current', 'Gained'])
            for rsn in users:
                try:
                    usr = hs.get_user(rsn)

                except ValueError:
                    log_message(f'User {rsn} not found on highscores', logfile)
                    continue
                if game_mode == 'skill':
                    score = int(hs.query_skill_xp(usr, target))
                elif game_mode == 'activity':
                    score = int(hs.query_activity_score(usr, target))
                elif game_mode == 'boss':
                    score = int(hs.query_boss_kc(usr, target))
                else:
                    log_message(f'Target {target} not recognized', logfile)
                if score < 0:
                    score = 0
                df.loc[len(df.index)] = [rsn, score, score, 0]
                master_dataframe.loc[len(
                    master_dataframe)] = hs.get_all_entries(rsn, update_number)

            master_dataframe.to_csv(MASTER_DF_NAME, index=False)
            df.to_csv(contest_datafile, index=False)

            return df

    elif update_mode == 'update':
        df = pd.read_csv(contest_datafile, skipfooter=1, engine='python')

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                log_message(f'User {rsn} not found! Potential name change detected!',
                            log=logfile)
                continue

            score = 0

            prev = int(df.at[i, 'Start'])
            if game_mode == 'skill':
                score = int(hs.query_skill_xp(usr, target))
            elif game_mode == 'activity':
                score = int(hs.query_activity_score(usr, target))
            elif game_mode == 'boss':
                score = int(hs.query_boss_kc(usr, target))
            else:
                log_message(f'Target {target} not recognized', log=logfile)
            if score < 50:
                score = prev
            gained = int(score) - int(prev)
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

            master_dataframe.loc[len(
                master_dataframe)] = hs.get_all_entries(rsn, update_number)

        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return master_dataframe, df

    elif update_mode == 'end':

        df = pd.read_csv(contest_datafile, skipfooter=1, engine='python')

        for i in range(len(df.index)):
            rsn = df.at[i, 'RSN']
            try:
                usr = hs.get_user(rsn)
            except ValueError:
                log_message(f'User {rsn} not found! Potential name change detected!',
                            log=logfile)
                continue

            score = 0

            prev = int(df.at[i, 'Start'])
            if game_mode == 'skill':
                score = int(hs.query_skill_xp(usr, target))
            elif game_mode == 'activity':
                score = int(hs.query_activity_score(usr, target))
            elif game_mode == 'boss':
                score = int(hs.query_boss_kc(usr, target))
            else:
                log_message(f'Target {target} not recognized', log=logfile)
            if score < 50:
                score = prev
            gained = int(score) - int(prev)
            df.at[i, 'Current'] = score
            df.at[i, 'Gained'] = gained

            master_dataframe.loc[len(
                master_dataframe)] = hs.get_all_entries(rsn, update_number)

        df = df.sort_values(by=['Gained'], ascending=False).reset_index(drop=True)

        return master_dataframe, df

    else:
        log_message(f'Update mode "{update_mode}" not recognized', log=logfile)
