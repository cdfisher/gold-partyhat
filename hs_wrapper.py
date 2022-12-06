"""Wrapper for matthew-palmer's package "osrs_highscores" which extends functionality a bit
and helps to increase ease of use.
Original package here: https://github.com/matthew-palmer/osrs_highscores/
Currently uses a forked version to resolve issues which can be found here:
https://github.com/cdfisher/osrs_highscores/
"""

from osrs_highscores import Highscores
from datetime import *

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

    if skill == 'overall':
        return int(user.overall.xp)
    elif skill == 'attack':
        return int(user.attack.xp)
    elif skill == 'defence':
        return int(user.defence.xp)
    elif skill == 'strength':
        return int(user.strength.xp)
    elif skill == 'hitpoints':
        return int(user.hitpoints.xp)
    elif skill == 'ranged':
        return int(user.ranged.xp)
    elif skill == 'prayer':
        return int(user.prayer.xp)
    elif skill == 'magic':
        return int(user.magic.xp)
    elif skill == 'cooking':
        return int(user.cooking.xp)
    elif skill == 'woodcutting':
        return int(user.woodcutting.xp)
    elif skill == 'fletching':
        return int(user.fletching.xp)
    elif skill == 'fishing':
        return int(user.fishing.xp)
    elif skill == 'firemaking':
        return int(user.firemaking.xp)
    elif skill == 'crafting':
        return int(user.crafting.xp)
    elif skill == 'smithing':
        return int(user.smithing.xp)
    elif skill == 'mining':
        return int(user.mining.xp)
    elif skill == 'herblore':
        return int(user.herblore.xp)
    elif skill == 'agility':
        return int(user.agility.xp)
    elif skill == 'thieving':
        return int(user.thieving.xp)
    elif skill == 'slayer':
        return int(user.slayer.xp)
    elif skill == 'farming':
        return int(user.farming.xp)
    elif skill == 'runecraft':
        return int(user.runecraft.xp)
    elif skill == 'hunter':
        return int(user.hunter.xp)
    elif skill == 'construction':
        return int(user.construction.xp)
    else:
        print(skill)
        return 'Skill not recognized.\n'


def query_skill_level(user, skill):
    """ Queries XP listed on user's highscores page.
    :param user: User object for player (as returned by get_user())
    :param skill: String specifying the skill to query (Typically set as SKILL
    in gph_config.py)
    :return: int of player's XP in given skill.
    """

    if skill == 'overall':
        return int(user.overall.level)
    elif skill == 'attack':
        return int(user.attack.level)
    elif skill == 'defence':
        return int(user.defence.level)
    elif skill == 'strength':
        return int(user.strength.level)
    elif skill == 'hitpoints':
        return int(user.hitpoints.level)
    elif skill == 'ranged':
        return int(user.ranged.level)
    elif skill == 'prayer':
        return int(user.prayer.level)
    elif skill == 'magic':
        return int(user.magic.level)
    elif skill == 'cooking':
        return int(user.cooking.level)
    elif skill == 'woodcutting':
        return int(user.woodcutting.level)
    elif skill == 'fletching':
        return int(user.fletching.level)
    elif skill == 'fishing':
        return int(user.fishing.level)
    elif skill == 'firemaking':
        return int(user.firemaking.level)
    elif skill == 'crafting':
        return int(user.crafting.level)
    elif skill == 'smithing':
        return int(user.smithing.level)
    elif skill == 'mining':
        return int(user.mining.level)
    elif skill == 'herblore':
        return int(user.herblore.level)
    elif skill == 'agility':
        return int(user.agility.level)
    elif skill == 'thieving':
        return int(user.thieving.level)
    elif skill == 'slayer':
        return int(user.slayer.level)
    elif skill == 'farming':
        return int(user.farming.level)
    elif skill == 'runecraft':
        return int(user.runecraft.level)
    elif skill == 'hunter':
        return int(user.hunter.level)
    elif skill == 'construction':
        return int(user.construction.level)
    else:
        print(skill)
        return 'Skill not recognized.\n'


def query_activity_score(user, activity):
    """ Queries activity scores listed on user's highscores page.

        :param user: User object for player (as returned by get_user())
        :param activity: String specifying the activity to query (valid values
        are listed in ACTIVITIES)
        :return: int of player's score in given activity.
        """
    if activity == 'league_points':
        return int(user.league_points.score)
    elif activity == 'bounty_hunter_hunter':
        return int(user.bounty_hunter_hunter.score)
    elif activity == 'bounty_hunter_rogue':
        return int(user.bounty_hunter_rogue.score)
    elif activity == 'clue_scrolls_all':
        return int(user.clue_scrolls_all.score)
    elif activity == 'clue_scrolls_beginner':
        return int(user.clue_scrolls_beginner.score)
    elif activity == 'clue_scrolls_easy':
        return int(user.clue_scrolls_easy.score)
    elif activity == 'clue_scrolls_medium':
        return int(user.clue_scrolls_medium.score)
    elif activity == 'clue_scrolls_hard':
        return int(user.clue_scrolls_hard.score)
    elif activity == 'clue_scrolls_elite':
        return int(user.clue_scrolls_elite.score)
    elif activity == 'clue_scrolls_master':
        return int(user.clue_scrolls_master.score)
    elif activity == 'lms_rank':
        return int(user.lms_rank.score)
    elif activity == 'pvp_arena_rank':
        return int(user.pvp_arena_rank.score)
    elif activity == 'soul_wars_zeal':
        return int(user.soul_wars_zeal.score)
    elif activity == 'rifts_closed':
        return int(user.rifts_closed.score)
    else:
        print(activity)
        return 'Activity not recognized.\n'


