import telebot
from config import keys, TOKEN
from extensions import APIException, ExchangeConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_info(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: ' \
           '\n<название валюты> <в какую валюту перевести> <сумма перевода>' \
           '\nУвидеть список всех достпуных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        base, quote, amount = values
        total_quote = ExchangeConverter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Бот не может обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {round((total_quote * float(amount)), 2)}'
        bot.send_message(message.chat.id, text)

bot.polling()

