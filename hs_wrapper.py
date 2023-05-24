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
ACTIVITIES = ['league_points', 'bounty_hunter_hunter', 'bounty_hunter_rogue', 'bounty_hunter_legacy_hunter',
              'bounty_hunter_legacy_rogue', 'clue_scrolls_all', 'clue_scrolls_beginner', 'clue_scrolls_easy',
              'clue_scrolls_medium', 'clue_scrolls_hard', 'clue_scrolls_elite', 'clue_scrolls_master', 'lms_rank',
              'pvp_arena_rank', 'soul_wars_zeal', 'rifts_closed']

"""Formatted list of activities, index matched with ACTIVITIES
"""
FORMATTED_ACTIVITIES = ['League Points', 'Bounty Hunter (Hunter)', 'Bounty Hunter (Rogue)',
                        'Bounty Hunter (Legacy) - Hunter', 'Bounty Hunter (Legacy) - Rogue', 'Clue Scrolls (All)',
                        'Clue Scrolls (Beginner)', 'Clue Scrolls (Easy)', 'Clue Scrolls (Medium)',
                        'Clue Scrolls (Hard)', 'Clue Scrolls (Elite)', 'Clue Scrolls (Master)', 'LMS Rank',
                        'PvP Arena Rank', 'Soul Wars Zeal', 'Rifts Closed']

"""List of all valid bosses listed on highscores
"""
BOSSES = ['abyssal_sire', 'alchemical_hydra', 'artio', 'barrows_chests', 'bryophyta', 'callisto', 'calvar_ion',
          'cerberus', 'chambers_of_xeric', 'chambers_of_xeric_challenge_mode', 'chaos_elemental', 'chaos_fanatic',
          'commander_zilyana', 'corporeal_beast', 'crazy_archaeologist', 'dagannoth_prime',
          'dagannoth_rex', 'dagannoth_supreme', 'deranged_archaeologist', 'general_graardor',
          'giant_mole', 'grotesque_guardians', 'hespori', 'kalphite_queen', 'king_black_dragon',
          'kraken', 'kree_arra', 'kril_tsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanis_nightmare', 'obor',
          'phantom_muspah', 'sarachnis', 'scorpia', 'skotizo', 'spindel', 'tempoross', 'the_gauntlet',
          'the_corrupted_gauntlet', 'theatre_of_blood', 'theatre_of_blood_hard_mode', 'thermonuclear_smoke_devil',
          'tombs_of_amascut', 'tombs_of_amascut_expert_mode', 'tzkal_zuk', 'tztok_jad', 'venenatis',
          'vet_ion', 'vorkath', 'wintertodt', 'zalcano', 'zulrah']

"""Formatted list of bosses, index matched with BOSSES
"""
FORMATTED_BOSSES = ['Abyssal Sire', 'Alchemical Hydra', 'Artio', 'Barrows Chests', 'Bryophyta', 'Callisto',
                    'Calvar\'ion', 'Cerberus', 'Chambers of Xeric', 'Chambers of Xeric Challenge Mode',
                    'Chaos Elemental', 'Chaos Fanatic', 'Commander Zilyana', 'Corporeal Beast', 'Crazy Archaeologist',
                    'Dagannoth Prime', 'Dagannoth Rex', 'Dagannoth Supreme', 'Deranged Archaeologist',
                    'General Graardor', 'Giant Mole', 'Grotesque Guardians', 'Hespori', 'Kalphite Queen',
                    'King Black Dragon', 'Kraken', 'Kree\'arra', 'K\'ril Tsutsaroth', 'Mimic', 'Nex', 'Nightmare',
                    'Phosani\'s Nightmare', 'Obor', 'Phantom Muspah', 'Sarachnis', 'Scorpia', 'Skotizo', 'Spindel',
                    'Tempoross', 'The Gauntlet', 'The Corrupted Gauntlet', 'Theatre of Blood',
                    'Theatre of Blood Hard Mode', 'Thermonuclear Smoke Devil', 'Tombs of Amascut',
                    'Tombs of Amascut Expert Mode', 'TzKal-Zuk', 'TzTok-Jad', 'Venenatis', 'Vet\'ion', 'Vorkath',
                    'Wintertodt', 'Zalcano', 'Zulrah']

