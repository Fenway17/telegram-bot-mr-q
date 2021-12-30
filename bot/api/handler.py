import os, time, json, requests, re
from datetime import datetime as date
from telegram import user
from telegram.ext import *
from telegram import *
from .service.eventmanager import EventManager
from .service.model.event import Event
from .service.model.user import User

# global bot key
BOT_KEY = os.getenv('BOT_KEY') # reads .env file from your root folder of this bot

# global strings to use in bot replies
version = "0.1.0"

# conversation handler constants
NAME_RESPONSE, LIMIT = range(2)
QUEUES_IN, QUEUES_MANAGE = range(2)

e = EventManager()
event_info = ['init', 0]

# TODO: this will probably break if >1 person is communicating with the bot at the same time
current_user = user

##################################################
             # Command Functions #
##################################################
def start_command(update, context):
    # chat and message IDs
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    user = update.message.from_user
    fullname = user['first_name']
    
    print(user)

    try: 
        # TODO: adding a new user cannot be just from /start command
        new_user = User(user_id=user['id'], fullname=fullname, username=user['username'], chat_id=chat_id) 
        e.add_user(new_user)
        # TODO: this will probably break if >1 person is communicating with the bot at the same time
        current_user = new_user
    except Exception as ex:
        print(ex)

    bot_welcome = """
        Hello {}! \n\nWelcome to version {} of QueueNow!\n
Use /newqueue to start a new queue!
Use /checkqueues to check your current queues!
Use /help to show more commands!""".format(fullname, version)
    
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
    
    update.message.reply_text(text=reply)
    
    return NAME_RESPONSE

