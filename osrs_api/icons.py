import re

from . import const


SKILL_ICON_BASE_URL = "https://www.runescape.com/img/rsp777/hiscores/skill_icon_{slug}1.gif"
GAME_ICON_BASE_URL = "https://www.runescape.com/img/rsp777/game_icon_{slug}.png"


_SKILL_SLUG_OVERRIDES = {
    "runecrafting": "runecraft",
}


def _normalize_name(name):
    return re.sub(r"[^a-z0-9]", "", name.casefold())


_CATEGORY_BY_NAME = {}

for _skill_name in const.SKILLS:
    _CATEGORY_BY_NAME[_normalize_name(_skill_name)] = "skill"

for _activity_name in const.MINIGAMES:
    _CATEGORY_BY_NAME[_normalize_name(_activity_name)] = "activity"

for _boss_name in const.BOSSES:
    _CATEGORY_BY_NAME[_normalize_name(_boss_name)] = "boss"


_ALIASES = {
    "bountyhunter": "Bounty Hunter - Hunter",
    "bountyhunterrogue": "Bounty Hunter - Rogue",
    "bountyhunterlegacyhunter": "Bounty Hunter (Legacy) - Hunter",
    "bountyhunterlegacyrogue": "Bounty Hunter (Legacy) - Rogue",
    "lms": "LMS - Rank",
    "pvparena": "PvP Arena - Rank",
    "barrows": "Barrows Chests",
    "gauntlet": "The Gauntlet",
    "corruptedgauntlet": "The Corrupted Gauntlet",
    "hueycoatl": "The Hueycoatl",
    "leviathan": "The Leviathan",
    "whisperer": "The Whisperer",
}


def get_icon_url(name):
    normalized_name = _normalize_name(name)

    if not normalized_name:
        raise ValueError("Icon name must contain at least one letter or number.")

    resolved_name = _ALIASES.get(normalized_name, name)
    resolved_key = _normalize_name(resolved_name)
    category = _CATEGORY_BY_NAME.get(resolved_key)

    if category is None:
        raise ValueError("Unknown skill, activity, or boss: %s" % name)

    if category == "skill":
        skill_slug = _SKILL_SLUG_OVERRIDES.get(resolved_key, resolved_key)
        return SKILL_ICON_BASE_URL.format(slug=skill_slug)

    return GAME_ICON_BASE_URL.format(slug=resolved_key)