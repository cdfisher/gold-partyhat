"""Wrapper for matthew-palmer's package "osrs_highscores" which extends functionality a bit
and helps to increase ease of use.
Original package here: https://github.com/matthew-palmer/osrs_highscores/
Currently uses a forked version to resolve issues which can be found here:
https://github.com/cdfisher/osrs_highscores/
"""

from osrs_highscores import Highscores

"""List of all valid skills listed on highscores
"""
SKILLS = ['overall', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic',
          'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing',
          'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecraft', 'hunter',
          'construction']

"""Formatted list of skills, index matched with SKILLS
"""
FORMATTED_SKILLS = ['Overall', 'Attack', 'Defence', 'Strength', 'Hitpoints', 'Ranged', 'Prayer', 'Magic',
                    'Cooking', 'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing',
                    'Mining', 'Herblore', 'Agility', 'Thieving', 'Slayer', 'Farming', 'Runecraft', 'Hunter',
                    'Construction']

"""List of all valid activities listed on highscores
"""
ACTIVITIES = ['league_points', 'bounty_hunter_hunter', 'bounty_hunter_rogue', 'clue_scrolls_all',
              'clue_scrolls_beginner', 'clue_scrolls_easy', 'clue_scrolls_medium', 'clue_scrolls_hard',
              'clue_scrolls_elite', 'clue_scrolls_master', 'lms_rank', 'pvp_arena_rank',
              'soul_wars_zeal', 'rifts_closed']

"""Formatted list of activities, index matched with ACTIVITIES
"""
FORMATTED_ACTIVITIES = ['League Points', 'Bounty Hunter (Hunter)', 'Bounty Hunter (Rogue)', 'Clue Scrolls (All)',
                        'Clue Scrolls (Beginner)', 'Clue Scrolls (Easy)', 'Clue Scrolls (Medium)',
                        'Clue Scrolls (Hard)', 'Clue Scrolls (Elite)', 'Clue Scrolls (Master)', 'LMS Rank',
                        'PvP Arena Rank', 'Soul Wars Zeal', 'Rifts Closed']

"""List of all valid bosses listed on highscores
"""
BOSSES = ['abyssal_sire', 'alchemical_hydra', 'barrows_chests', 'bryophyta', 'callisto', 'cerberus',
          'chambers_of_xeric', 'chambers_of_xeric_challenge_mode', 'chaos_elemental', 'chaos_fanatic',
          'commander_zilyana', 'corporeal_beast', 'crazy_archaeologist', 'dagannoth_prime',
          'dagannoth_rex', 'dagannoth_supreme', 'deranged_archaeologist', 'general_graardor',
          'giant_mole', 'grotesque_guardians', 'hespori', 'kalphite_queen', 'king_black_dragon',
          'kraken', 'kree_arra', 'kril_tsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanis_nightmare',
          'obor', 'sarachnis', 'scorpia', 'skotizo', 'tempoross', 'the_gauntlet', 'the_corrupted_gauntlet',
          'theatre_of_blood', 'theatre_of_blood_hard_mode', 'thermonuclear_smoke_devil',
          'tombs_of_amascut', 'tombs_of_amascut_expert_mode', 'tzkal_zuk', 'tztok_jad', 'venenatis',
          'vet_ion', 'vorkath', 'wintertodt', 'zalcano', 'zulrah']

"""Formatted list of bosses, index matched with BOSSES
"""
FORMATTED_BOSSES = ['Abyssal Sire', 'Alchemical Hydra', 'Barrows Chests', 'Bryophyta', 'Callisto', 'Cerberus',
                    'Chambers of Xeric', 'Chambers of Xeric Challenge Mode', 'Chaos Elemental', 'Chaos Fanatic',
                    'Commander Zilyana', 'Corporeal Beast', 'Crazy Archaeologist', 'Dagannoth Prime',
                    'Dagannoth Rex', 'Dagannoth Supreme', 'Deranged Archaeologist', 'General Graardor',
                    'Giant Mole', 'Grotesque Guardians', 'Hespori', 'Kalphite Queen', 'King Black Dragon',
                    'Kraken', 'Kree\'arra', 'K\'ril Tsutsaroth', 'Mimic', 'Nex', 'Nightmare', 'Phosani\'s Nightmare',
                    'Obor', 'Sarachnis', 'Scorpia', 'Skotizo', 'Tempoross', 'The Gauntlet', 'The Corrupted Gauntlet',
                    'Theatre of Blood', 'Theatre of Blood Hard Mode', 'Thermonuclear Smoke Devil',
                    'Tombs of Amascut', 'Tombs of Amascut Expert Mode', 'TzKal-Zuk', 'TzTok-Jad', 'Venenatis',
                    'Vet\'ion', 'Vorkath', 'Wintertodt', 'Zalcano', 'Zulrah']


