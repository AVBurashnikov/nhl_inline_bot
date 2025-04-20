from telegram import InlineKeyboardButton, InlineKeyboardMarkup

menu = [
    [InlineKeyboardButton("Day schedule", callback_data="day_schedule"),
     InlineKeyboardButton("Schedule", callback_data="schedule")],
    [InlineKeyboardButton("Main menu", callback_data="main_menu")],
]

schedule_menu = InlineKeyboardMarkup(menu)