def name_response(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    event_name = update.message.text
    event_info[0] = event_name
    
    update.message.reply_text("""{}? Sounds like it's going to be a lit event!\n
So how many people are you expecting for {}?""".format(event_name, event_name))

    return LIMIT

def limit_command(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    event_limit = update.message.text
    print('limit command msg id: ',msg_id)
    
    try: # test if given message is a whole number
        event_limitInt = int(event_limit) # prevent users from giving a float number
        event_limit = str(event_limitInt) 
        event_info[1] = event_limit
        event_name = event_info[0]
        event_limit = event_info[1]

        new_event = Event(event_name, date.today().strftime("%d/%m/%Y"), date.now().strftime("%H:%M:%S"), event_limit)
        e.add_event(new_event)
        event_id = str(new_event.get_event_id())
        
        keyboard = build_event_buttons(event_id, 'admin')
        queue_message = build_queue_message(new_event)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text("Okie, setting event limit to {}".format(event_limit))
        update.message.reply_text( 
            text=queue_message, 
            reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as ex:
        update.message.reply_text("Sorry, please give me a whole number!")
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
    query_data = update.callback_query.data
    
    data_list = query_data.split('_')
    event_id = data_list[1]
    button_type = data_list[2]
    
    try:
        event = e.get_event(event_id)
    except Exception as exception:
        context.bot.answerCallbackQuery(text='Event not found!', callback_query_id=query_id)
        return
    
    queue_message = build_queue_message(event)
    keyboard = build_event_buttons(event_id, button_type)
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        context.bot.edit_message_text(text=queue_message, chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup)
        context.bot.answerCallbackQuery(text='Event updated!', callback_query_id=query_id)
    except Exception as exception:
        context.bot.answerCallbackQuery(text='Event is already updated!', callback_query_id=query_id)
        

def hcq_delete(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    query_data = update.callback_query.data
    message = update.callback_query.message
    
    print('delete msg id: ', msg_id)
    
    data_list = query_data.split('_')
    event_id = data_list[1]
    
    try:
        event = e.get_event(event_id)
        queue_message = build_queue_message(event)
        e.remove_event(event)
        context.bot.edit_message_text(text=queue_message, chat_id=chat_id, message_id=msg_id)
        context.bot.answerCallbackQuery(text='Event deleted!', callback_query_id=query_id)
    except:
        context.bot.answerCallbackQuery(text='Event not found!', callback_query_id=query_id)
    
def hcq_enqueue(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    query_data = update.callback_query.data
    user_id = update.callback_query.from_user.id

    print('enqueue msg id: ', msg_id)
    
    data_list = query_data.split('_')
    event_id = data_list[1]
    button_type = data_list[2]
    
    try:
        event = e.get_event(event_id)
    except Exception as exception:
        context.bot.answerCallbackQuery(text='Event not found!', callback_query_id=query_id)
        return
    
    try:
        user = e.get_user(user_id)
        e.add_user_to_event(event, user)
        queue_message = build_queue_message(event)
        keyboard = build_event_buttons(event_id, button_type)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(text=queue_message, chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup)
        context.bot.answerCallbackQuery(text='You are added!', callback_query_id=query_id)
    except Exception as exception:
        print(exception)
        context.bot.answerCallbackQuery(text='You are already added!', callback_query_id=query_id)
    
def hcq_dequeue(update, context): 
    chat_id = update.callback_query.message.chat.id
    msg_id = update.callback_query.message.message_id
    query_id = update.callback_query.id
    query_data = update.callback_query.data
    user_id = update.callback_query.from_user.id
    
    data_list = query_data.split('_')
    event_id = data_list[1]
    button_type = data_list[2]
    
    try:
        event = e.get_event(event_id)
    except Exception as exception:
        context.bot.answerCallbackQuery(text='Event not found!', callback_query_id=query_id)
        return
    
    try:
        user = e.get_user(user_id)
        e.remove_user_from_event(event, user)
        queue_message = build_queue_message(event)
        keyboard = build_event_buttons(event_id, button_type)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        context.bot.edit_message_text(text=queue_message, chat_id=chat_id, message_id=msg_id, reply_markup=reply_markup)
        context.bot.answerCallbackQuery(text='You are removed!', callback_query_id=query_id)
    except Exception as exception:
        context.bot.answerCallbackQuery(text='You are already removed!', callback_query_id=query_id)
    
def check_queues_in(update, context): 
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    user_id = update.message.from_user.id
    
    queues_message = build_queues_list(user_id)
    
    context.bot.sendMessage(chat_id=chat_id, text=queues_message)
    context.bot.sendMessage(chat_id=chat_id, text="Send me the queue number you want to check!")
    
    return QUEUES_IN

def check_queues_manage(update, context): 
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    user_id = update.message.from_user.id
    
    # TODO: Ask backend how user participating queues are different from admin queues
    queues_message = build_queues_list(user_id)
    
    context.bot.sendMessage(chat_id=chat_id, text=queues_message)
    context.bot.sendMessage(chat_id=chat_id, text="Send me the queue number you want to check!")
    
    return QUEUES_MANAGE

def display_queues_in(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    selected_queue = update.message.text
    
    try:
        selected_queue = int(selected_queue)
        # TODO: get event id from event name in the list (potential problem of non unique names)
        event_id = '0' # PLACEHOLDER
        keyboard = build_event_buttons(event_id, 'non-admin')
        event = e.get_event(event_id)
        queue_template = build_queue_message(event)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(text=queue_template, reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as ex: 
        update.message.reply_text("Sorry, please give me a whole number!")
        return QUEUES_IN
    
    
def display_queues_manage(update, context):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    selected_queue = update.message.text
    
    try:
        selected_queue = int(selected_queue)
        # TODO: get event id from event name in the list (potential problem of non unique names)
        event_id = '0' # PLACEHOLDER
        keyboard = build_event_buttons(event_id, 'admin')
        event = e.get_event(event_id)
        queue_template = build_queue_message(event)
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(text=queue_template, reply_markup=reply_markup)

        return ConversationHandler.END
    
    except Exception as ex: 
        update.message.reply_text("Sorry, please give me a whole number!")
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
    event_id = event.get_event_id()
    event_name = event.name
    event_date = event.date
    event_time = event.time 
    event_participants = event.participants_list.items
    event_participants_max = str(event.participants_limit)
    event_waiting = event.waiting_list.items
    
    participants = ""
    waiting = ""
    participants_count = 0
    waiting_count = 0
    for person in event_participants:
        name = person.fullname
        participants += name + "\n"
        participants_count += 1
    
    for person in event_waiting:
        name = person.fullname
        waiting += name + "\n"
        waiting_count += 1
    
    message_content = """
{}\n
Participating! ({}/{} people)
{}\n
Waiting! ({} people)
{}\n
""".format(event_name, str(participants_count), event_participants_max, participants, str(waiting_count), waiting)
    
    return message_content

def build_queues_list(user_id):
    user = e.get_user(user_id)
    user_events = user.events
    
    message = "These are your queues! \n\n"
    event_counter = 1
    
    for event in user_events:
        message += str(event_counter) + ". " + event.name + "\n"
        event_counter += 1
        
    return message
    
def build_event_buttons(event_id, type):
    # event_id is the unique id of event, type defines the keyboard buttons generated
    event_id = str(event_id)
    update_button = 'update_' + event_id + '_' + str(type)
    delete_button = 'delete_' + event_id + '_' + str(type)
    enqueue_button = 'enqueue_' + event_id + '_' + str(type)
    dequeue_button = 'dequeue_' + event_id + '_' + str(type)
    
    if type == 'admin':
        keyboard = [
                [InlineKeyboardButton("Publish Queue", switch_inline_query='PLACEHOLDER')], 
                [InlineKeyboardButton("Update Queue", callback_data=update_button),
                    InlineKeyboardButton("Delete Queue", callback_data=delete_button)],
                [InlineKeyboardButton("I'm going!", callback_data=enqueue_button),
                    InlineKeyboardButton("I'm not going!", callback_data=dequeue_button)]
            ]
    elif type == 'non-admin':
        keyboard = [
                [InlineKeyboardButton("Update Queue", callback_data=update_button)],
                [InlineKeyboardButton("I'm going!", callback_data=enqueue_button),
                    InlineKeyboardButton("I'm not going!", callback_data=dequeue_button)]
            ]
    elif type == 'group':
        keyboard = [
                [InlineKeyboardButton("Update Queue", callback_data=update_button)],
                [InlineKeyboardButton("I'm going!", callback_data=enqueue_button),
                    InlineKeyboardButton("I'm not going!", callback_data=dequeue_button)]
            ]
    else:
        keyboard = [
                [InlineKeyboardButton("Unrecognized type", callback_data='unrecognized')]
            ]
        
    return keyboard

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
            MessageHandler(Filters.regex(re.compile('Queues I\'m participating in', re.IGNORECASE)), check_queues_in),
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
    dp.add_handler(CallbackQueryHandler(hcq_update, pattern='update'))
    dp.add_handler(CallbackQueryHandler(hcq_delete, pattern='delete'))
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
