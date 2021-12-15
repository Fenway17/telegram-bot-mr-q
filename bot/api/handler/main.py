import os
from flask import Blueprint, request
import telegram

bot_handler = Blueprint('bot', __name__)


@bot_handler.route('/')
def respond():
    return "Bot Handler"