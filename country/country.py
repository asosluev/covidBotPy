import telebot
import os


import common.tg_analytics as tga

from functools import wraps

from services.country_service import CountryService
from services.statistics_service import StatisticsService


token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)
user_steps = {}
known_users = []
stats_service = StatisticsService()
country_service = CountryService()
def get_user_step(uid):
    if uid in user_steps:
        return user_steps[uid]
    else:
        known_users.append(uid)
        user_steps[uid] = 0
        return user_steps[uid]


# decorator for bot actions
def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(message, *args, **kwargs):
            bot.send_chat_action(chat_id=message.chat.id, action=action)
            return func(message, *args, **kwargs)
        return command_func
    return decorator


# decorator for save user activity
def save_user_activity():
    def decorator(func):
        @wraps(func)
        def command_func(message, *args, **kwargs):
            tga.statistics(message.chat.id, message.text)
            return func(message, *args, **kwargs)
        return command_func
    return decorator


@bot.message_handler(commands=['countryLocation'])
@send_action('typing')
@save_user_activity()
def countryLocationSng_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇺🇦 Україна', callback_data='ua'),
        telebot.types.InlineKeyboardButton(text='🇧🇾 Білорусь ', callback_data='by'),
        telebot.types.InlineKeyboardButton(text='🇰🇿Казахстан', callback_data='kz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇩Молдова', callback_data='md'),
        telebot.types.InlineKeyboardButton(text='🇷🇺 Росія', callback_data='ru'),
        telebot.types.InlineKeyboardButton(text='🇦🇿Азербайджан', callback_data='az'),
        # telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇺Угорщина ', callback_data='hu'),
        telebot.types.InlineKeyboardButton(text='🇰🇬Киргизстан', callback_data='kgz'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇯Таджикистан', callback_data='tj'),
        telebot.types.InlineKeyboardButton(text='🇺🇿Узбекистан', callback_data='uz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)