from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start = KeyboardButton("/Start")
menu = KeyboardButton("/Меню",)
download = KeyboardButton("/Загрузить_txt")
clear = KeyboardButton("/Очистить_клавиатуру")
# share_number = KeyboardButton("/Поделиться номером")
# share_location = KeyboardButton("/Поделиться расположением")

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)

keyboard_client.add(start).add(menu).insert(download).add(clear)#.row(share_number, share_location)
