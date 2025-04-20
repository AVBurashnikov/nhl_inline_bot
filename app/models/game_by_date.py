from datetime import date as date_type, datetime

from helpers.formatters import get_team_icon
from utils.text_style import bold, italic
from models.base import NHLAPIBaseModel
from utils.text_snippets import hint


class GameDay(NHLAPIBaseModel):
    date: date_type
    day_abbrev: str
    number_of_games: int


class NameDefault(NHLAPIBaseModel):
    default: str

    def __repr__(self):
        return self.default


class Team(NHLAPIBaseModel):
    id: int
    name: NameDefault
    abbrev: str
    record: str | None = None
    score: int | None = None
    sog: int | None = None

    def __repr__(self):
        return f"{get_team_icon(self.abbrev.lower())} {self.name.__repr__()}"


class GameClock(NHLAPIBaseModel):
    time_remaining: str
    seconds_remaining: int
    running: bool
    in_intermission: bool


class PeriodDescriptor(NHLAPIBaseModel):
    number: int
    period_type: str  # PeriodTypeEnum


class Assist(NHLAPIBaseModel):
    player_id: int
    name: NameDefault
    assists_to_date: int

    # def __repr__(self):
    #     return f"{self.name.default}({self.assists_to_date})"


class Goal(NHLAPIBaseModel):
    period: int
    period_descriptor: PeriodDescriptor
    time_in_period: str
    player_id: int
    name: NameDefault
    first_name: NameDefault
    last_name: NameDefault
    goal_modifier: str | None = None
    assists: list[Assist]
    team_abbrev: str
    goals_to_date: int | None = None
    away_score: int
    home_score: int
    strength: str  # TeamStrengthEnum

    # def __repr__(self):
    #     goal = f"({self.away_score} - {self.home_score}) "
    #     goal += f"{self.time_in_period} {self.first_name} {self.last_name}\n"
    #     goal += f"Ассистенты: {" ".join(map(str, self.assists))}\n"
    #     return goal + "\n"


class GameOutcome(NHLAPIBaseModel):
    last_period_type: str  # PeriodTypeEnum


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


class TeamLeader(NHLAPIBaseModel):
    id: int
    first_name: NameDefault
    last_name: NameDefault
    team_abbrev: str
    sweater_number: int
    position: str
    category: str
    value: int | float


class Game(NHLAPIBaseModel):
    id: int
    season: int
    game_type: int  # GameTypeEnum
    game_date: date_type
    start_time_u_t_c: datetime
    game_state: str  # GameStateEnum
    away_team: Team
    home_team: Team
    series_status: SeriesStatus | None = None
    team_leaders: list[TeamLeader] | None = None
    three_min_recap: str | None = None
    clock: GameClock | None = None
    game_outcome: GameOutcome | None = None
    goals: list[Goal] | None = None

    def __repr__(self):
        game = f"{self.away_team.__repr__()} - {self.home_team.__repr__()}"
        game += f" /g_{self.id}\n"
        return game


class GamesByDateModel(NHLAPIBaseModel):

    prev_date: date_type
    current_date: date_type
    next_date: date_type

    game_week: list[GameDay]

    games: list[Game]

    def __repr__(self):
        message = f"{bold(self.current_date.strftime("%d.%m.%Y"))}\n\n"
        for game in self.games:
            message += f"{game.__repr__()}"
        footer = hint("нажмите на команду с кодом матча чтобы получить подробности")
        message += italic(footer)
        return message



