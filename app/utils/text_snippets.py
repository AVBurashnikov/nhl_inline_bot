from app.constants.teams import TEAMS


def team_icon(abbrev: str) -> str:
    return TEAMS.get(abbrev.lower(),{}).get("icon", "")


def team_common_name(abbrev: str) -> str:
    return TEAMS.get(abbrev.lower(),{}).get("common_name", "")


def team_place_name(abbrev: str) -> str:
    return TEAMS.get(abbrev.lower(),{}).get("place_name", "")