import telebot
from Config import TOKEN, keys
from extensions import ConvertionExpetion, CryptoConverter

bot = telebot.TeleBot(TOKEN)


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Для начала работы введите команду боту в формате <имя валюты цену которой он хочет узнать> \
<имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def value_info(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionExpetion('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExpetion as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()
