from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
import datetime as dt
import time
from SignalDetection import *


updater = Updater(token='1765200872:AAFqsN4-tXoDrX3RssYn2IUFlGWZ8xcjRAg', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="TempoQuant v1.0.0 launched. Auto scanning signals.")
    while True:
        h = dt.datetime.now().hour
        mi = dt.datetime.now().minute
        wd = dt.datetime.now().weekday()
        
        if wd in range(5) and h == 18 and mi == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text= "Auto updating watch list...")
            out = updateWatchList(significance=1.5, life=30)
            context.bot.send_message(chat_id=update.effective_chat.id, text= out)
        if wd in range(5) and h in range(9,16):
            for out in alert(tolerance=0.005):
                context.bot.send_message(chat_id=update.effective_chat.id, text= out)
            time.sleep(30)

def updateWL(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Auto updating watch list...")
    out = updateWatchList(significance=1.5, life=30)
    context.bot.send_message(chat_id=update.effective_chat.id, text= out)


def testAlert(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Testing alert pipeline...")
    for out in alert(tolerance=0.005):
        context.bot.send_message(chat_id=update.effective_chat.id, text= out)
    time.sleep(5)
    context.bot.send_message(chat_id=update.effective_chat.id, text= "Test Complete.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
update_handler = CommandHandler('update', updateWL)
dispatcher.add_handler(update_handler)
test_handler = CommandHandler('test', testAlert)
dispatcher.add_handler(test_handler)

updater.start_polling()