"""EHB_RATES:
    Dict of bosses and their respective kills per efficient bossing hour.
    EHB_RATES(boss) returns a tuple of length 2 as a key.
    key[0] is the EHB rate for main accounts, and key[1] is the rate for ironman accounts.
    A rate value of -1.0 indicates boss kills do not count toward EHB for that account type.
    Rates have been sourced from https://wiseoldman.net/rates/ehb
    """
EHB_RATES = {'abyssal_sire': (42.0, 32.0),
             'alchemical_hydra': (27.0, 26.0),
             'artio': (-1.0, -1.0),
             'barrows_chests': (-1.0, 18.0),
             'bryophyta': (-1.0, 9.0),
             'callisto': (50.0, 30.0),
             'calvar_ion': (-1.0, -1.0),
             'cerberus': (61.0, 54.0),
             'chambers_of_xeric': (3.0, 2.8),
             'chambers_of_xeric_challenge_mode': (2.2, 2.0),
             'chaos_elemental': (60.0, 48.0),
             'chaos_fanatic': (100.0, 80.0),
             'commander_zilyana': (55.0, 25.0),
             'corporeal_beast': (50.0, 6.5),
             'crazy_archaeologist': (-1.0, 75.0),
             'dagannoth_prime': (88.0, 88.0),
             'dagannoth_rex': (88.0, 88.0),
             'dagannoth_supreme': (88.0, 88.0),
             'deranged_archaeologist': (-1.0, 80.0),
             'general_graardor': (50.0, 25.0),
             'giant_mole': (100.0, 80.0),
             'grotesque_guardians': (36.0, 31.0),
             'hespori': (-1.0, 60.0),
             'kalphite_queen': (50.0, 30.0),
             'king_black_dragon': (120.0, 70.0),
             'kraken': (90.0, 82.0),
             'kree_arra': (25.0, 22.0),
             'kril_tsutsaroth': (65.0, 26.0),
             'mimic': (-1.0, 60.0),
             'nex': (12.0, 12.0),
             'nightmare': (14.0, 11.0),
             'phosanis_nightmare': (7.5, 6.5),
             'obor': (-1.0, 12.0),
             'phantom_muspah': (25.0, 25.0),
             'sarachnis': (80.0, 56.0),
             'scorpia': (130.0, 60.0),
             'skotizo': (45.0, 38.0),
             'spindel': (-1.0, -1.0),
             'tempoross': (-1.0, -1.0),
             'the_gauntlet': (10.0, 10.0),
             'the_corrupted_gauntlet': (6.5, 6.5),
             'theatre_of_blood': (3.0, 2.5),
             'theatre_of_blood_hard_mode': (3.0, 2.4),
             'thermonuclear_smoke_devil': (125.0, 80.0),
             'tombs_of_amascut': (2.5, 2.5),
             'tombs_of_amascut_expert_mode': (2.0, 2.0),
             'tzkal_zuk': (0.8, 0.8),
             'tztok_jad': (2.0, 2.0),
             'venenatis': (50.0, 35.0),
             'vet_ion': (30.0, 23.0),
             'vorkath': (32.0, 32.0),
             'wintertodt': (-1.0, -1.0),
             'zalcano': (-1.0, -1.0),
             'zulrah': (35.0, 32.0)}


def get_ehb(boss: str, kc: int, mode: str) -> float:
    """ Returns EHB value for a given boss.
    :param boss: string from BOSSES in hs_wrapper.py denoting all tracked bosses
    :param kc: int, player's kill count for :parameter boss
    :param mode: str with value 'main' or 'iron', denoting which set of rates to use
    :return: float representing player's efficient hours spent at :parameter boss
    """
    if mode == 'main':
        return kc / EHB_RATES[boss][0]
    elif mode == 'iron':
        return kc / EHB_RATES[boss][1]
    else:
        print(f'{mode} not recognized\n')


