from telegram import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton("Playoff", callback_data="playoff"),
     InlineKeyboardButton("Schedule", callback_data="schedule")],
    [InlineKeyboardButton("Score", callback_data="score"),
     InlineKeyboardButton("Stats", callback_data="stats")],
]

main_menu = InlineKeyboardMarkup(menu)