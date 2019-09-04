import logging
import os
import scenes

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# def error(bot, update, error):
#     logger.warning('Update "%s" caused error "%s"', update, error)

class TestBoop:
    def __init__(self):
        self.TOKEN = os.environ.get('TOKEN', None)
        self.NAME = os.environ.get('NAME', None)
        # Port is given by Heroku
        self.PORT = os.environ.get('PORT')

        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        #State 
        self.click = 0
        # Set up the Updater
        updater = Updater(self.TOKEN)
        dp = updater.dispatcher
        # Add handlers

        dp.add_handler(CommandHandler('start', scenes.start))
        dp.add_handler(CommandHandler('help', scenes.help))
        dp.add_handler(CommandHandler('test', scenes.test))
        dp.add_handler(CommandHandler('boop', self.boop))

        # dp.add_handler(MessageHandler(Filters.text, echo))
        dp.add_error_handler(self.error)

        # Start the webhook
        updater.start_webhook(listen="0.0.0.0",
                            port=int(self.PORT),
                            url_path=self.TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(self.NAME, self.TOKEN))
        updater.idle()
        
    
    def boop(self, bot, update):
        self.click += 1
        update.effective_message.reply_text(text="*Boop* {}".format(self.click),parse_mode=telegram.ParseMode.MARKDOWN)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)
        


if __name__ == "__main__":
    # # Set these variable to the appropriate values
    # TOKEN = os.environ.get('TOKEN', None)
    # NAME = os.environ.get('NAME', None)

    # # Port is given by Heroku
    # PORT = os.environ.get('PORT')

    # # Enable logging
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                     level=logging.INFO)
    # logger = logging.getLogger(__name__)

    # # Set up the Updater
    # updater = Updater(TOKEN)
    # dp = updater.dispatcher
    # # Add handlers

    # dp.add_handler(CommandHandler('start', scenes.start))
    # dp.add_handler(CommandHandler('help',scenes.help))
    # dp.add_handler(CommandHandler('test',scenes.test))

    # # dp.add_handler(MessageHandler(Filters.text, echo))
    # dp.add_error_handler(error)

    # # Start the webhook
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    # updater.idle()

    bot = TestBoop()