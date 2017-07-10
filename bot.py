
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from key import apikey
from urllib.parse import urlparse
import os, logging, datetime, time, requests, random
from html.parser import HTMLParser

notelist = []

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def updateNoteList():
    global notelist
    notelist = []

    r = requests.get('http://www.billwurtz.com/notebook.html')

    # create a subclass and override the handler methods
    class NoteParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            global notelist

            if (tag == "a"):
                notelist.append(attrs[0][1])

    parser = NoteParser()
    parser.feed(r.text)

    #print(notelist)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Just do /note my dude")


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Just do /note my dude \nbillwurtz.com')

def ping(bot, update):
    bot.sendMessage(update.message.chat_id, text='Pong')


def time(bot, update):
    bot.sendMessage(update.message.chat_id, text=str(datetime.datetime.now()))


def chatinfo(bot, update):
    bot.sendMessage(update.message.chat_id, text="chat_id is "+str(update.message.chat_id))
    bot.sendMessage(update.message.chat_id, text="user id is "+str(update.message.from_user.id))


def note(bot, update):
    global notelist

    r = requests.get('http://www.billwurtz.com/' +
        notelist[random.randint(0, len(notelist)-1)])

    print(r.url)

    class NoteReader(HTMLParser):
        def handle_data(self, data):
            print(data)

            if (data.replace(" ", "").replace(" ", "") != '' and data.replace(" ", "").replace(" ", "") != '\n'):
                bot.sendMessage(update.message.chat_id, text=data)

    parser = NoteReader()
    parser.feed(r.text)


def error(bot, update, error):
    print('Update "%s" caused error "%s"' % (update, error))


def parse(bot, update):
    #print(str(update.channel_post.chat_id))
    print("file: " + str(update.message.document.file_id))
    print("Message from " + update.message.from_user.first_name + "(" + str(update.message.from_user.id) + "): " +
          update.message.text + " (" + str(update.message.message_id) + ")")


def main():
    updateNoteList()

    TOKEN = apikey
    PORT = int(os.environ.get('PORT', '5000'))
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # add handlers
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.setWebhook("https://" + str(os.environ.get("APPNAME")) + ".herokuapp.com/" + TOKEN)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("chatinfo", chatinfo))
    dp.add_handler(CommandHandler("note", note))

    dp.add_handler(MessageHandler([Filters.text], parse))

    dp.add_error_handler(error)

    updater.idle()


if __name__ == '__main__':
    main()
