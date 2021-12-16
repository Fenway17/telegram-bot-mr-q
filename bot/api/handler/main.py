import os
import time
import json
import requests
from telegram.ext import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# global bot key
BOT_KEY = os.getenv('BOT_KEY') # reads .env file from your root folder of this bot

# global strings to use in bot replies
version = "0.1.0"
bot_welcome = """
    Welcome to version {0} of QueueNow! \n
    Use /newqueue to start a new queue!
    """.format(version)

bot_error = "The command was not recognized, try a different one!"
bot_help = """These are the list of commands you can use! \n
    /start : start the bot
    /newqueue : create a new queue
    /checkqueues : check the queues you are in or manage
    """
bot_new_queue = "Give me a name for your new queue!"
bot_check_queue = "Which queues do you want?"

# global variables
typing_duration = 0.3

# bot commands
BOT_COMMANDS = [
    {"command":"/start", "description":"Starts the bot!"},
    {"command":"/help","description":"Gets you some help!"},
    {"command":"/newqueue","description":"Create a new queue!"},
    {"command":"/checkqueues","description":"Checks your queues!"}
    ]

def setMyCommands():
    # sets command suggestions for the bot
    # TODO: literally does not work right now - yr
    send_text = 'https://api.telegram.org/bot' + str(BOT_KEY) + '/setMyCommands?commands=' + str(json.dumps(BOT_COMMANDS) ) 
    response = requests.get(send_text)
   
def start_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    context.bot.send_chat_action(chat_id=chat_id, action="typing", timeout=1)
    time.sleep(typing_duration)
    update.message.reply_text(text=bot_welcome, reply_to_message_id=msg_id)

def help_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    context.bot.send_chat_action(chat_id=chat_id, action="typing", timeout=1)
    time.sleep(typing_duration)
    update.message.reply_text(text=bot_help, reply_to_message_id=msg_id)

def newqueue_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    context.bot.send_chat_action(chat_id=chat_id, action="typing", timeout=1)
    time.sleep(typing_duration)
    update.message.reply_text(text=bot_new_queue, reply_to_message_id=msg_id)
    
def checkqueues_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    keyboard = [
            [InlineKeyboardButton("Queues I'm in", callback_data='queues_in')],
            [InlineKeyboardButton("Queues I manage", callback_data='queues_manage')],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_chat_action(chat_id=chat_id, action="typing", timeout=1)
    time.sleep(typing_duration)
    update.message.reply_text( 
        text=bot_check_queue, 
        reply_to_message_id=msg_id, 
        reply_markup=reply_markup)
    
def handle_message(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    text = str(update.message.text).lower()
    response = "test"

    update.message.reply_text(response)

def handle_callback_query(update, context):
    # TODO: handle the callbacks from inline keyboard - yr
    # chat and message IDs
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    callback_data = update.callback_query.data
    user_id = str(update.callback_query.from_user.id)
    query_id = update.callback_query.id
    
    if callback_data == 'queues_in':
        # TODO: call backend to retrieve queues user is participating in - yr
        context.bot.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        pass
    elif callback_data == 'queues_manage':
        # TODO: call backend to retrieve queues user is managing (aka admin) - yr
        context.bot.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        pass
    else:
        context.bot.answerCallbackQuery(text='Invalid data!', callback_query_id=query_id)
        
    
def handle_inline_query(update, context):
    # TODO: handle inline query if there is any we add in the future - yr
    # chat and message IDs
    chat_id = update.inline_query.message.chat.id
    msg_id = update.inline_query.message.message_id
    inline_query = update.inline_query
    text = inline_query.query.lower()
    user_id = str(inline_query.from_user.id)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(os.getenv('BOT_KEY'), use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("newqueue", newqueue_command))
    dp.add_handler(CommandHandler("checkqueues", checkqueues_command))
    
    dp.add_handler(MessageHandler(Filters.text, help_command))
    
    dp.add_error_handler(error)
    
    setMyCommands()
    
    print('Bot Started....')
    updater.start_polling()
    updater.idle()