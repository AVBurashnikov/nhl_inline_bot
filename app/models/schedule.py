import locale
from datetime import date as date_type, datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants.week_days import WEEK_DAYS
from app.models.base import NHLAPIBaseModel
from app.utils.text_snippets import team_icon
from app.utils.text_style import bold, underline, code


locale.setlocale(locale.LC_TIME, "ru_RU")


class NameDefault(NHLAPIBaseModel):
    default: str

    def render(self):
        return self.default


class Team(NHLAPIBaseModel):
    id: int
    common_name: NameDefault
    place_name: NameDefault
    abbrev: str

    def render(self):
        return f"{team_icon(self.abbrev)}{self.common_name.render()}"


class Game(NHLAPIBaseModel):
    id: int
    season: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team

    def render_menu(self):
        start_time_msc = self.start_time_u_t_c + timedelta(hours=3)
        text = f"[{start_time_msc.time().strftime("%H:%M")}]   "
        text += f"{self.away_team.render()} - {self.home_team.render()}"
        return [InlineKeyboardButton(text=text, callback_data=f"game_{self.id}")]


class GameDay(NHLAPIBaseModel):
    date: date_type
    day_abbrev: str
    number_of_games: int
    games: list[Game]

    def render(self):
        message = underline(f"{WEEK_DAYS.get(self.day_abbrev)}, ")
        message += code(f"{self.date.strftime("%d.%m.%Y")}\n")
        if not self.games:
            message += "Игр нет\n\n"

        return message

    def render_menu(self):
        keyboard = []
        for game in self.games:
            keyboard.append(game.render_menu())

        return keyboard


class ScheduleModel(NHLAPIBaseModel):
    game_week: list[GameDay]

    def render_message(self, date: date_type = date_type.today()):
        current_date_loc = f"{date.day}-{date.day + 1} {date.strftime("%b")}, {date.year}"
        return bold(f"Расписание игр {current_date_loc}")

    def render_menu(self, date: date_type = date_type.today()):
        keyboard = []

        for day in self.game_week:
            if day.date == date:
                keyboard = day.render_menu()

        keyboard.append(
            [InlineKeyboardButton("Week schedule", callback_data="schedule_week"),
             InlineKeyboardButton("Team schedule", callback_data="schedule_team")],
        )
        keyboard.append(
            [InlineKeyboardButton("🔙Back", callback_data="back"),
             InlineKeyboardButton("🔝Home", callback_data="home")]
        )
        return InlineKeyboardMarkup(keyboard)
