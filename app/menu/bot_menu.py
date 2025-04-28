from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.constants.teams import TEAMS

_back_buttons = [InlineKeyboardButton("🔙Back", callback_data="back"), InlineKeyboardButton("🔝Home", callback_data="home")]

back_menu = InlineKeyboardMarkup([_back_buttons])

_main = [
    [InlineKeyboardButton("Playoff", callback_data="playoff")],
    [InlineKeyboardButton("Schedule", callback_data="schedule")],
    [InlineKeyboardButton("Score", callback_data="score")],
    [InlineKeyboardButton("Stats", callback_data="stats")],
]
main_menu = InlineKeyboardMarkup(_main)

_schedule = [
    [InlineKeyboardButton("Week schedule", callback_data="schedule_week"),
     InlineKeyboardButton("Team schedule", callback_data="schedule_team")],
    _back_buttons,
]
schedule_menu = InlineKeyboardMarkup(_schedule)

_schedule_team = []
_line = []
_counter = 0
for k, v in TEAMS.items():
    _line.append(InlineKeyboardButton(f"{v["icon"]}{k.upper()}", callback_data=f"schedule_team_{k}"))
    _counter += 1
    if _counter == 4:
        _schedule_team.append(_line)
        _line = []
        _counter = 0
_schedule_team.append(_back_buttons)
schedule_team_menu = InlineKeyboardMarkup(_schedule_team)