def get_user(rsn):
    """Fetches a given user's highscores entries.

    :param rsn: String of player's OSRS username.
    :return: Highscores object for given user.
    """
    return Highscores(rsn)


def query_skill_xp(user, skill):
    """ Queries XP listed on user's highscores page.
    :param user: User object for player (as returned by get_user())
    :param skill: String specifying the skill to query (Typically set as SKILL
    in gph_config.py)
    :return: int of player's XP in given skill.
    """
    try:
        skill_entry = user.__getattribute__(skill)
    except AttributeError:
        print(f'Skill {skill} not found!\n')
        raise
    else:
        return int(skill_entry.xp)


def query_skill_level(user, skill):
    """ Queries XP listed on user's highscores page.
    :param user: User object for player (as returned by get_user())
    :param skill: String specifying the skill to query (Typically set as SKILL
    in gph_config.py)
    :return: int of player's XP in given skill.
    """
    try:
        skill_entry = user.__getattribute__(skill)
    except AttributeError:
        print(f'Skill {skill} not found!\n')
        raise
    else:
        return int(skill_entry.level)


def query_activity_score(user, activity):
    """ Queries activity scores listed on user's highscores page.

        :param user: User object for player (as returned by get_user())
        :param activity: String specifying the activity to query (valid values
        are listed in ACTIVITIES)
        :return: int of player's score in given activity.
        """
    try:
        activity_entry = user.__getattribute__(activity)
    except AttributeError:
        print(f'Activity {activity} not found!\n')
        raise
    else:
        return int(activity_entry.score)


def query_boss_kc(user, boss):
    """ Queries KC listed on user's highscores page.

    :param user: User object for player (as returned by get_user())
    :param boss: String specifying the boss to query (Typically set as BOSS
    in gph_config.py)
    :return: int of player's KC for given boss.
    """
    try:
        boss_entry = user.__getattribute__(boss)
    except AttributeError:
        print(f'Boss {boss} not found!\n')
        raise
    else:
        return int(boss_entry.kills)

# TODO rewrite all three 'fetch_all' functions to return lists and build the
# TODO strings they currently return in the calling scripts so that they
# TODO are more broadly useful. Requires changes to the Clockwork Penguin bot.


def fetch_all_skills(rsn, user):
    """Writes list of user's XP in all skills to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s XP: \n'.format(rsn)
    for i in range(len(SKILLS)):
        msg += '{} : {} XP\n'.format(SKILLS[i], query_skill_xp(user, SKILLS[i]))
    return msg


def fetch_all_activities(rsn, user):
    """Writes list of user's score in all activities to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s activity scores: \n'.format(rsn)
    for i in range(len(ACTIVITIES)):
        msg += '{} : {} \n'.format(ACTIVITIES[i], query_activity_score(user, ACTIVITIES[i]))
    return msg


def fetch_all_bosses(rsn, user):
    """Writes list of user's KC for all bosses to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s boss KC: \n'.format(rsn)
    for i in range(len(BOSSES)):
        msg += '{} : {} KC\n'.format(BOSSES[i], query_boss_kc(user, BOSSES[i]))
    return msg


def get_all_entries(rsn: str) -> list:
    """Fetches a list of all OSRS highscores entries for user rsn

    :param rsn: String of player's OSRS username.
    :return: list of all entries on a player's OSRS highscores page, with entries that are not
    found being set to zero
    """
    outlist = []
    usr = get_user(rsn)
    for i in range(len(SKILLS)):
        xp = query_skill_xp(usr, SKILLS[i])
        if xp <= 0:
            xp = 0
        outlist.append(xp)
    for i in range(len(ACTIVITIES)):
        score = query_activity_score(usr, ACTIVITIES[i])
        if score <= 0:
            score = 0
        outlist.append(score)
    for i in range(len(BOSSES)):
        kc = query_boss_kc(usr, BOSSES[i])
        if kc <= 0:
            kc = 0
        outlist.append(kc)

    return outlist
