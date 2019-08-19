import random
import configparser

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging


places = ['KFC', 'Шаверма на Чкаловском', 'Китайцы', 'Корейцы', 'Итальянское место, где тупят официанты',
          'Макдональдс. Илья, привет!', 'Кетчап', 'Чито гврито']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('config.ini')


def start(bot, update):
    update.message.reply_text('Не можешь выбрать, куда сходить поесть? Пиши /roll')


def help(bot, update):
    update.message.reply_text("""\
Как пользоваться:
     /help                     Вывести это сообщение
     /roll                     Выбрать место для ланча
     /list                     Вывести весь список мест
     /add <место>              Добавить место
""")


def roll(bot, update):
    # print(update.message.chat_id)
    # print(bot.get_chat(update.message.chat_id))
    update.message.reply_text(random.choice(places))

def list_handler(bot, update):
    update.message.reply_text('\n'.join(places))

def add(bot, update, **args):
    if not args or not args['args'] or len(args['args']) == 0:
        update.message.reply_text('Нужно задать имя местечка, например, так: "/add Кафе у Армена"')
        return

    new_place = ' '.join(args['args'])
    places.append(new_place)
    update.message.reply_text('Местечко "' + new_place + '" добавлено')

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    updater = Updater(config['BOT']['Token'])

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("roll", roll))
    dp.add_handler(CommandHandler("list", list_handler))
    dp.add_handler(CommandHandler("add", add, pass_args=True))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