def query_boss_kc(user, boss):
    """ Queries KC listed on user's highscores page.

    :param user: User object for player (as returned by get_user())
    :param boss: String specifying the boss to query (Typically set as BOSS
    in gph_config.py)
    :return: int of player's KC for given boss.
    """

    if boss == 'abyssal_sire':
        return int(user.abyssal_sire.kills)
    elif boss == 'alchemical_hydra':
        return int(user.alchemical_hydra.kills)
    elif boss == 'barrows_chests':
        return int(user.barrows_chests.kills)
    elif boss == 'bryophyta':
        return int(user.bryophyta.kills)
    elif boss == 'callisto':
        return int(user.callisto.kills)
    elif boss == 'cerberus':
        return int(user.cerberus.kills)
    elif boss == 'chambers_of_xeric':
        return int(user.chambers_of_xeric.kills)
    elif boss == 'chambers_of_xeric_challenge_mode':
        return int(user.chambers_of_xeric_challenge_mode.kills)
    elif boss == 'chaos_elemental':
        return int(user.chaos_elemental.kills)
    elif boss == 'chaos_fanatic':
        return int(user.chaos_fanatic.kills)
    elif boss == 'commander_zilyana':
        return int(user.commander_zilyana.kills)
    elif boss == 'corporeal_beast':
        return int(user.corporeal_beast.kills)
    elif boss == 'crazy_archaeologist':
        return int(user.crazy_archaeologist.kills)
    elif boss == 'dagannoth_prime':
        return int(user.dagannoth_prime.kills)
    elif boss == 'dagannoth_rex':
        return int(user.dagannoth_rex.kills)
    elif boss == 'dagannoth_supreme':
        return int(user.dagannoth_supreme.kills)
    elif boss == 'deranged_archaeologist':
        return int(user.deranged_archaeologist.kills)
    elif boss == 'general_graardor':
        return int(user.general_graardor.kills)
    elif boss == 'giant_mole':
        return int(user.giant_mole.kills)
    elif boss == 'grotesque_guardians':
        return int(user.grotesque_guardians.kills)
    elif boss == 'hespori':
        return int(user.hespori.kills)
    elif boss == 'kalphite_queen':
        return int(user.kalphite_queen.kills)
    elif boss == 'king_black_dragon':
        return int(user.king_black_dragon.kills)
    elif boss == 'kraken':
        return int(user.kraken.kills)
    elif boss == 'kree_arra':
        return int(user.kree_arra.kills)
    elif boss == 'kril_tsutsaroth':
        return int(user.kril_tsutsaroth.kills)
    elif boss == 'mimic':
        return int(user.mimic.kills)
    elif boss == 'nex':
        return int(user.nex.kills)
    elif boss == 'nightmare':
        return int(user.nightmare.kills)
    elif boss == 'phosanis_nightmare':
        return int(user.phosanis_nightmare.kills)
    elif boss == 'obor':
        return int(user.obor.kills)
    elif boss == 'sarachnis':
        return int(user.sarachnis.kills)
    elif boss == 'scorpia':
        return int(user.scorpia.kills)
    elif boss == 'skotizo':
        return int(user.skotizo.kills)
    elif boss == 'tempoross':
        return int(user.tempoross.kills)
    elif boss == 'the_gauntlet':
        return int(user.the_gauntlet.kills)
    elif boss == 'the_corrupted_gauntlet':
        return int(user.the_corrupted_gauntlet.kills)
    elif boss == 'theatre_of_blood':
        return int(user.theatre_of_blood.kills)
    elif boss == 'theatre_of_blood_hard_mode':
        return int(user.theatre_of_blood_hard_mode.kills)
    elif boss == 'thermonuclear_smoke_devil':
        return int(user.thermonuclear_smoke_devil.kills)
    elif boss == 'tombs_of_amascut':
        return int(user.tombs_of_amascut.kills)
    elif boss == 'tombs_of_amascut_expert_mode':
        return int(user.tombs_of_amascut_expert_mode.kills)
    elif boss == 'tzkal_zuk':
        return int(user.tzkal_zuk.kills)
    elif boss == 'tztok_jad':
        return int(user.tztok_jad.kills)
    elif boss == 'venenatis':
        return int(user.venenatis.kills)
    elif boss == 'vet_ion':
        return int(user.vet_ion.kills)
    elif boss == 'vorkath':
        return int(user.vorkath.kills)
    elif boss == 'wintertodt':
        return int(user.wintertodt.kills)
    elif boss == 'zalcano':
        return int(user.zalcano.kills)
    elif boss == 'zulrah':
        return int(user.zulrah.kills)
    else:
        print(boss)
        return 'Boss not recognized.\n'


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


def get_all_entries(rsn: str, n_update: int) -> list:
    now = datetime.now()
    timestamp = now.strftime('[%d %b %Y - %H:%M:%S]')
    outlist = [timestamp, n_update, rsn]
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
