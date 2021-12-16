import os
import time
from flask import Blueprint, request
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot_handler = Blueprint('bot', __name__)
BOT_KEY = os.getenv('5024320262:AAEAa5rcSXHaYYC4RqfbbSkK5ycVr4Hfu6w') # reads .env file from your root folder of this bot
bot = telegram.Bot(token='5024320262:AAEAa5rcSXHaYYC4RqfbbSkK5ycVr4Hfu6w')

# global strings to use in bot replies
version = "0.1.0"
bot_welcome = """
    Welcome to version {0} of QueueNow! \n
    Use /newqueue to start a new queue!
    """.format(version)
bot_error = "The command was not recognized, try a different one!"
bot_help = """These are the list of commands you can use! \n
    /start : start the bot \n
    /newqueue : create a new queue \n
    /checkqueues : check the queues you are in or manage \n
    """
bot_new_queue = "Give me a name for your new queue!"
bot_check_queue = "Which queues do you want?"

# global variables
typing_duration = 0.5

@bot_handler.route('/{}'.format(BOT_KEY), methods=['POST', 'GET']) # access this via BOT KEY
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot) 
    # TODO: check if this works properly 
    
    # figure out which type of query given
    if update.message:
        respond_message(update)
        
    elif update.callback_query:
        respond_callback_query(update)
        
    elif update.inline_query:
        respond_inline_query(update)
        
async def respond_message(update: telegram.Update):
    
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    # if no text, it is not a message to respond to
    if not update.message.text:
            return
    
    # force text message to conform to UTF8 (may not be needed)
    text = update.message.text.encode('utf-8').decode()


    # check command
    if text == "/start":
       bot.sendChatAction(chat_id=chat_id, action="typing")
       time.sleep(typing_duration)
       update.message.reply_text(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
       
    elif text == "/newqueue":
        bot.sendChatAction(chat_id=chat_id, action="typing")
        time.sleep(typing_duration)
        update.message.reply_text(chat_id=chat_id, text=bot_new_queue, reply_to_message_id=msg_id)
        
    elif text == "/checkqueues":
        bot.sendChatAction(chat_id=chat_id, action="typing")
        time.sleep(typing_duration)
        
        keyboard = [
            [InlineKeyboardButton("Queues I'm in", callback_data='queues_in')],
            [InlineKeyboardButton("Queues I manage", callback_data='queues_manage')],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            chat_id=chat_id, 
            text=bot_check_queue, 
            reply_to_message_id=msg_id, 
            reply_markup=reply_markup,
            one_time_keyboard=True)
        
    elif text == "/help":
        bot.sendChatAction(chat_id=chat_id, action="typing")
        time.sleep(typing_duration)
        bot.sendMessage(chat_id=chat_id, text=bot_help, reply_to_message_id=msg_id)
        
    else:
        bot.sendChatAction(chat_id=chat_id, action="typing")
        time.sleep(typing_duration)
        bot.sendMessage(chat_id=chat_id, text=bot_error, reply_to_message_id=msg_id)
        
    return "Bot Handler is working"

async def respond_callback_query(update: telegram.Update):
    # TODO: handle the callbacks from inline keyboard
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    callback_data = update.callback_query.data
    user_id = str(update.callback_query.from_user.id)
    query_id = update.callback_query.id
    
    if callback_data == 'queues_in':
        # TODO: call backend to retrieve queues user is participating in
        update.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        pass
    elif callback_data == 'queues_manage':
        # TODO: call backend to retrieve queues user is managing (aka admin)
        update.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        pass
    else:
        update.answerCallbackQuery(text='Invalid data!', callback_query_id=query_id)
        
    
async def respond_inline_query(update: telegram.Update):
    # TODO: handle inline query if there is any we add in the future
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    inline_query = update.inline_query
    text = inline_query.query.lower()
    user_id = str(inline_query.from_user.id)