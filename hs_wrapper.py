"""Wrapper for matthew-palmer's package "osrs_highscores" which extends functionality a bit
and helps to increase ease of use.
Original package here: https://github.com/matthew-palmer/osrs_highscores/
"""

from osrs_highscores import Highscores

SKILLS = ['overall', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic',
          'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing',
          'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecraft', 'hunter',
          'construction']

# TODO: Add ACTIVITIES

# TODO: Add entries for Tempoross and Phosani's Nightmare when they are added to the osrs-highscores
# TODO: package and remove single quotes from kree'arra, k'ril_tsutsaroth and vet'ion when they
# TODO: are updated in that package

# TODO: Bosses appearing from Vorkath onward in this list are not currently supported
BOSSES = ['abyssal_sire', 'alchemical_hydra', 'barrows_chests', 'bryophyta', 'callisto', 'cerberus',
          'chambers_of_xeric', 'chambers_of_xeric_challenge_mode', 'chaos_elemental', 'chaos_fanatic',
          'commander_zilyana', 'corporeal_beast', 'crazy_archaeologist', 'dagannoth_prime',
          'dagannoth_rex', 'dagannoth_supreme', 'deranged_archaeologist', 'general_graardor',
          'giant_mole', 'grotesque_guardians', 'hespori', 'kalphite_queen', 'king_black_dragon',
          'kraken', 'kree\'arra', 'k\'ril_tsutsaroth', 'mimic', 'nex', 'nightmare', 'phosanis_nightmare',
          'obor', 'sarachnis', 'scorpia', 'skotizo', 'the_gauntlet', 'the_corrupted_gauntlet',
          'theatre_of_blood', 'theatre_of_blood_hard_mode', 'thermonuclear_smoke_devil',
          'tombs_of_amascut', 'tombs_of_amascut_expert_mode', 'tzkal_zuk', 'tztok_jad', 'venenatis',
          'vet\'ion', 'vorkath', 'wintertodt', 'zalcano', 'zulrah']


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
        return 'Skill not recognized'

# TODO: Implement query_activity_score(user, activity)



