import telebot
import os
import codecs

import common.tg_analytics as tga

from functools import wraps
from telebot import types
from jinja2 import Template
from services.country_service import CountryService
from services.statistics_service import StatisticsService

#from dotenv import load_dotenv

#load_dotenv()



# bot initialization
token = os.getenv('API_BOT_TOKEN')
bot = telebot.TeleBot(token)
user_steps = {}
known_users = []
stats_service = StatisticsService()
country_service = CountryService()
commands = {'start': 'Start using this bot',
            'country': 'Please, write a country name',
            'statistics': 'Statistics by users queries',
            'help': 'Useful information about this bot',
            'contacts': 'Developer contacts',
            'countryLocation': 'dsdsds'
            }


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


# start command handler
@bot.message_handler(commands=['start'])
@send_action('typing')
@save_user_activity()
def start_command_handler(message):
    cid = message.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='🤷‍♂Помощь!🤷‍♀', callback_data=1))
    markup.add(telebot.types.InlineKeyboardButton(text='🚨Статистика!🚨', callback_data=2))
    markup.add(telebot.types.InlineKeyboardButton(text='🎫Контакты!', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='🌐Начало!🌐', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='Covid-19', callback_data=7))
    markup.add(telebot.types.InlineKeyboardButton(text='📊  Выбор страны!🗺', callback_data=5))
    markup.add(telebot.types.InlineKeyboardButton(text='🧭Отправить геопозицию!', callback_data=6))
    bot.send_message(cid, 'Првиет, {0}, Виберите команду из меню'.format(message.chat.username),reply_markup=markup)


