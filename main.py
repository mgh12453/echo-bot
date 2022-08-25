import logging
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def echo_photo(update, context):
    update.message.reply_text("مگه غلومی بهت نگفته بود فایل بفرستی فقظ")

def fileid(update, context):
    # update.text("Pleasss")
    # update.message.reply_text('check 2')
    # update.message.reply_text(update.message.document.file_id)
    # f = context.bot.get_file(update.message.document).download()
    # buff = os.path.basename(f.name)
    filename = update.message.document.file_name
    fileid = update.message.document.file_id
    chatid = update.message.chat.id
    
    context.bot.get_file(update.message.document).download()
    # writing to a custom file
    with open(filename, 'wb') as f:
        context.bot.get_file(update.message.document).download(out=f)
    
    context.bot.sendPhoto(chat_id=chatid, caption=filename, photo=open(filename, 'rb').read())
    # update.message.reply_photo(update.message.document, caption=filename)
    # update.message.reply_text(update.message.document.file_name)
    # update.message.reply_text(text="Done!")
    # os.rm(buff)
    # update.message.reply_text(update.message.document.file_path)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    TOKEN = '5549731915:AAECKDbPBfR7HIpin8U_HF2iJpFLe2V0cWs'
    APP_NAME='https://echo-bot-12453.herokuapp.com/'

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.document, fileid))
    dp.add_handler(MessageHandler(Filters.photo, echo_photo))

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN,webhook_url=APP_NAME + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()

