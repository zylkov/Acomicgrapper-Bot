import telegram 
import pkg_resources

def get_response_text(file_name):
    # https://stackoverflow.com/a/20885799/2490759
    path = '/'.join(('texts', file_name))
    return pkg_resources.resource_string(__name__, path).decode("UTF-8")

def start(bot, update):
    update.effective_message.reply_text(text=get_response_text('greeting.tg.md').format(update.message.from_user.first_name), parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def help(bot, update):
    update.effective_message.reply_text(text=get_response_text('help.tg.md'), parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

def test(bot, update):
    text = "*bold* _italic_ `fixed width font` [link](http://google.com)."
    bot.send_message(chat_id=update.message.chat_id,text=text, parse_mode=telegram.ParseMode.MARKDOWN)

