from telegram import InlineKeyboardButton, InlineKeyboardMarkup

home = [
    [InlineKeyboardButton("Playoff", callback_data="playoff"),
     InlineKeyboardButton("Schedule", callback_data="schedule")],
    [InlineKeyboardButton("Score", callback_data="score"),
     InlineKeyboardButton("Stats", callback_data="stats")],
]

main_menu = InlineKeyboardMarkup(home)

schedule = [
    [InlineKeyboardButton("Day schedule", callback_data="day_schedule"),
     InlineKeyboardButton("Team schedule", callback_data="team_schedule")],
    [InlineKeyboardButton("Home", callback_data="home")],
]

schedule_menu = InlineKeyboardMarkup(schedule)