# TODO: Implement error handling for unsupported bosses
def query_boss_kc(user, boss):
    """ Queries KC listed on user's highscores page.

    :param user: User object for player (as returned by get_user())
    :param boss: String specifying the boss to query (Typically set as BOSS
    in gph_config.py)
    :return: int of player's KC for given boss.
    """

    # TODO: osrs-highscores currently returns incorrect values for bosses
    # TODO: so this will have to be replaced with a version that returns
    # TODO: as many correct values as possible until that is fixed.

    # TODO: Does not include the following bosses as the osrs-highscores
    # TODO: package does not yet include them: Phosani's Nightmare, Tempoross

    if boss == 'abyssal_sire':
        return int(user.barrows_chests.kills)
    elif boss == 'alchemical_hydra':
        return int(user.bryophyta.kills)
    elif boss == 'barrows_chests':
        return int(user.callisto.kills)
    elif boss == 'bryophyta':
        return int(user.cerberus.kills)
    elif boss == 'callisto':
        return int(user.chambers_of_xeric.kills)
    elif boss == 'cerberus':
        return int(user.chambers_of_xeric_challenge_mode.kills)
    elif boss == 'chambers_of_xeric':
        return int(user.chaos_elemental.kills)
    elif boss == 'chambers_of_xeric_challenge_mode':
        return int(user.chaos_fanatic.kills)
    elif boss == 'chaos_elemental':
        return int(user.commander_zilyana.kills)
    elif boss == 'chaos_fanatic':
        return int(user.corporeal_beast.kills)
    elif boss == 'commander_zilyana':
        return int(user.crazy_archaeologist.kills)
    elif boss == 'corporeal_beast':
        return int(user.dagannoth_prime.kills)
    elif boss == 'crazy_archaeologist':
        return int(user.dagannoth_rex.kills)
    elif boss == 'dagannoth_prime':
        return int(user.dagannoth_supreme.kills)
    elif boss == 'dagannoth_rex':
        return int(user.deranged_archaeologist.kills)
    elif boss == 'dagannoth_supreme':
        return int(user.general_graardor.kills)
    elif boss == 'deranged_archaeologist':
        return int(user.giant_mole.kills)
    elif boss == 'general_graardor':
        return int(user.grotesque_guardians.kills)
    elif boss == 'giant_mole':
        return int(user.hespori.kills)
    elif boss == 'grotesque_guardians':
        return int(user.kalphite_queen.kills)
    elif boss == 'hespori':
        return int(user.king_black_dragon.kills)
    elif boss == 'kalphite_queen':
        return int(user.kraken.kills)
    elif boss == 'king_black_dragon':
        # TODO: Attribute name is non-compliant with Python naming rules
        # TODO: and so I'm using 'kreeara' as a placeholder. Non-functional
        # TODO: at this time.
        return int(user.kreeara.kills)
    elif boss == 'kraken':
        # TODO: Attribute name is non-compliant with Python naming rules
        # TODO: and so I'm using 'kril_tsutsaroth' as a placeholder. Non-functional
        # TODO: at this time.
        return int(user.kraken.kills)
    elif boss == 'kree\'ara':
        return int(user.kraken.kills)
    elif boss == 'k\'rul_tsutsaroth':
        return int(user.nex.kills)
    elif boss == 'mimic':
        return int(user.nightmare.kills)
    elif boss == 'nex':
        return int(user.obor.kills)
    elif boss == 'nightmare':
        return int(user.sarachnis.kills)
    elif boss == 'phosanis_nightmare':
        # TODO: not currently included in osrs-hiscores but
        # TODO: since there's an offset we can access it
        return int(user.scorpia.kills)
    elif boss == 'obor':
        return int(user.skotizo.kills)
    elif boss == 'sarachnis':
        return int(user.the_gauntlet.kills)
    elif boss == 'scorpia':
        return int(user.the_corrupted_gauntlet.kills)
    elif boss == 'skotizo':
        return int(user.theatre_of_blood.kills)
    elif boss == 'tempoross':
        # TODO: not currently included in osrs-hiscores but
        # TODO: since there's an offset we can access it
        return int(user.theatre_of_blood_hard_mode.kills)
    elif boss == 'the_gauntlet':
        return int(user.thermonuclear_smoke_devil.kills)
    elif boss == 'the_corrupted_gauntlet':
        return int(user.tombs_of_amascut.kills)
    elif boss == 'theatre_of_blood':
        return int(user.tombs_of_amascut_expert_mode.kills)
    elif boss == 'theatre_of_blood_hard_mode':
        return int(user.tzkal_zuk.kills)
    elif boss == 'thermonuclear_smoke_devil':
        return int(user.tztok_jad.kills)
    elif boss == 'tombs_of_amascut':
        return int(user.venenatis.kills)
    elif boss == 'tombs_of_amascut_expert_mode':
        # TODO: Attribute name is non-compliant with Python naming rules
        # TODO: and so I'm using 'vetion' as a placeholder. Non-functional
        # TODO: at this time.
        return int(user.tombs_of_amascut_expert_mode.kills)
    elif boss == 'tzkal_zuk':
        return int(user.vorkath.kills)
    elif boss == 'tztok_jad':
        return int(user.wintertodt.kills)
    elif boss == 'venenatis':
        return int(user.zalcano.kills)
    elif boss == 'vet\'ion':
        return int(user.zulrah.kills)
    elif boss == 'vorkath':
        # TODO: Bosses from here onward do not work due to an
        # TODO: issue with the source library currently
        return int(user.vorkath.kills)
    elif boss == 'wintertodt':
        return int(user.wintertodt.kills)
    elif boss == 'zalcano':
        return int(user.zalcano.kills)
    elif boss == 'zulrah':
        return int(user.zulrah.kills)
    else:
        print(boss)
        return 'Boss not recognized'


def fetch_all_skills(rsn, user):
    """Prints list of user's XP in all skills to console.
    Not currently used but may be updated to a more useful form in the
    future.

    :param rsn: String of player's OSRS username.
    :param user: User object for player (as returned by get_user())
    :return: No return value, prints to console
    """
    print(rsn + "'s XP:")
    for i in range(len(SKILLS)):
        print(SKILLS[i] + ' : ' + query_skill_xp(user, SKILLS[i]))


def get_mole_kc(user):
    """DEPRECIATED -- Left as reference for now.
    Used to get the tracker functional for the Giant Mole Boss of the Week
    event.
    Queries of boss KC need significant updating, this was just a workaround.

    :param user: User object for player (as returned by get_user())
    :return: int of player's KC for a given boss.
    """
    # Why is this checking Kalphite Queen KC rather than Giant Mole, you ask?
    # Well the offsets for bosses in the osrs_highscores package are outdated!
    # So when we queried giant_mole, on our end, we were actually getting the
    # entries for dagannoth_supreme. To fix this, we need to add an offset of 3
    # entries in the boss table!
    kc = int(user.kalphite_queen.kills)
    if kc < 0:
        kc = 0
    return kc

