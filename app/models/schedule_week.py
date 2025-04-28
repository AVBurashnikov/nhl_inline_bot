import locale
from datetime import date as date_type, datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants.week_days import WEEK_DAYS
from app.models.base import NHLAPIBaseModel
from app.utils.text_snippets import team_icon
from app.utils.text_style import bold, underline, code


locale.setlocale(locale.LC_TIME, "ru-RU")


class NameDefault(NHLAPIBaseModel):
    default: str

    def render_message(self):
        return bold(self.default)


class Team(NHLAPIBaseModel):
    id: int
    common_name: NameDefault
    place_name: NameDefault
    abbrev: str

    def render_message(self):
        return f"{team_icon(self.abbrev)}{self.common_name.render_message()}"


class Game(NHLAPIBaseModel):
    id: int
    start_time_u_t_c: datetime
    game_state: str
    away_team: Team
    home_team: Team

    def render_message(self):
        start_time_msc = self.start_time_u_t_c + timedelta(hours=3)
        message = f"[{start_time_msc.time().strftime("%H:%M")}]"
        message += self.away_team.render_message()
        message += " - "
        message += self.home_team.render_message()
        message += "\n"
        return message


class GameDay(NHLAPIBaseModel):
    date: date_type
    day_abbrev: str
    number_of_games: int
    games: list[Game]

    def render_message(self):
        message = f"{self.date.day}-{self.date.day + 1} "
        message += f"{self.date.strftime("%b")}, {self.date.year}\n"
        for game in self.games:
            message += game.render_message()
        message += "\n"
        return message

    def render_menu(self):

        text = f"{self.date.day}-{self.date.day + 1} "
        text += f"{self.date.strftime("%b")}, {self.date.year}"
        text += " - "

        if self.number_of_games == 1:
            text += f"{self.number_of_games} игра"
        elif 2 <= self.number_of_games <= 4:
            text += f"{self.number_of_games} игры"
        else:
            text += f"{self.number_of_games} игр"

        return InlineKeyboardButton(
            text=text,
            callback_data=f"schedule_date_{self.date.strftime("%d.%m.%Y")}"
        )


class ScheduleWeekModel(NHLAPIBaseModel):
    game_week: list[GameDay]

    def render_message(self):
        message = bold("Расписание игр\n\n")
        for day in self.game_week:
            message += day.render_message()
        message += "\n\n"
        return message

    def render_menu(self):
        keyboard = []
        line = []
        line_len = 2
        item_counter = 0
        for day in self.game_week:
            line.append(day.render_menu())
            item_counter += 1
            if item_counter == line_len:
                keyboard.append(line)
                line = []
                item_counter = 0
        if len(line) > 0:
            keyboard.append(line)

        keyboard.append(
            [InlineKeyboardButton("🔙Back", callback_data="back"),
             InlineKeyboardButton("🔝Home", callback_data="home")]
        )

        return InlineKeyboardMarkup(keyboard)
