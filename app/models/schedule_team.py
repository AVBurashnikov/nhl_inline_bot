from datetime import date as date_type, datetime, timedelta

from app.models.base import NHLAPIBaseModel
from app.utils.text_snippets import team_icon, team_common_name, team_place_name
from app.utils.text_style import code, link, bold


class NameDefault(NHLAPIBaseModel):
    default: str

    def render(self):
        return bold(self.default)


class Team(NHLAPIBaseModel):
    id: int
    name: NameDefault
    common_name: NameDefault
    place_name_with_preposition: NameDefault
    abbrev: str
    score: int | None = None

    def render(self, team_abbrev):
        return f"{team_icon(self.abbrev)}{self.common_name.render()}"


class Game(NHLAPIBaseModel):
    id: int
    season: int
    game_type: int
    game_date: date_type
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team
    three_min_recap: str | None = None

    def render(self, team_abbrev):
        start_time_msc = self.start_time_u_t_c + timedelta(hours=3)
        message = code(f"[{start_time_msc.time().strftime("%H:%M")}]")
        message += f"{self.away_team.render(team_abbrev)} - {self.home_team.render(team_abbrev)}\n"
        if self.three_min_recap:
            message += f"{link("Обзор матча", f"https://nhl.com{self.three_min_recap}")}\n"
        message += "\n"
        return message


class GameDay(NHLAPIBaseModel):
    date: date_type
    games: list[Game]

    def render(self, team_abbrev):
        message = code(f"{self.date.strftime("%d.%m.%Y")}\n")
        for game in self.games:
            message += game.render(team_abbrev)
        return message


class ScheduleTeamModel(NHLAPIBaseModel):
    games_by_date: list[GameDay]

    def render(self, team_abbrev):
        message = f"Расписание игр для "
        message += f"{team_icon(team_abbrev)}"
        message += f"{team_place_name(team_abbrev)} "
        message += f"{team_common_name(team_abbrev)}\n\n"
        for game_day in self.games_by_date:
            message += game_day.render(team_abbrev)
        return message
