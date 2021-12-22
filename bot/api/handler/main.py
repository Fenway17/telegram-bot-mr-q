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

NAME_RESPONSE, LIMIT = range(2)
eventInfo = []

##################################################
             # Command Functions #
##################################################
def start_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    username = update.message.from_user
    
    bot_welcome = """
        Hello {}! Welcome to version {} of QueueNow!\n
Use /newqueue to start a new queue!
Use /checkqueues to check your current queues!
Use /help to show more commands!
        """.format(username['first_name'], version)
    
    context.bot.sendChatAction(chat_id=chat_id, action="typing")
    update.message.reply_text(text=bot_welcome, reply_to_message_id=msg_id)

def help_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    bot_help = """These are the list of commands you can use! \n
/start : start the bot
/newqueue : create a new queue
/checkqueues : check the queues you are in or manage"""
    
    context.bot.sendChatAction(chat_id=chat_id, action="typing")
    update.message.reply_text(text=bot_help, reply_to_message_id=msg_id)
    
def newqueue_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    username = update.message.from_user

    reply = "Hello {}! Let's start off with the name of your event! ".format(username['first_name'])
    
    context.bot.sendChatAction(chat_id=chat_id, action="typing")
    update.message.reply_text(text="{}".format(reply), reply_to_message_id=msg_id)
    
    return NAME_RESPONSE


def name_response(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    name = update.message.text
    eventInfo.append(name)
    
    context.bot.sendChatAction(chat_id=chat_id, action="typing")
    update.message.reply_text("""{}? Sounds like it's going to be a lit event!\n
So how many people are you expecting for {}?""".format(name, name))

    return LIMIT

def limit_command(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    eventLimit = update.message.text
    
    try: # test if given message is a whole number
        eventLimitInt = int(eventLimit)
        eventLimit = str(eventLimitInt) # prevent users from giving a float number
        eventInfo.append(eventLimit)
        context.bot.sendChatAction(chat_id=chat_id, action="typing")
        update.message.reply_text("Ogie, setting event limit to {}".format(eventLimit))
        
        keyboard = [
            [InlineKeyboardButton("Publish Poll", callback_data='publish_poll')], 
            [InlineKeyboardButton("Update Poll", callback_data='update_poll'),
                InlineKeyboardButton("Delete Poll", callback_data='delete_poll')],
            [InlineKeyboardButton("I'm going!", callback_data='enqueue'),
                InlineKeyboardButton("I'm not going!", callback_data='dequeue')]
        ]

        queueTemplate = "{}\n\nI'm going! (Max Limit: {} pax)\n\nWaiting List: \n".format(eventInfo[0], eventInfo[1])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.sendChatAction(chat_id=chat_id, action="typing")
        update.message.reply_text( 
            text=queueTemplate, 
            reply_to_message_id=msg_id, 
            reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as e:
        context.bot.sendChatAction(chat_id=chat_id, action="typing")
        update.message.reply_text("Sorry, please give me a whole number!".format(eventLimit))
        print(e)
        return LIMIT
    

def checkqueues_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    keyboard = [
            [InlineKeyboardButton("Queues I'm in", callback_data='queues_in')],
            [InlineKeyboardButton("Queues I manage", callback_data='queues_manage')],
        ]
    
    bot_check_queue = "Which queues do you want?"
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.sendChatAction(chat_id=chat_id, action="typing")
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

    context.bot.sendChatAction(chat_id=chat_id, action="typing")
    update.message.reply_text(response)

def handle_callback_query(update, context):
    # TODO: separate this function into multiple functions to handle the different callbacks queries - yr
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    callback_data = update.callback_query.data
    user_id = str(update.callback_query.from_user.id)
    query_id = update.callback_query.id

    if callback_data == 'queues_in':
        # TODO: call backend to retrieve queues user is participating in - yr
        context.bot.sendChatAction(chat_id=chat_id, action="typing")
        context.bot.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        context.bot.sendMessage(
            chat_id=chat_id, 
            text="""Here are your queues: \n\nQueue 1 \nQueue 2""")
    elif callback_data == 'queues_manage':
        # TODO: call backend to retrieve queues user is managing (aka admin) - yr
        context.bot.sendChatAction(chat_id=chat_id, action="typing")
        context.bot.answerCallbackQuery(text='Here are your queues!', callback_query_id=query_id)
        context.bot.sendMessage(
            chat_id=chat_id, 
            text="""Here are your queues: \n\nQueue 1 \nQueue 2""")
    else:
        context.bot.answerCallbackQuery(text='Invalid data!', callback_query_id=query_id)


##############################################
            # TODO for integration
##############################################

def hcq_publish(update, context): 
    pass

def hcq_update(update, context):     
    pass

def hcq_delete(update, context): 
    pass

def hcq_enqueue(update, context): 
    pass

def hcq_dequeue(update, context): 
    pass

def handle_inline_query(update, context):
    # TODO: handle inline query if there is any we add in the future - yr
    # chat and message IDs
    chat_id = update.inline_query.message.chat.id
    msg_id = update.inline_query.message.message_id
    inline_query = update.inline_query
    text = inline_query.query.lower()
    user_id = str(inline_query.from_user.id)

##################################################
              # Static Functions #
##################################################
def setMyCommands():
    # sets command suggestions for the bot
    # bot commands
    BOT_COMMANDS = [
        {"command":"/start", "description":"Starts the bot!"},
        {"command":"/newqueue","description":"Create a new queue!"},
        {"command":"/checkqueues","description":"Checks your queues!"},
        {"command":"/help","description":"Shows you the commands!"}
        ]

    send_text = 'https://api.telegram.org/bot' + str(BOT_KEY) + '/setMyCommands?commands=' + str(json.dumps(BOT_COMMANDS) ) 
    response = requests.get(send_text)
    
def error(update, context):
    print(f"Update {update} caused error {context.error}")

##################################################
               # Main Function #
##################################################
def main():
    # runs the bot setup
    updater = Updater(os.getenv('BOT_KEY'), use_context=True)
    dp = updater.dispatcher

    # main state handler
    convo_handler = ConversationHandler(
        entry_points=[CommandHandler('newqueue', newqueue_command)],
        states = {
            NAME_RESPONSE: [MessageHandler(Filters.text, name_response)],
            LIMIT: [MessageHandler(Filters.text, limit_command)]
        },
        fallbacks=[],
    )
    # command handlers
    dp.add_handler(convo_handler)
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('checkqueues', checkqueues_command))
    
    # callback query handlers
    dp.add_handler(CallbackQueryHandler(hcq_publish, pattern='publish_poll'))
    dp.add_handler(CallbackQueryHandler(hcq_update, pattern='update_poll'))
    dp.add_handler(CallbackQueryHandler(hcq_delete, pattern='delete_poll'))
    dp.add_handler(CallbackQueryHandler(hcq_enqueue, pattern='enqueue'))
    dp.add_handler(CallbackQueryHandler(hcq_dequeue, pattern='dequeue'))
    
    # other handlers
    # dp.add_handler(MessageHandler(Filters.text, help_command)) # sends help command for any random message
    dp.add_error_handler(error)
    
    setMyCommands()
    
    print('Bot Started....')
    updater.start_polling()
    updater.idle()