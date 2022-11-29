import os
import time
import telebot  #pip install pytelegrambotapi
from telebot import types
from requests.exceptions import ConnectionError
import pytube
from pytube import YouTube

my_secret = os.environ['secret_key']
TOKEN = my_secret

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts
commands = {  # command description used in the "help" command
  'youtubeurl': 'to download ',
  'bye ': 'To End the Chat ',
  'about ': 'Info of this bot',
  'help': 'infor of the available commands '
  #'/Type yt-download' : 'To Download YT Videos for Free \n'
}


def get_user_step(uid):
  if uid in userStep:
    return userStep[uid]
  else:
    knownUsers.append(uid)
    userStep[uid] = 0
    print("New user detected, who hasn't used \"/start\" yet")
    return 0


def listener(messages):
  """
    When new messages arrive TeleBot will call this function.
    """
  for m in messages:
    if m.content_type == 'text':
      # print the sent message to the console
      print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)
# help page


@bot.message_handler(commands=['help'])
def command_help(m):
  cid = m.chat.id
  help_text = "The following commands are available: \n"
  for key in commands:  # generate help text out of the commands dictionary defined at the top
    help_text += "/" + key + ": "
    help_text += commands[key] + "\n"
  bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['bye'])
def command_help(m):
  cid = m.chat.id
  for key in commands:  # generate help text out of the commands dictionary defined at the top
    bye_text = "bye sweet soul " + m.chat.first_name
  bot.send_message(cid, bye_text)  # send the generated help page


@bot.message_handler(commands=['about'])
def command_help(m):
  cid = m.chat.id
  for key in commands:  # generate help text out of the commands dictionary defined at the top
    bye_text = "Youtube Video Downloader \nDeveloped by divij and param"
  bot.send_message(cid, bye_text)


@bot.message_handler(commands=['youtubeurl'])
def command_help(m):
  cid = m.chat.id
  bot.send_message(m.chat.id, "Please send the Url of the video")

  @bot.message_handler(func=lambda message: True, content_types=['text'])
  def ytube_download(m):
    bot.send_message(m.chat.id, "Please Wait,Video on the way")
    link = m.text
    yt = YouTube(link)
    print("Title: ", yt.title)
    stream = yt.streams.get_by_itag(22)
    stream.download()
    os.rename(stream.download(), 'download.mp4')
    bot.send_message(m.chat.id, "Video on the way")
    bot.send_document(cid, open('download.mp4', 'rb'))

  bot.send_message(cid, m.text)


bot.set_update_listener(listener)
bot.infinity_polling()
