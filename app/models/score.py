from datetime import date, datetime, timedelta

from helpers.formatters import get_team_icon
from models.base import NHLAPIBaseModel
from utils.text_style import bold, underline, link, code


class NameDefault(NHLAPIBaseModel):
    default: str

    def __repr__(self):
        return bold(self.default)


class Team(NHLAPIBaseModel):
    id: int
    name: NameDefault
    abbrev: str
    score: int | None = None
    sog: int | None = None

    def __repr__(self):
        message = f"{get_team_icon(self.abbrev.lower())}{bold(self.name.__repr__())} "
        if self.score and self.sog:
            message += f"{self.score}({self.sog})"
        return message


class Game(NHLAPIBaseModel):
    id: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team
    three_min_recap: str | None = None

    def __repr__(self):
        start_time_msc = self.start_time_u_t_c + timedelta(hours=3)
        message = code(f"[{start_time_msc.date().strftime("%d.%m.%Y")} ")
        message += code(f"{start_time_msc.strftime("%H:%M")} {self.game_state}]\n")
        message += f"{self.away_team.__repr__()} - {self.home_team.__repr__()} /g_{self.id}\n"
        if self.three_min_recap:
            message += f"{link("Обзор матча", f"https://nhl.com{self.three_min_recap}")}"
        message += "\n\n"
        return message


class ScoreModel(NHLAPIBaseModel):
    current_date: date
    games: list[Game]

    def __repr__(self):
        message = f"Результаты матчей\n\n"
        for game in self.games:
            message += game.__repr__()
        return message
