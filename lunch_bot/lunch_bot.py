import random
import configparser
import redis

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('../config.ini')
db = redis.Redis(host='redis')


def get_redis():
    return db


def get_places(update):
    db = get_redis()
    places = db.smembers(update.message.chat_id)
    return tuple(map(lambda x: x.decode('utf-8'), places))


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
    places = get_places(update)
    #logger.info(update.message.chat_id)
    update.message.reply_text(random.choice(places))

def list_handler(bot, update):
    #logger.info(places)
    update.message.reply_text('\n'.join(get_places(update)))

def add(bot, update, **args):
    db = get_redis()
    key = update.message.chat_id
    if not args or not args['args'] or len(args['args']) == 0:
        update.message.reply_text('Нужно задать имя местечка, например, так: "/add Кафе у Армена"')
        return

    new_place = ' '.join(args['args'])
    db.sadd(key, new_place)
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

