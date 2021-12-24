import os, time, json, requests, re
import datetime 
from telegram.ext import *
from telegram import *
# from ..service import event as Event, user as User, main as EventManager

# global bot key
BOT_KEY = os.getenv('BOT_KEY') # reads .env file from your root folder of this bot

# global strings to use in bot replies
version = "0.1.0"

# conversation handler constants
NAME_RESPONSE, LIMIT = range(2)
QUEUES_IN, QUEUES_MANAGE = range(2)


eventInfo = []

##################################################
             # Command Functions #
##################################################
def start_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    user = update.message.from_user
    first_name = user['first_name']
    
    bot_welcome = """
        Hello {}! \n\nWelcome to version {} of QueueNow!\n
Use /newqueue to start a new queue!
Use /checkqueues to check your current queues!
Use /help to show more commands!
        """.format(first_name, version)
    
    update.message.reply_text(text=bot_welcome)

def help_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    bot_help = """These are the list of commands you can use! \n
/start : start the bot
/newqueue : create a new queue
/checkqueues : check the queues you are in or manage"""
    
    update.message.reply_text(text=bot_help)
    
def newqueue_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    user = update.message.from_user

    reply = "Alrighty! Let's start with the name of your event! "
    
    update.message.reply_text(text="{}".format(reply))
    
    return NAME_RESPONSE