def calc_ehb_from_list(rsn: str, boss_kc_list: list, is_ironman=None) -> float:
    """Calculates a player's efficient hours bossed and returns it
    as a float.
    @:param rsn: str of the user's RuneScape username
    @:param boss_kc_list: list representing the player's KC for each boss

    @:return float correspoding to the player's efficient hours bossed.
    """
    if is_ironman is None:
        try:
            iron = is_iron(rsn)
        except ValueError:
            print(f'User {rsn} not found!')
            return -1.0
    else:
        iron = is_ironman

    if iron:
        mode = 'iron'
    else:
        mode = 'main'

    total_ehb = 0.0
    for i in range(len(BOSSES)):
        kc = boss_kc_list[i]
        ehb = get_ehb(BOSSES[i], kc, mode)
        if (kc > 0) & (ehb > 0):
            total_ehb += ehb

    total_ehb = round(total_ehb, 2)
    return total_ehb


def is_iron(rsn: str) -> bool:
    """Checks if a given player is an Ironman account.
    :param rsn: str value of a player's OSRS username
    :return: boolean, True if user is an ironman, False if not
    @:raises ValueError if player is not found on highscores
    """
    # If we find a user on the Ironman highscores, we know they're an ironman.
    # Otherwise, we check to make sure the user exists on the main highscore board
    # This isn't a great solution but it's really the only way to check an account's status
    try:
        user = Highscores(rsn, target='ironman')
        return True
    except ValueError:
        try:
            user = Highscores(rsn)
            return False
        except ValueError:
            raise ValueError


def get_user(rsn: str) -> Highscores:
    """Fetches a given user's highscores entries.

    :param rsn: String of player's OSRS username.
    :return: Highscores object for given user.
    """
    return Highscores(rsn)


def get_target_type(target: str) -> str:
    """Returns whether a given contest target is a skill, activity, or boss.

    :param target: String representation of target to query
    :return: String representing type.
    """
    if target in SKILLS:
        return 'skill'
    elif target in ACTIVITIES:
        return 'activity'
    elif target in BOSSES:
        return 'boss'
    else:
        return f'Target {target} not recognized.'


# TODO Wrap all of these query methods into one query_entry(user, target, attr='default') method
def query_skill_xp(user: Highscores, skill: str) -> int:
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


def query_skill_level(user: Highscores, skill: str) -> int:
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


def query_activity_score(user: Highscores, activity: str) -> int:
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


def query_boss_kc(user: Highscores, boss: str) -> int:
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


def fetch_all_skills(rsn: str, user: Highscores) -> str:
    """Writes list of user's XP in all skills to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s XP: \n'.format(rsn)
    for i in range(len(SKILLS)):
        msg += '{} : {} XP\n'.format(SKILLS[i], query_skill_xp(user, SKILLS[i]))
    return msg


def fetch_all_activities(rsn: str, user: Highscores) -> str:
    """Writes list of user's score in all activities to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s activity scores: \n'.format(rsn)
    for i in range(len(ACTIVITIES)):
        msg += '{} : {} \n'.format(ACTIVITIES[i], query_activity_score(user, ACTIVITIES[i]))
    return msg


def fetch_all_bosses(rsn: str, user: Highscores) -> str:
    """Writes list of user's KC for all bosses to string and returns.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: String msg
    """

    msg = '{}\'s boss KC: \n'.format(rsn)
    for i in range(len(BOSSES)):
        msg += '{} : {} KC\n'.format(BOSSES[i], query_boss_kc(user, BOSSES[i]))
    return msg


def get_all_entries(usr: Highscores) -> list:
    """Fetches a list of all OSRS highscores entries for user rsn

    :param usr: Highscores object pointing to a given user
    :return: list of all entries on a player's OSRS highscores page, with entries that are not
    found being set to zero
    """
    outlist = []
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
