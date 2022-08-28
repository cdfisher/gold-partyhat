"""Wrapper for matthew-palmer's package "osrs_highscores" which extends functionality a bit
and helps to increase ease of use.
Original package here: https://github.com/matthew-palmer/osrs_highscores/
"""

from osrs_highscores import Highscores

SKILLS = ['overall', 'attack', 'defence', 'strength', 'hitpoints', 'ranged', 'prayer', 'magic',
          'cooking', 'woodcutting', 'fletching', 'fishing', 'firemaking', 'crafting', 'smithing',
          'mining', 'herblore', 'agility', 'thieving', 'slayer', 'farming', 'runecraft', 'hunter',
          'construction']


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
    # TODO: Extend to include things other than xp/kc

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

