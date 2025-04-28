from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from app.models.base import NHLAPIBaseModel
from app.utils.text_snippets import team_icon
from app.utils.text_style import bold


class NameDefault(NHLAPIBaseModel):
    default: str

    def render(self):
        return self.default


class Team(NHLAPIBaseModel):
    id: int
    abbrev: str
    name: NameDefault
    common_name: NameDefault
    place_name_with_preposition: NameDefault

    def render(self):
        return f"{team_icon(self.abbrev)}{self.abbrev}"


class Series(NHLAPIBaseModel):
    series_title: str
    series_abbrev: str
    series_letter: str
    playoff_round: int
    top_seed_wins: int
    bottom_seed_wins: int
    top_seed_team: Team | None = None
    bottom_seed_team: Team | None = None

    def menu_button_or_none(self) -> list[InlineKeyboardButton] | None:
        if self.top_seed_team is None or self.bottom_seed_team is None:
            return None
        text = f"{self.top_seed_team.render()}"
        text += f" - "
        text += f"{self.bottom_seed_team.render()} | "
        text += f"Счет в серии: {self.top_seed_wins} - {self.bottom_seed_wins}"
        return [InlineKeyboardButton(
            text=text,
            callback_data=f"playoff_series_{self.series_letter}"
        )]


class PlayoffModel(NHLAPIBaseModel):
    series: list[Series]

    def render_message(self):
        return bold("Серии плейофф сезона 2024/2025")

    def render_menu(self):
        keyboard = []
        for match in self.series:
            button = match.menu_button_or_none()
            if button is not None:
                keyboard.append(button)
        keyboard.append(
            [InlineKeyboardButton("🔙Back", callback_data="back"),
             InlineKeyboardButton("🔝Home", callback_data="home")]
        )
        return InlineKeyboardMarkup(keyboard)