@bot.message_handler(commands=['country'])
@send_action('typing')
@save_user_activity()
def country_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    bot.send_message(cid, '{0}, write name of country please'.format(message.chat.username))
# countryLocation command handler
@bot.message_handler(commands=['countryLocation'])
@send_action('typing')
@save_user_activity()
def countryLocation_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    # bot.py
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🗺Країни СНД', callback_data='sng'),
        telebot.types.InlineKeyboardButton(text='🌍Європа ', callback_data='europe'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🌏Азія', callback_data='Asia'),
        telebot.types.InlineKeyboardButton(text='🌍Африка', callback_data='Africa'),
        #telebot.types.InlineKeyboardButton(text='Антарктида', callback_data='Antarctica'),

    )
    markup.row(telebot.types.InlineKeyboardButton(text='🌏Австралія і Океанія', callback_data='Australia'))
    markup.row(telebot.types.InlineKeyboardButton(text='Марс', callback_data=1))
    markup.row(telebot.types.InlineKeyboardButton(text='↩Назад', callback_data=4))
    bot.send_message(cid, '{0}, Виберіть локацію зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)
#SNG
@bot.message_handler(commands=['countryLocationSng'])
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
#Europe
@bot.message_handler(commands=['countryLocationEurope'])
@send_action('typing')
@save_user_activity()
def countryLocationEurope_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇹 Австрія', callback_data='at'),
        telebot.types.InlineKeyboardButton(text='🇧🇪	Бельгія', callback_data='be'),
        telebot.types.InlineKeyboardButton(text='🇱🇮 Ліхтенштейн', callback_data='li')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇺 Люксембург', callback_data='lu'),
        telebot.types.InlineKeyboardButton(text='🇲🇨 Монако', callback_data='mc'),
        telebot.types.InlineKeyboardButton(text='🇳🇱 Нідерланди', callback_data='nl'),
        # telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇩🇪 Німеччина', callback_data=' de'),
        telebot.types.InlineKeyboardButton(text='🇫🇷 Франція', callback_data='fr'),
        telebot.types.InlineKeyboardButton(text='🇨🇭Швейцарія', callback_data='ch')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇱Албанія', callback_data='al'),
        telebot.types.InlineKeyboardButton(text='🇦🇩Андорра', callback_data='ad'),
        telebot.types.InlineKeyboardButton(text='🇬🇷Греція', callback_data='gr'),
       telebot.types.InlineKeyboardButton(text='🇧🇦Боснія і Герцеговина', callback_data='ba')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇻🇦	Ватикан', callback_data='va'),
        telebot.types.InlineKeyboardButton(text='🇪🇸Іспанія', callback_data='es'),
        telebot.types.InlineKeyboardButton(text='🇮🇹Італія', callback_data='it')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇰Македонія', callback_data='mk'),
        telebot.types.InlineKeyboardButton(text='🇵🇹Португалія', callback_data='pt'),
        telebot.types.InlineKeyboardButton(text='🇲🇹Мальта', callback_data='mt')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇲Сан-Марино', callback_data='Sint-Maarten'),
        telebot.types.InlineKeyboardButton(text='🇸🇮Словенія', callback_data='sl'),
        telebot.types.InlineKeyboardButton(text='🇭🇷Хорватія', callback_data='hr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇪Чорногорія', callback_data='me'),
        telebot.types.InlineKeyboardButton(text='🇬🇧Велика Британія', callback_data='gb'),
        telebot.types.InlineKeyboardButton(text='🇩🇰 Данія*', callback_data='dk')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇪Естонія', callback_data='ee'),
        telebot.types.InlineKeyboardButton(text='🇮🇪Ірландія', callback_data='ie'),
        telebot.types.InlineKeyboardButton(text='🇮🇸Ісландія', callback_data='is')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇻Латвія', callback_data='lv'),
        telebot.types.InlineKeyboardButton(text='🇱🇹Литва', callback_data='lt'),
        telebot.types.InlineKeyboardButton(text='🇳🇴Норвегія', callback_data='no')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇫🇮Фінляндія', callback_data='fi'),
        telebot.types.InlineKeyboardButton(text='🇸🇪Швеція', callback_data='se'),
        telebot.types.InlineKeyboardButton(text='🇳🇴Норвегія', callback_data='no')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇾 Білорусь ', callback_data='by'),
        telebot.types.InlineKeyboardButton(text='🇧🇬Болгарія*', callback_data='bg'),
        telebot.types.InlineKeyboardButton(text='🇲🇩Молдова', callback_data='md')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇱Польща ', callback_data='pl'),
        telebot.types.InlineKeyboardButton(text='🇷🇴Румунія', callback_data='ro'),
        telebot.types.InlineKeyboardButton(text='🇸🇰	Словаччина*', callback_data='sk')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇺Угорщина ', callback_data='hu'),
        telebot.types.InlineKeyboardButton(text='🇺🇦 Україна', callback_data='ua'),
        telebot.types.InlineKeyboardButton(text='🇨🇿Чехія', callback_data='cz')
    )

    markup.row(telebot.types.InlineKeyboardButton(text='Європа ', callback_data='statisticeurope'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну Европи зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)
#Asia
@bot.message_handler(commands=['countryLocationAsia'])
@send_action('typing')
@save_user_activity()
def countryLocationAsia_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇫Афганістан', callback_data='af'),
        telebot.types.InlineKeyboardButton(text='🇦🇿Азербайджан', callback_data='az'),
        telebot.types.InlineKeyboardButton(text='🇦🇲 Вірменія', callback_data='am')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇭Бахрейн', callback_data='bh'),
        telebot.types.InlineKeyboardButton(text='🇧🇩Бангладеш', callback_data='bd'),
        telebot.types.InlineKeyboardButton(text='🇧🇹Бутан', callback_data='bt'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇳Бруней', callback_data='bn'),
        telebot.types.InlineKeyboardButton(text='🇲🇲Бірма', callback_data='mm'),
        telebot.types.InlineKeyboardButton(text='🇰🇭Камбоджа', callback_data='kh'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇳КНР', callback_data='cn'),
        telebot.types.InlineKeyboardButton(text='🇨🇾Кіпр', callback_data='cy'),
        telebot.types.InlineKeyboardButton(text='🇹🇱Східний Тимор', callback_data='tl'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇪Грузія', callback_data='ge'),
        telebot.types.InlineKeyboardButton(text='🇭🇰Гонконг', callback_data='hk'),
        telebot.types.InlineKeyboardButton(text='🇮🇳	Індія', callback_data='in'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇮🇩Індонезія', callback_data='id'),
        telebot.types.InlineKeyboardButton(text='🇮🇷Іран', callback_data='ir'),
        telebot.types.InlineKeyboardButton(text='🇮🇶Ірак', callback_data='iq'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇮🇱 Ізраїль', callback_data='il'),
        telebot.types.InlineKeyboardButton(text='🇯🇵Японія', callback_data='jp'),
        telebot.types.InlineKeyboardButton(text='🇯🇴Йорданія', callback_data='jo'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇰🇿Казахстан', callback_data='kz'),
        telebot.types.InlineKeyboardButton(text='🇰🇷Корея', callback_data='kr'),
        telebot.types.InlineKeyboardButton(text='🇰🇼Кувейт', callback_data='kw'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇰🇬Киргизстан', callback_data='kg'),
        telebot.types.InlineKeyboardButton(text='🇱🇦Лаос', callback_data='la'),
        telebot.types.InlineKeyboardButton(text='🇱🇧Ліван', callback_data='lb'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇴Макао', callback_data='mo'),
        telebot.types.InlineKeyboardButton(text='🇲🇾Малайзія', callback_data='my'),
        telebot.types.InlineKeyboardButton(text='🇲🇻Мальдіви', callback_data='mv'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇳Монголія', callback_data='mn'),
        telebot.types.InlineKeyboardButton(text='🇳🇵Непал', callback_data='np'),
        telebot.types.InlineKeyboardButton(text='🇴🇲Оман', callback_data='om'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇰Пакистан', callback_data='pk'),
        telebot.types.InlineKeyboardButton(text='🇵🇭Філіппіни', callback_data='ph'),
        telebot.types.InlineKeyboardButton(text='🇶🇦Катар', callback_data='qa'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇷🇺Росія', callback_data='ru'),
        telebot.types.InlineKeyboardButton(text='🇸🇦Саудівська Аравія', callback_data='sa'),
        telebot.types.InlineKeyboardButton(text='🇸🇬Сінгапур', callback_data='sg'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇰Шрі-Ланка', callback_data='lk'),
        telebot.types.InlineKeyboardButton(text='🇸🇾Сирія', callback_data='sy'),
        telebot.types.InlineKeyboardButton(text='🇹🇼Тайвань', callback_data='tw'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇯Таджикистан', callback_data='tj'),
        telebot.types.InlineKeyboardButton(text='🇹🇭Таїланд', callback_data='th'),
        telebot.types.InlineKeyboardButton(text='🇹🇷Туреччина', callback_data='tr'),
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Туркменістан', callback_data='tm'),
        telebot.types.InlineKeyboardButton(text='ОАЕ', callback_data='ae'),
        telebot.types.InlineKeyboardButton(text='🇺🇿Узбекистан', callback_data='uz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇻🇳 В`єтнам', callback_data='vn'),
        telebot.types.InlineKeyboardButton(text='🇾🇪Ємен', callback_data='ye')
    )

    markup.row(telebot.types.InlineKeyboardButton(text='Азія ', callback_data='statisticasia'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid, '{0}, Виберіть країну Азії зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)

#Africa
@bot.message_handler(commands=['countryLocationAfrica'])
@send_action('typing')
@save_user_activity()
def countryLocationAfrica_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='Азорські острови', callback_data='raa'),
        telebot.types.InlineKeyboardButton(text='🇩🇿Алжир', callback_data='dz'),
        telebot.types.InlineKeyboardButton(text='🇦🇴Ангола', callback_data='ao')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇯Бенін', callback_data='bj'),
        telebot.types.InlineKeyboardButton(text='🇧🇼Ботсвана', callback_data='bw'),
        telebot.types.InlineKeyboardButton(text='🇧🇫Буркіна-Фасо', callback_data='bf')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇮Бурунді', callback_data='bi'),
        telebot.types.InlineKeyboardButton(text='🇬🇦Габон', callback_data='ga'),
        telebot.types.InlineKeyboardButton(text='🇬🇲Гамбія', callback_data='gm')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇭Гана', callback_data='gh'),
        telebot.types.InlineKeyboardButton(text='🇬🇳Гвінея', callback_data='gn'),
        telebot.types.InlineKeyboardButton(text='🇬🇼Гвінея-Бісау', callback_data='gw')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇩Демократична Республіка Конго', callback_data='cd'),
        telebot.types.InlineKeyboardButton(text='🇩🇯Джибуті', callback_data='dj'),
        telebot.types.InlineKeyboardButton(text='🇬🇶Екваторіальна Гвінея', callback_data='gq')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇷Еритрея', callback_data='er'),
        telebot.types.InlineKeyboardButton(text='🇪🇹Ефіопія', callback_data='et'),
        telebot.types.InlineKeyboardButton(text='🇪🇬Єгипет', callback_data='eg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇿🇲Замбія', callback_data='zm'),
        telebot.types.InlineKeyboardButton(text='🇿🇼Зімбабве', callback_data='zw'),
        telebot.types.InlineKeyboardButton(text='🇨🇻Кабо-Верде', callback_data='cv')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇲Камерун', callback_data='cm'),
        telebot.types.InlineKeyboardButton(text='🇰🇪Кенія', callback_data='ke'),
        telebot.types.InlineKeyboardButton(text='Кот-д`Івуар', callback_data='ci')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇱🇸Лесото', callback_data='ls'),
        telebot.types.InlineKeyboardButton(text='🇱🇷Ліберія', callback_data='lr'),
        telebot.types.InlineKeyboardButton(text='🇲🇺Маврикій', callback_data='mu')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇷Мавританія', callback_data='mr'),
        telebot.types.InlineKeyboardButton(text='🇲🇬Мадагаскар', callback_data='mg'),
        telebot.types.InlineKeyboardButton(text='🇲🇱Малі', callback_data='ml')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇾🇹Майотта', callback_data='yt'),
        telebot.types.InlineKeyboardButton(text='🇲🇼Малаві', callback_data='mw'),
        telebot.types.InlineKeyboardButton(text='🇲🇦Марокко', callback_data='ma')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇪🇦Мелілья', callback_data='mel'),
        telebot.types.InlineKeyboardButton(text='🇲🇿Мозамбік', callback_data='mz'),
        telebot.types.InlineKeyboardButton(text='🇳🇦	Намібія', callback_data='na')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇬Нігерія', callback_data='ng'),
        telebot.types.InlineKeyboardButton(text='🇿🇦ЮAР', callback_data='za'),
        telebot.types.InlineKeyboardButton(text='🇸🇸Південний Судан', callback_data='sss')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Республіка Конго', callback_data='cg'),
        telebot.types.InlineKeyboardButton(text='🇷🇪Реюньйон', callback_data='re'),
        telebot.types.InlineKeyboardButton(text='🇷🇼Руанда', callback_data='rw')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇹Сан-Томе і Принсіпі', callback_data='st'),
        telebot.types.InlineKeyboardButton(text='🇸🇨Сейшельські Острови', callback_data='sc'),
        telebot.types.InlineKeyboardButton(text='🇸🇳Сенегал', callback_data='sn')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇴Сомалі', callback_data='so'),
        telebot.types.InlineKeyboardButton(text='🇸🇩Судан', callback_data='sd'),
        telebot.types.InlineKeyboardButton(text='🇸🇱Сьєрра-Леоне', callback_data='sl')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇿Танзанія', callback_data='tz'),
        telebot.types.InlineKeyboardButton(text='🇹🇬Того', callback_data='tg'),
        telebot.types.InlineKeyboardButton(text='🇹🇳Туніс', callback_data='tn')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇺🇬Уганда', callback_data='ug'),
        telebot.types.InlineKeyboardButton(text='🇨🇫Центральноафриканська Республіка', callback_data='cf'),
        telebot.types.InlineKeyboardButton(text='🇹🇩Чад', callback_data='td')
    )
    markup.row(telebot.types.InlineKeyboardButton(text='Африка ', callback_data='statisticafrica'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,'{0}, Виберіть країну Африки зі списку по якій потрібна інформація'.format(message.chat.username), reply_markup=markup)

#Aьукшсф
@bot.message_handler(commands=['countryLocationAmerica'])
@send_action('typing')
@save_user_activity()
def countryLocationAmerica_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇲Бермудські Острови', callback_data='bm'),
        telebot.types.InlineKeyboardButton(text='🇬🇱Гренландія', callback_data='gl'),
        telebot.types.InlineKeyboardButton(text='🇨🇦Канада', callback_data='ca')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇽Мексика', callback_data='mx'),
        telebot.types.InlineKeyboardButton(text='США', callback_data='usa'),
        telebot.types.InlineKeyboardButton(text='🇧🇿Беліз', callback_data='bz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇬🇹Гватемала', callback_data='gt'),
        telebot.types.InlineKeyboardButton(text='🇭🇳Гондурас', callback_data='hn'),
        telebot.types.InlineKeyboardButton(text='🇨🇷Коста-Рика', callback_data='cr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇮Нікарагуа', callback_data='ni'),
        telebot.types.InlineKeyboardButton(text='🇵🇦Панама', callback_data='pa'),
        telebot.types.InlineKeyboardButton(text='🇸🇻Сальвадор', callback_data='sv')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇬Антигуа і Барбуда', callback_data='ag'),
        telebot.types.InlineKeyboardButton(text='🇦🇼Аруба', callback_data='aw'),
        telebot.types.InlineKeyboardButton(text='🇧🇸Багамські Острови', callback_data='bs')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇧🇧Барбадос', callback_data='bb'),
        telebot.types.InlineKeyboardButton(text='🇧🇶Бонайре', callback_data='bq'),
        telebot.types.InlineKeyboardButton(text='🇻🇬Британські Віргінські Острови', callback_data='vg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇭🇹Гаїті', callback_data='ht'),
        telebot.types.InlineKeyboardButton(text='🇬🇵Гваделупа', callback_data='gp'),
        telebot.types.InlineKeyboardButton(text='🇬🇩Гренада', callback_data='gd')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇩🇲Домініка', callback_data='dm'),
        telebot.types.InlineKeyboardButton(text='🇩🇴Домініканська Республіка', callback_data='do'),
        telebot.types.InlineKeyboardButton(text='🇰🇾Кайманові Острови', callback_data='ky')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇨🇺Куба', callback_data='cu'),
        telebot.types.InlineKeyboardButton(text='🇨🇼Кюрасао', callback_data='cw'),
        telebot.types.InlineKeyboardButton(text='🇲🇶Мартиніка', callback_data='mq')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇲🇸Монтсеррат', callback_data='ms'),
        telebot.types.InlineKeyboardButton(text='🇹🇨Острови Теркс і Кайкос', callback_data='tc'),
        telebot.types.InlineKeyboardButton(text='🇵🇷Пуерто-Рико ', callback_data='pr')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇳🇱Саба ', callback_data='bq'),
        telebot.types.InlineKeyboardButton(text='🇯🇲Ямайка', callback_data='jm'),
        telebot.types.InlineKeyboardButton(text=' Сент-Люсія', callback_data='lc')
    )

    markup.row(
        telebot.types.InlineKeyboardButton(text='Пд Америка', callback_data='statisticamericaso'),
        telebot.types.InlineKeyboardButton(text='ПН Ямайка', callback_data='statisticamericano')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,'{0}, Виберіть країну Америки зі списку по якій потрібна інформація'.format(message.chat.username),reply_markup=markup)

#Australia
@bot.message_handler(commands=['countryLocationAustralia'])
@send_action('typing')
@save_user_activity()
def countryLocationAustralia_command_handler(message):
    cid = message.chat.id
    user_steps[cid] = 1
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇦🇺Австралія', callback_data='au'),
        telebot.types.InlineKeyboardButton(text='🇻🇺Вануату', callback_data='vu'),
        telebot.types.InlineKeyboardButton(text='🇵🇬Папуа Нова Гвінея', callback_data='pg')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇸🇧Соломонові острови', callback_data='sb'),
        telebot.types.InlineKeyboardButton(text='🇫🇯Фіджі', callback_data='fj'),
        telebot.types.InlineKeyboardButton(text='🇰🇮Кірібаті', callback_data='ki')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='Маршаллові острови', callback_data='mh'),
        telebot.types.InlineKeyboardButton(text='🇳🇷Науру', callback_data='nr'),
        telebot.types.InlineKeyboardButton(text='🇳🇿Нова Зеландія', callback_data='nz')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇵🇼Палау', callback_data='pw'),
        telebot.types.InlineKeyboardButton(text='🇼🇸Самоа', callback_data='ws'),
        telebot.types.InlineKeyboardButton(text='🇹🇴Тонга', callback_data='to')
    )
    markup.row(
        telebot.types.InlineKeyboardButton(text='🇹🇻Тувалу', callback_data='tv'),
        telebot.types.InlineKeyboardButton(text='🇫🇲Федеративні Штати Мікронезії', callback_data='fm'),
        telebot.types.InlineKeyboardButton(text='', callback_data='to')
    )
    markup.row(telebot.types.InlineKeyboardButton(text='Австараліа', callback_data='statisticaustralia'))
    markup.row(
        telebot.types.InlineKeyboardButton(text='↩Назад', callback_data='nazad'),
        telebot.types.InlineKeyboardButton(text='📲Меню', callback_data=4)
    )
    bot.send_message(cid,
                     '{0}, Виберіть країну Америки зі списку по якій потрібна інформація'.format(message.chat.username),
                     reply_markup=markup)


@bot.message_handler(commands=['helpcovid'])
@send_action('typing')
@save_user_activity()
def helpcovid_command_handler(message):
    cid = message.chat.id
    markupcovid = telebot.types.InlineKeyboardMarkup()
    markupcovid.row(
        telebot.types.InlineKeyboardButton(text='Fizer', callback_data='fizer'),
        telebot.types.InlineKeyboardButton(text='Coronavac', callback_data='coronavac'),
        telebot.types.InlineKeyboardButton(text='Moderna', callback_data='moderna')
    )
    with codecs.open('templates/helpcovid.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())

        bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML',reply_markup=markupcovid)

def helpcovidFizer_command_handler(message):
    cid=message.chat.id
    with codecs.open('templates/helpCovidFizer.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
    bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    kb = types.InlineKeyboardMarkup()
    cid = call.message.chat.id
    mid = call.message.message_id

    bot.answer_callback_query(callback_query_id=call.id, text='Ви обрали країну!')

    match call.data:
        case "1":
            help_command_handler(call.message)
        case "2":
            statistics_command_handler(call.message)
        case "3":
            contacts_command_handler(call.message)
        case "4":
            start_command_handler(call.message)
        case "5":
            countryLocation_command_handler(call.message)
        case "6":
             countryLocationSend_command_handler(call.message)
        case "7":
             helpcovid_command_handler(call.message)
        case "fizer":
            helpcovidFizer_command_handler(call.message)
        case "nazad":
            countryLocation_command_handler(call.message)
        case "sng":
            countryLocationSng_command_handler(call.message)
        case "europe":
            countryLocationEurope_command_handler(call.message)
        case "statisticeurope":
            countrytest_statistics_command_handler(call.message, 'europe')
        case "Asia":
            countryLocationAsia_command_handler(call.message)
        case "statisticasia":
            countrytest_statistics_command_handler(call.message, 'asia')
        case "Africa":
            countryLocationAfrica_command_handler(call.message)
        case "statisticafrica":
            countrytest_statistics_command_handler(call.message, 'africa')
        case "America":
            countryLocationAmerica_command_handler(call.message)
        case "statisticamericaso":
            countrytest_statistics_command_handler(call.message, 'America')
        case "statisticamericano":
            countrytest_statistics_command_handler(call.message, 'America')
        case "Australia":
            countryLocationAustralia_command_handler(call.message)
        case "statisticaustralia":
            countrytest_statistics_command_handler(call.message, 'statisticaustralia')
        case 'ua':
             countrytest_statistics_command_handler(call.message, 'UKRAINE')
        case "by":
            countrytest_statistics_command_handler(call.message, 'Belarus')
        case "kz":
             countrytest_statistics_command_handler(call.message, 'Kazakhstan')
        case "md":
            countrytest_statistics_command_handler(call.message, 'Moldova')
        case "ru":
            countrytest_statistics_command_handler(call.message, 'Russia')
        case "az":
            countrytest_statistics_command_handler(call.message, 'Azerbaijan')
        case "tm":
            countrytest_statistics_command_handler(call.message, 'Turkmenistan')
        case "am":
            countrytest_statistics_command_handler(call.message, 'Armenia')
        case "kgz":
            countrytest_statistics_command_handler(call.message, 'Kyrgyzstan')
        case "tj":
            countrytest_statistics_command_handler(call.message, 'Tajikistan')
        case "uz":
            countrytest_statistics_command_handler(call.message, 'Uzbekistan')
        case "at":
            countrytest_statistics_command_handler(call.message, "Austria")
        case "be":
            countrytest_statistics_command_handler(call.message, "Belgium")
        case "li":
            countrytest_statistics_command_handler(call.message,'Liechtenstein')
        case "lu":
            countrytest_statistics_command_handler(call.message,'Luxembourg')
        case "mc":
            countrytest_statistics_command_handler(call.message,'Monaco')
        case "nl":
            countrytest_statistics_command_handler(call.message,'Netherlands')
        case "de":
            countrytest_statistics_command_handler(call.message,'Germany')
        case "fr":
            countrytest_statistics_command_handler(call.message,'France')
        case "ch":
            countrytest_statistics_command_handler(call.message,'Switzerland')
        case "al":
            countrytest_statistics_command_handler(call.message,'Albania')
        case "ad":
            countrytest_statistics_command_handler(call.message,'Andorra')
        case"ba":
            countrytest_statistics_command_handler(call.message,'Bosnia-and-Herzegovina')
        case "gr":
            countrytest_statistics_command_handler(call.message,'Greece')
        case "va":
            countrytest_statistics_command_handler(call.message,'Vatican-City')
        case "es":
            countrytest_statistics_command_handler(call.message, 'Spain')
        case "it":
            countrytest_statistics_command_handler(call.message,'Italy')
        case "mk":
            countrytest_statistics_command_handler(call.message,'North-Macedonia')
        case "pt":
            countrytest_statistics_command_handler(call.message,'Portugal')
        case "mt":
            countrytest_statistics_command_handler(call.message,'Malta')
        case "sm":
            countrytest_statistics_command_handler(call.message,'SanMarino')
        case "rs":
            countrytest_statistics_command_handler(call.message, 'Serbia')
        case "sl":
            countrytest_statistics_command_handler(call.message,'Slovenia')
        case "hr":
            countrytest_statistics_command_handler(call.message,"Croatia")
        case "me":
            countrytest_statistics_command_handler(call.message,'Montenegro')
        case "gb":
            countrytest_statistics_command_handler(call.message, 'UK')
        case "dk":
            countrytest_statistics_command_handler(call.message,'Denmark')
        case "ee":
            countrytest_statistics_command_handler(call.message, 'Estonia')
        case "ie":
            countrytest_statistics_command_handler(call.message, 'Ireland')
        case "is":
            countrytest_statistics_command_handler(call.message, 'Iceland')
        case "lv":
            countrytest_statistics_command_handler(call.message, 'Latvia')
        case "lt":
            countrytest_statistics_command_handler(call.message, 'Lithuania')
        case "no":
            countrytest_statistics_command_handler(call.message, 'Norway')
        case "fi":
            countrytest_statistics_command_handler(call.message, 'Finland')
        case "se":
            countrytest_statistics_command_handler(call.message, 'Sweden')
        case "bg":
            countrytest_statistics_command_handler(call.message, 'Bulgaria')
        case "pl":
            countrytest_statistics_command_handler(call.message, 'Poland')
        case "ro":
            countrytest_statistics_command_handler(call.message, 'Romania')
        case "sk":
            countrytest_statistics_command_handler(call.message, 'Slovakia')
        case "hu":
            countrytest_statistics_command_handler(call.message, 'Hungary')
        case "cz":
            countrytest_statistics_command_handler(call.message, 'Czechia')
        case "af":
            countrytest_statistics_command_handler(call.message, 'Afghanistan')
        case "am":
            countrytest_statistics_command_handler(call.message, 'Armenia')
        case "bh":
            countrytest_statistics_command_handler(call.message, 'Bahrain')
        case "bh":
            countrytest_statistics_command_handler(call.message, 'Bangladesh')
        case "bt":
            countrytest_statistics_command_handler(call.message,'Bhutan')
        case "bn":
            countrytest_statistics_command_handler(call.message, 'Brunei-')
        case "mm":
            countrytest_statistics_command_handler(call.message, 'Burma')
        case "kh":
            countrytest_statistics_command_handler(call.message, 'Cambodia')
        case "cn":
            countrytest_statistics_command_handler(call.message, 'China')
        case "cy":
            countrytest_statistics_command_handler(call.message, 'Cyprus')
        case "tl":
            countrytest_statistics_command_handler(call.message, 'Timor-Leste')
        case "ge":
            countrytest_statistics_command_handler(call.message, 'Georgia')
        case "hk":
            countrytest_statistics_command_handler(call.message, 'Hong-Kong')
        case "in":
            countrytest_statistics_command_handler(call.message, 'India')
        case "id":
            countrytest_statistics_command_handler(call.data, 'Indonesia')
        case "ir":
            countrytest_statistics_command_handler(call.data, '	Iran')
        case "iq":
            countrytest_statistics_command_handler(call.message, 'Iraq')
        case "il":
            countrytest_statistics_command_handler(call.message, 'Israel')
        case "jp":
            countrytest_statistics_command_handler(call.message, 'Japan')
        case "jo":
            countrytest_statistics_command_handler(call.message, 'Jordan')
        case "kr":
            countrytest_statistics_command_handler(call.message, 'S.-Korea')
        case "kw":
            countrytest_statistics_command_handler(call.message, 'Kuwait')
        case "kg":
            countrytest_statistics_command_handler(call.message, 'Kyrgyzstan')
        case "la":
            countrytest_statistics_command_handler(call.message, 'Laos')
        case "lb":
            countrytest_statistics_command_handler(call.message, 'Lebanon')
        case "mo":
            countrytest_statistics_command_handler(call.message, 'Macau')
        case "my":
            countrytest_statistics_command_handler(call.message, 'Malaysia')
        case "mv":
            countrytest_statistics_command_handler(call.message, 'Maldives')
        case "mn":
            countrytest_statistics_command_handler(call.message, 'Mongolia')
        case "np":
            countrytest_statistics_command_handler(call.message, 'Nepal')
        case "om":
            countrytest_statistics_command_handler(call.message, 'Oman')
        case "pk":
            countrytest_statistics_command_handler(call.message, 'Pakistan')
        case "ph":
            countrytest_statistics_command_handler(call.message, 'Philippines')
        case "qa":
            countrytest_statistics_command_handler(call.message, 'Quatar')
        case "sa":
            countrytest_statistics_command_handler(call.message, 'Saudi-Arabia')
        case "sg":
            countrytest_statistics_command_handler(call.message, 'Singapore')
        case "lk":
            countrytest_statistics_command_handler(call.message, 'Sri-Lanka')
        case "sy":
            countrytest_statistics_command_handler(call.message, 'Syria')
        case "tw":
            countrytest_statistics_command_handler(call.message, 'Taiwan')
        case "th":
            countrytest_statistics_command_handler(call.message, 'Thailand')
        case "tr":
            countrytest_statistics_command_handler(call.message, 'Turkey')
        case "ae":
            countrytest_statistics_command_handler(call.message, 'UAE')
        case "vn":
            countrytest_statistics_command_handler(call.message, 'Vietnam')
        case "ye":
            countrytest_statistics_command_handler(call.message, 'Yemen')
        case "dz":
            countrytest_statistics_command_handler(call.message, 'Algeria')
        case "ao":
            countrytest_statistics_command_handler(call.message, 'Angola')
        case "bj":
            countrytest_statistics_command_handler(call.message, 'Benin')
        case "bw":
            countrytest_statistics_command_handler(call.message, 'Botswana')
        case "bf":
            countrytest_statistics_command_handler(call.message, 'Burkina-Faso')
        case "bi":
            countrytest_statistics_command_handler(call.message, 'Burundi')
        case "ga":
            countrytest_statistics_command_handler(call.message, 'Gabon')
        case "gm":
            countrytest_statistics_command_handler(call.message, 'Gambia')
        case "gh":
            countrytest_statistics_command_handler(call.message, 'Ghana')
        case "gn":
            countrytest_statistics_command_handler(call.message, 'Guinea')
        case "gw":
            countrytest_statistics_command_handler(call.message, 'Guinea-Bissau')
        case "cd":
            countrytest_statistics_command_handler(call.message, 'Congo, Democratic Republic of the')
        case "dj":
            countrytest_statistics_command_handler(call.message, 'Djibouti')
        case "gq":
            countrytest_statistics_command_handler(call.message, 'Equatorial-Guinea')
        case "er":
            countrytest_statistics_command_handler(call.message, 'Eritrea')
        case "et":
            countrytest_statistics_command_handler(call.message, 'Ethiopia')
        case "eg":
            countrytest_statistics_command_handler(call.message, 'Egypt')
        case "zm":
            countrytest_statistics_command_handler(call.message, 'Zambia')
        case "zw":
            countrytest_statistics_command_handler(call.message, 'Zimbabwe')
        case "cv":
            countrytest_statistics_command_handler(call.message, 'Cape-Verde')
        case "cm":
            countrytest_statistics_command_handler(call.message, 'Cameroon')
        case "ke":
            countrytest_statistics_command_handler(call.message, 'Kenya')
        case "ci":
            countrytest_statistics_command_handler(call.message, 'Cote')
        case "ls":
            countrytest_statistics_command_handler(call.message, 'Lesotho')
        case "lr":
            countrytest_statistics_command_handler(call.message, 'Liberia')
        case "mu":
            countrytest_statistics_command_handler(call.message, 'Mauritius')
        case "mr":
            countrytest_statistics_command_handler(call.message, 'Mauritania')
        case "mg":
            countrytest_statistics_command_handler(call.message, 'Madagascar')
        case "yt":
            countrytest_statistics_command_handler(call.message, 'Mayotte')
        case "mw":
            countrytest_statistics_command_handler(call.message, 'Malawi')
        case "ml":
            countrytest_statistics_command_handler(call.message, 'Mali')
        case "ma":
            countrytest_statistics_command_handler(call.message, 'Morocco')
        case "mel":
            countrytest_statistics_command_handler(call.message, 'Melilla')
        case "mz":
            countrytest_statistics_command_handler(call.message, 'Mozambique')
        case "na":
            countrytest_statistics_command_handler(call.message, 'Namibia')
        case "ng":
            countrytest_statistics_command_handler(call.message, 'Nigeria')
        case "za":
            countrytest_statistics_command_handler(call.message, 'South-Africa')
        case "sss":
            countrytest_statistics_command_handler(call.message, 'South-Sudan')
        case "cg":
            countrytest_statistics_command_handler(call.message, '🇨🇬Republic of the Congo')
        case "re":
            countrytest_statistics_command_handler(call.message, 'Reunion')
        case "rw":
            countrytest_statistics_command_handler(call.message, 'Rwanda')
        case "st":
            countrytest_statistics_command_handler(call.message, 'Sao Tome and Principe')
        case "sc":
            countrytest_statistics_command_handler(call.message, 'Seychelles')
        case "sn":
            countrytest_statistics_command_handler(call.message, 'Senegal')
        case "so":
            countrytest_statistics_command_handler(call.message, 'Somalia')
        case "sd":
            countrytest_statistics_command_handler(call.message, 'Sudan')
        case "sl":
            countrytest_statistics_command_handler(call.message, 'Sierra-Leone')
        case "tz":
            countrytest_statistics_command_handler(call.message, 'Tanzania')
        case "tg":
            countrytest_statistics_command_handler(call.message, 'Togo')
        case "tn":
            countrytest_statistics_command_handler(call.message, 'Tunisia')
        case "ug":
            countrytest_statistics_command_handler(call.message, 'Uganda')
        case "cf":
            countrytest_statistics_command_handler(call.message, 'Central African Republic')
        case "td":
            countrytest_statistics_command_handler(call.message, 'Chad')
        case "bm":
            countrytest_statistics_command_handler(call.message, 'Bermuda')
        case "gl":
            countrytest_statistics_command_handler(call.message, 'Greenland')
        case "ca":
            countrytest_statistics_command_handler(call.message, 'Canada')
        case "mx":
            countrytest_statistics_command_handler(call.message, 'Mexico')
        case "usa":
            countrytest_statistics_command_handler(call.message, 'usa')
        case "bz":
            countrytest_statistics_command_handler(call.message, 'Belize')
        case "gt":
            countrytest_statistics_command_handler(call.message, 'Guatemala')
        case "hn":
            countrytest_statistics_command_handler(call.message, 'Honduras')
        case "cr":
            countrytest_statistics_command_handler(call.message, 'Costa-Rica')
        case "ni":
            countrytest_statistics_command_handler(call.message, 'Nicaragua')
        case "pa":
            countrytest_statistics_command_handler(call.message, 'Panama')
        case "sv":
            countrytest_statistics_command_handler(call.message, 'El-Salvador')
        case "ag":
            countrytest_statistics_command_handler(call.message, 'Antigua-and-Barbuda')
        case "aw":
            countrytest_statistics_command_handler(call.message, 'Aruba')
        case "bs":
            countrytest_statistics_command_handler(call.message, 'Bahamas')
        case "bb":
            countrytest_statistics_command_handler(call.message, 'Barbados')
        case "bq":
            countrytest_statistics_command_handler(call.message, 'Bonaire')
        case "vg":
            countrytest_statistics_command_handler(call.message, 'Virgin-Islands')
        case "ht":
            countrytest_statistics_command_handler(call.message, 'Haiti')
        case "gp":
            countrytest_statistics_command_handler(call.message, 'Guadeloupe')
        case "gd":
            countrytest_statistics_command_handler(call.message, 'Grenada')
        case "dm":
            countrytest_statistics_command_handler(call.message, 'Dominica')
        case "do":
            countrytest_statistics_command_handler(call.message, 'Dominican-Republic')
        case "ky":
            countrytest_statistics_command_handler(call.message, 'Cayman-Islands')
        case "cu":
            countrytest_statistics_command_handler(call.message, 'Cuba')
        case "cw":
            countrytest_statistics_command_handler(call.message, 'Curaçao')
        case "mq":
            countrytest_statistics_command_handler(call.message, 'Martinique')
        case "ms":
            countrytest_statistics_command_handler(call.message, 'Montserrat')
        case "tc":
            countrytest_statistics_command_handler(call.message, 'Turks-and-Caicos-Islands')
        case "pr":
            countrytest_statistics_command_handler(call.message, 'Puerto Rico')
        case "jm":
            countrytest_statistics_command_handler(call.message, 'Jamaica')
        case "lc":
            countrytest_statistics_command_handler(call.message, 'Saint-Lucia')
        case "au":
            countrytest_statistics_command_handler(call.message, 'Australia')
        case "vu":
            countrytest_statistics_command_handler(call.message, 'Vanuatu')
        case "pg":
            countrytest_statistics_command_handler(call.message, 'Papua New Guinea')
        case "sb":
            countrytest_statistics_command_handler(call.message, 'Solomon-Islands')
        case "fj":
            countrytest_statistics_command_handler(call.message, 'Fiji')
        case "ki":
            countrytest_statistics_command_handler(call.message, 'Kiribati')
        case "mh":
            countrytest_statistics_command_handler(call.message, 'Marshall-Islands')
        case "nr":
            countrytest_statistics_command_handler(call.message, 'Nauru')
        case "nz":
            countrytest_statistics_command_handler(call.message, 'New Zealand')
        case "pw":
            countrytest_statistics_command_handler(call.message, 'Palau')
        case "ws":
            countrytest_statistics_command_handler(call.message, 'Samoa')
        case "to":
            countrytest_statistics_command_handler(call.message, 'Tonga')
        case "tv":
            countrytest_statistics_command_handler(call.message, 'Tuvalu')
        case "fm":
            countrytest_statistics_command_handler(call.message, 'Micronesia')


@bot.message_handler(commands=['countrylocationsend'])
@send_action('typing')
@save_user_activity()
def countryLocationSend_command_handler(message):
    cid = message.chat.id
    markup1 = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text='Відправити свою геопозицію', request_location=True)
    markup1.add(button_geo)
    bot.send_message(cid, 'Будь ласка, виберіть команди з меню', reply_markup=markup1)


# geo command handler
@bot.message_handler(content_types=['location'])
@send_action('typing')
@save_user_activity()
def geo_command_handler(message):
    cid = message.chat.id
    geo_result = country_service.get_country_information(message.location.latitude, message.location.longitude)
    statistics = stats_service.get_statistics_by_country_name(geo_result['countryName'], message.chat.username)
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')

# country statistics command handler
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
@send_action('typing')
@save_user_activity()
def country_statistics_command_handler(message):
    country_name = message.text.strip()
    cid = message.chat.id
    try:
        statistics = stats_service.get_statistics_by_country_name(country_name, message.chat.username)
    except Exception as e:
        raise e
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')

@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
@send_action('typing')
@save_user_activity()
def countrytest_statistics_command_handler(message, country_name):
    cid = message.chat.id
    try:
        statistics = stats_service.get_statistics_by_country_name(country_name, message.chat.username)
    except Exception as e:
        raise e
    user_steps[cid] = 0
    bot.send_message(cid, statistics, parse_mode='HTML')


# query statistics command handler
@bot.message_handler(commands=['statistics'])
@send_action('typing')
@save_user_activity()
def statistics_command_handler(message):
    cid = message.chat.id
    bot.send_message(cid, stats_service.get_statistics_of_users_queries(), parse_mode='HTML')


# contacts command handler
@bot.message_handler(commands=['contacts'])
@send_action('typing')
@save_user_activity()
def contacts_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/contacts.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
        bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')

#######################


#################################

# help command handler
@bot.message_handler(commands=['help'])
@send_action('typing')
@save_user_activity()
def help_command_handler(message):
    cid = message.chat.id
    help_text = 'The following commands are available \n'
    for key in commands:
        help_text += '/' + key + ': '
        help_text += commands[key] + '\n'
    help_text += 'ANTI_COVID_19_BOT speaks english, be careful and take care'
    bot.send_message(cid, help_text)


# hi command handler
@bot.message_handler(func=lambda message: message.text.lower() == 'hi')
@send_action('typing')
@save_user_activity()
def hi_command_handler(message):
    cid = message.chat.id
    with codecs.open('templates/himydear.html', 'r', encoding='UTF-8') as file:
        template = Template(file.read())
        bot.send_message(cid, template.render(user_name=message.chat.username), parse_mode='HTML')


# default text messages and hidden statistics command handler
@bot.message_handler(func=lambda message: True, content_types=['text'])
@send_action('typing')
@save_user_activity()
def default_command_handler(message):
    cid = message.chat.id
    if message.text[:int(os.getenv('PASS_CHAR_COUNT'))] == os.getenv('STAT_KEY'):
        st = message.text.split(' ')
        if 'txt' in st:
            tga.analysis(st, cid)
            with codecs.open('%s.txt' % cid, 'r', encoding='UTF-8') as file:
                bot.send_document(cid, file)
                tga.remove(cid)
        else:
            messages = tga.analysis(st, cid)
            bot.send_message(cid, messages)
    else:
        with codecs.open('templates/idunnocommand.html', 'r', encoding='UTF-8') as file:
            template = Template(file.read())
            bot.send_message(cid, template.render(text_command=message.text), parse_mode='HTML')

 #set web hook

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
