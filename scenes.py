import telegram 

def start(bot, update):
    text = (
        "**Добро пожаловать!**  :wave: :smile:"
        "Я помогу вам в поисках комикса на сайте :heart: [acomic.ru](https://acomics.ru) :heart:, а также скачаю страницы специально для вас."   
        "Если вы знаете название комикса выберите поиск комикса по названию. :capital_abcd: :mag:"
        "Если вы не знаете название и хотите найти специально для себя комикс выберите поиск по категориям :large_blue_diamond: :mag:"
)
    update.effective_message.reply_text(text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot, update):
    text=(
        "**Заблудились?** :confounded:"
        "Ничего здесь список основных команд:"
        ":star: /start - Поприветствую вас ещё раз. Мне не сложно :relaxed:"
        ":star: /help - Ты прям здесь! :smirk:"
        ":star: /searchword - Поиск комикса по названию. :capital_abcd: :mag:"
        ":star: /searchcat - Поиск комикса по категориям :large_blue_diamond: :mag:"
        ":star: /open - Откроем этот комикс. Главное введите правильный его индикатор :sweat_smile:"
    )
    update.effective_message.reply_text(text=text, parse_mode=telegram.ParseMode.MARKDOWN)

def test(bot, update):
    text = "*bold* _italic_ `fixed width font` [link](http://google.com)."
    bot.send_message(chat_id=update.message.chat_id,text=text, parse_mode=telegram.ParseMode.MARKDOWN)

