import telebot
from config import currencies, TOKEN
from extensions import ConvertException, CurrencyConvertor


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    if message.text == '/start':
        text = f'Приветствую, {message.from_user.first_name}!\n \
Для начала работы введите команду в следующем формате:\n \
<название валюты>\n \
<название валюты в которую нужно конвертировать>\n \
<количество валюты для конвертации>.\n \
Примечание: данные вводить в одну строку через пробел\n \
Увидеть список доступных валют: /values'
        bot.reply_to(message, text)
    else:
        text = 'Для начала работы введите команду в следующем формате:\n \
<название валюты>\n \
<название валюты в которую нужно конвертировать>\n \
<количество валюты для конвертации>.\n \
Примечание: данные вводить в одну строку через пробел\n \
Увидеть список доступных валют: /values'
        bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key.title()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        elements = message.text.split()

        if len(elements) != 3:
            raise ConvertException('Неверное количество параметров!')

        base, sym, amount = elements
        total_base = CurrencyConvertor.get_price(base, sym, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')
    else:
        text = f'Цена {amount} {base.lower()} в {sym.lower()} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
