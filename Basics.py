import os
import telebot
from telebot import types

my_secret = os.environ['Token'] # Enter your token Id in place of TOKEN which you will get from Bot Father 

TOKEN = my_secret
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

# handle the "/start" command
@bot.message_handler(commands=['start']) 
def command_start(m):
    cid = m.chat.id
    bot.send_message(cid, "Hello "+m.chat.first_name)
    
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n
    /yt : Download Youtube Videos \n
    /greet : Greet the User"
      
    bot.send_message(cid, help_text)  # send the generated help page

    
bot.polling()  
