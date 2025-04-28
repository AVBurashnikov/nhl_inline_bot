from datetime import date as date_type, datetime

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from app.models.base import NHLAPIBaseModel
from app.utils.text_snippets import team_icon, team_common_name, team_place_name
from app.utils.text_style import bold


class NameDefault(NHLAPIBaseModel):
    default: str

    def render(self):
        return self.default


class SeriesStatus(NHLAPIBaseModel):
    top_seed_wins: int
    bottom_seed_wins: int


class Team(NHLAPIBaseModel):
    id: int
    common_name: NameDefault
    place_name: NameDefault
    abbrev: str
    score: int | None = None

    def render(self):
        return f"{team_icon(self.abbrev)}{self.common_name.render()}  {self.score}"


class Game(NHLAPIBaseModel):
    id: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team
    series_status: SeriesStatus | None = None

    def menu_button_or_none(self):
        if self.game_state != "OFF":
            return None

        text = team_icon(self.away_team.abbrev)
        text += f"{self.away_team.abbrev}"
        text += " - "
        text += team_icon(self.home_team.abbrev)
        text += f"{self.home_team.abbrev}"
        text += " | "
        text += "Счет в матче: "
        text += f"{self.away_team.score}"
        text += " - "
        text += f"{self.home_team.score}"

        return [InlineKeyboardButton(
            text=text,
            callback_data=f"game_{self.id}"
        )]


class SeedTeam(NHLAPIBaseModel):
    abbrev: str
    series_wins: int

    def render_message(self):
        text = team_icon(self.abbrev)
        text += f"{team_place_name(self.abbrev)} {team_common_name(self.abbrev)}   "
        text += bold(self.series_wins)
        return text


class PlayoffSeriesModel(NHLAPIBaseModel):
    round: int
    series_letter: str
    top_seed_team: SeedTeam
    bottom_seed_team: SeedTeam
    games: list[Game]

    def render_message(self, series_letter: str):
        message = bold(f"Раунд {self.round}, ")
        message += f"Серия {series_letter}\n\n"
        message += bold("Счет в серии\n")
        message += f"{self.top_seed_team.render_message()}\n"
        message += f"{self.bottom_seed_team.render_message()}\n\n"
        message += bold("Матчи:")
        return message

    def render_menu(self, series_letter: str):
        keyboard = []
        for number, game in enumerate(self.games):
            button = game.menu_button_or_none()
            if button is not None:
                keyboard.append(button)
        keyboard.append(
            [InlineKeyboardButton("🔙Back", callback_data="back"),
             InlineKeyboardButton("🔝Home", callback_data="home")]
        )
        return InlineKeyboardMarkup(keyboard)