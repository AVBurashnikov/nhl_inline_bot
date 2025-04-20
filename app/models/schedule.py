from datetime import date as date_type, datetime, timedelta

from helpers.constants import WEEK_DAYS
from helpers.formatters import get_team_icon
from models.base import NHLAPIBaseModel
from utils.text_style import bold, underline, code


class NameDefault(NHLAPIBaseModel):
    default: str

    def __repr__(self):
        return bold(self.default)


class Team(NHLAPIBaseModel):
    id: int
    common_name: NameDefault
    place_name: NameDefault
    abbrev: str

    def __repr__(self):
        return f"{get_team_icon(self.abbrev.lower())} {self.common_name.__repr__()}"


class SeriesStatus(NHLAPIBaseModel):
    round: int
    series_abbrev: str
    series_title: str
    series_letter: str
    needed_to_win: int
    top_seed_team_abbrev: str
    top_seed_wins: int
    bottom_seed_team_abbrev: str
    bottom_seed_wins: int
    game_number_of_series: int


class Game(NHLAPIBaseModel):
    id: int
    season: int
    game_type: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team
    series_status: SeriesStatus | None = None

    def __repr__(self):
        start_time_msc = self.start_time_u_t_c + timedelta(hours=3)
        message = code(f"[{start_time_msc.time().strftime("%H:%M")}]")
        message += f"{self.away_team.__repr__()} - {self.home_team.__repr__()}"
        message += f" /g_{self.id}\n"
        return message


class GameDay(NHLAPIBaseModel):
    date: date_type
    day_abbrev: str
    number_of_games: int
    games: list[Game]

    def __repr__(self):
        message = underline(f"{WEEK_DAYS.get(self.day_abbrev)}, ")
        message += code(f"{self.date.strftime("%d.%m.%Y")}\n")
        if not self.games:
            message += "Игр нет\n\n"
        else:
            for game in self.games:
                message += game.__repr__()
            message += "\n"
        return message


class ScheduleModel(NHLAPIBaseModel):
    game_week: list[GameDay]

    def __repr__(self):
        message = bold("Расписание матчей\n\n")
        for game_day in self.game_week:
            message += game_day.__repr__()
        return message
