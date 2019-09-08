from subprocess import call
from collections import deque

from telegram.ext import Updater
from telegram.ext import CommandHandler

from config import *  # Leemos la configuracion

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, see /help for help!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def tail(update, context):
    """Mira las n ultimas lineas del archivo log_file"""
    if context.args:
        n = int(context.args[0])
        if n > 20:  # No permitimos n muy grandes
            n = 20
    else:
        n = 5
    with open(log_file, 'r') as f:
        last_lines = list(deque(f, maxlen=n))
    text_tail = '\n'.join(last_lines)
    context.bot.send_message(chat_id=update.message.chat_id, text=text_tail)

tail_handler = CommandHandler('tail', tail)
dispatcher.add_handler(tail_handler)

def is_running(update, context):
    """Chequea si esta corriendo cmd_name"""
    stat = call(["ps", "-C", cmd_name])
    text_is_running = f"Is running: {stat == 0}"
    context.bot.send_message(chat_id=update.message.chat_id, text=text_is_running)

is_running_handler = CommandHandler('is_running', is_running)
dispatcher.add_handler(is_running_handler)

def help(update, context):
    """Mustra la ayuda del boot"""
    text_help = """Bot para seguir una corrida larga de un programa.

    /tail n - Muestra las ultimas n lineas del log. Por defecto 5, maximo 20.
    /is_running - Comprueba si sigue corriendo."""
    context.bot.send_message(chat_id=update.message.chat_id, text=text_help)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

updater.start_polling()
