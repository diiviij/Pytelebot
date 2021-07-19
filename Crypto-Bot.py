import os
import time
import telebot
from telebot import types
from tracker import get_prices

my_secret = os.environ['API_KEY']
TOKEN = my_secret
knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot \n',
    'help'        : 'Gives you information about the available commands \n',
    'crypto'      : 'CryptoCurreny Prices Real Time \n',
    '/Type name'  : 'Example Type BTC to know BTC price'
}

# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        bot.send_message(cid, "Hello, stranger, let me scan you...")
        bot.send_message(cid, "Scanning complete, I know you now")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need for me to scan you again!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")

@bot.message_handler(commands=['crypto'])
def crypto_price(m):
    cid = m.chat.id
    message=""
    crypto_data = get_prices()
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"
        
    bot.send_message(cid, message)
    


# user can chose an image (multi-stage command example)

# filter on a specific message
@bot.message_handler(func=lambda message: message.text.lower() == "hi")
def command_text_hi(m):
    name = m.chat.first_name
    bot.send_message(m.chat.id, "Hi "+ str(name)+ "\n How are you ?")


@bot.message_handler(func=lambda message: message.text.lower() == "fine")
def geerti_reply(m):
    usr = m.chat.id
    bot.reply_to(usr,"Great")

    
@bot.message_handler(func=lambda message: message.text.lower() == "wrx")
def btc_price(m):
      cid = m.chat.id
      btcpr = get_prices()
      for i in btcpr:
        coin = btcpr[i]["coin"]
        price = btcpr[i]["price"]
        change_day = btcpr[i]["change_day"]
        change_hour = btcpr[i]["change_hour"]
        wrxanswer = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: #{change_day:.3f}%\n\n"
        if coin == 'WRX':
          break

      bot.send_message(cid, wrxanswer)

@bot.message_handler(func=lambda message: message.text.lower() == "btc")
def btc_price(m):
      cid = m.chat.id
      btcpr2 = get_prices()
      for i in btcpr2:
        coin = btcpr2[i]["coin"]
        price = btcpr2[i]["price"]
        change_day = btcpr2[i]["change_day"]
        change_hour = btcpr2[i]["change_hour"]
        message = f"Coin: {coin}\nPrice: ${price:,.2f}\nHour Change: {change_hour:.3f}%\nDay Change: #{change_day:.3f}%\n\n"
        
        if coin == 'BTC':
              break

      bot.send_message(cid, message)

@bot.message_handler(func=lambda message: message.text.lower() == "bye")
def bye_message(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "Bye Have a Gret Day !")
    

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")




bot.polling()