def name_response(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    event_name = update.message.text
    eventInfo.append(event_name)
    
    update.message.reply_text("""{}? Sounds like it's going to be a lit event!\n
So how many people are you expecting for {}?""".format(event_name, event_name))

    return LIMIT

def limit_command(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    eventLimit = update.message.text
    
    try: # test if given message is a whole number
        eventLimitInt = int(eventLimit)
        eventLimit = str(eventLimitInt) # prevent users from giving a float number
        eventInfo.append(eventLimit)
        
        keyboard = [
            [InlineKeyboardButton("Publish Poll", switch_inline_query='PLACEHOLDER')], 
            [InlineKeyboardButton("Update Poll", callback_data='update_poll'),
                InlineKeyboardButton("Delete Poll", callback_data='delete_poll')],
            [InlineKeyboardButton("I'm going!", callback_data='enqueue'),
                InlineKeyboardButton("I'm not going!", callback_data='dequeue')]
        ]

        # TODO: standardize format of showing queue
        queueTemplate = "{}\n\nI'm going! (Max Limit: {} pax)\n\nWaiting List: \n".format(eventInfo[0], eventInfo[1])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text("Ogie, setting event limit to {}".format(eventLimit))
        update.message.reply_text( 
            text=queueTemplate, 
            reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as ex:
        update.message.reply_text("Sorry, please give me a whole number!")
        print(ex)
        return LIMIT

def checkqueues_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    keyboard = [
            ["Queues I'm participating in!"],
            ["Queues I'm managing!"],
        ]
    
    bot_check_queue = "Which queues do you want to check?"
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True) 
    
    update.message.reply_text( 
        text=bot_check_queue, 
        reply_markup=reply_markup)
    
def handle_message(update, context):
    # currently not in use - yr
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    text = str(update.message.text).lower()
    response = "test"

    update.message.reply_text(response)

# def handle_callback_query(update, context):
#     # not needed for current iteration - yr
#     chat_id = update.callback_query.message.chat.id
#     msg_id = update.callback_query.message.message_id
#     callback_data = update.callback_query.data
#     user_id = str(update.callback_query.from_user.id)
#     query_id = update.callback_query.id

#     context.bot.answerCallbackQuery(text='Invalid data!', callback_query_id=query_id)

##############################################
            # TODO for integration
##############################################

def hcq_update(update, context):     
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    
    # TODO: get bot to fetch the current queue and edit the message to show the updated queue
    context.bot.answerCallbackQuery(text='Placeholder', callback_query_id=query_id)

def hcq_delete(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id

    # TODO: get bot to delete queue
    context.bot.answerCallbackQuery(text='Placeholder', callback_query_id=query_id)
    
def hcq_enqueue(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    
    # TODO: add user to queue
    context.bot.answerCallbackQuery(text='Placeholder', callback_query_id=query_id)
    
def hcq_dequeue(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    
    # TODO: remove user from queue
    context.bot.answerCallbackQuery(text='Placeholder', callback_query_id=query_id)
    
def check_queues_in(update, context): 
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    # TODO: get bot to fetch the queues and show the queue
    # TODO: call backend to retrieve queues user is participating in - yr
    context.bot.sendMessage(
        chat_id=chat_id, 
        text="""Here are your queues: \n\n1. Queue 1 \n2. Queue 2""")
    context.bot.sendMessage(chat_id=chat_id, text="Send me the queue number you want to check!")
    
    return QUEUES_IN

def check_queues_manage(update, context): 
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    # TODO: get bot to fetch the queues and show the queue
    # TODO: call backend to retrieve queues user is managing (aka admin) - yr
    context.bot.sendMessage(
        chat_id=chat_id, 
        text="""Here are your queues: \n\n1. Queue 1 \n2. Queue 2""")
    context.bot.sendMessage(chat_id=chat_id, text="Send me the queue number you want to check!")
    
    return QUEUES_MANAGE

def display_queues_in(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    selected_queue = update.message.text
    
    try:
        selected_queue = int(selected_queue)
        keyboard = [ 
            [InlineKeyboardButton("I'm not going anymore!", callback_data='dequeue')],
            [InlineKeyboardButton("Update queue", callback_data='update_poll')]
        ]

        # TODO: standardize format of showing queue
        queueTemplate = "Queue {}\n\nI'm going! (Max Limit: {} pax)\n\nWaiting List: \n".format(selected_queue, "69")
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text( 
            text=queueTemplate, 
            reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as e: 
        update.message.reply_text("Sorry, please give me a whole number!")
        print(e)
        return QUEUES_IN
    
    
def display_queues_manage(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    selected_queue = update.message.text
    
    try:
        selected_queue = int(selected_queue)
        keyboard = [ 
            [InlineKeyboardButton("I'm not going anymore!", callback_data='dequeue')],
            [InlineKeyboardButton("Update queue", callback_data='update_poll')]
        ]

        # TODO: standardize format of showing queue
        queueTemplate = "Queue {}\n\nI'm going! (Max Limit: {} pax)\n\nWaiting List: \n".format(selected_queue, "69")
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text( 
            text=queueTemplate, 
            reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as e: 
        update.message.reply_text("Sorry, please give me a whole number!")
        print(e)
        return QUEUES_MANAGE
    
def handle_inline_query(update, context):
    query_id = update.inline_query.id
    inline_query = update.inline_query
    text = inline_query.query.lower()
    user_id = str(inline_query.from_user.id)

    if text == "": # user input nothing
        return
    
    # TODO: handle inline query
    results = [
        InlineQueryResultArticle(
            id="PLACEHOLDER",
            title="EVENTNAMEPLACEHOLDER",
            input_message_content=InputTextMessageContent("CONTENTPLACEHOLDER"),
        ),
    ]

    context.bot.answerInlineQuery(inline_query_id=query_id, results=results)
    
##################################################
           # Static Helper Functions #
##################################################
def build_queue_message(event):
    # fetch variables
    event_id = event.id
    event_name = event.name
    event_date = event.date
    event_time = event.time 
    event_participants = event.participants_list
    event_participants_max = str(event.participants_limit)
    event_waiting = event.waiting_list
    
    participants = ""
    waiting = ""
    participants_count = 0
    waiting_count = 0
    for person in event_participants:
        name = person.name
        participants.append(name + "\n")
        participants_count += 1
    
    for person in event_waiting:
        name = person.name
        waiting.append(name + "\n")
        waiting_count += 1
    
    message_content = """
{}\n
Participating! ({}/{} people)
{}\n
Waiting! ({} people)
{}\n
""".format(event_name, str(participants_count), event_participants_max, participants, str(waiting_count), waiting)
    
    return message_content

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

    # newqueue conversation handler
    newqueue_convo_handler = ConversationHandler(
        entry_points=[CommandHandler('newqueue', newqueue_command)],
        states = {
            NAME_RESPONSE: [MessageHandler(Filters.text, name_response)],
            LIMIT: [MessageHandler(Filters.text, limit_command)]
        },
        fallbacks=[],
    )
    
    # checkqueue conversation handler
    checkqueue_convo_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(re.compile('Queues I\'m in', re.IGNORECASE)), check_queues_in),
            MessageHandler(Filters.regex(re.compile('Queues I manage', re.IGNORECASE)), check_queues_in)],
        states = {
            QUEUES_IN: [MessageHandler(Filters.text, display_queues_in)],
            QUEUES_MANAGE: [MessageHandler(Filters.text, display_queues_manage)]
        },
        fallbacks=[],
    )
    
    # command handlers
    dp.add_handler(newqueue_convo_handler)
    dp.add_handler(checkqueue_convo_handler)
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('checkqueues', checkqueues_command))
    dp.add_handler(CommandHandler('help', help_command))
    
    # callback query handlers
    dp.add_handler(CallbackQueryHandler(hcq_update, pattern='update_poll'))
    dp.add_handler(CallbackQueryHandler(hcq_delete, pattern='delete_poll'))
    dp.add_handler(CallbackQueryHandler(hcq_enqueue, pattern='enqueue'))
    dp.add_handler(CallbackQueryHandler(hcq_dequeue, pattern='dequeue'))
    # dp.add_handler(CallbackQueryHandler(hcq_check_queues_in, pattern='queues_in'))
    # dp.add_handler(CallbackQueryHandler(hcq_check_queues_manage, pattern='queues_manage'))

    # inline query handlers
    dp.add_handler(InlineQueryHandler(handle_inline_query))
    
    # other handlers
    dp.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.command, help_command))
    # dp.add_handler(MessageHandler(Filters.text & (~Filters.command), help_command))
    
    setMyCommands()
    
    ############# FOR TESTING ##################################################
    # e = EventManager.EventManager()
    ############################################################################
    
    print('Bot Started....')
    updater.start_polling()
    updater.idle()