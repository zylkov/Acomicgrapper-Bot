import telegram 
import pkg_resources

def get_response_text(file_name):
    # https://stackoverflow.com/a/20885799/2490759
    path = '/'.join(('texts', file_name))
    return pkg_resources.resource_string(__name__, path).decode("UTF-8")

def get_message_text(name_file, args={}):
    return get_response_text(name_file).format(args)

def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

def create_button_list(info_button_list):
    return [telegram.InlineKeyboardButton(butt[0], callback_data = butt[1]) for butt in info_button_list]

def start(bot, update):
    update.effective_message.reply_text(text=get_message_text('greeting.tg.md', update.message.from_user.first_name), parse_mode=telegram.ParseMode.MARKDOWN)

def help(bot, update):
    update.effective_message.reply_text(text=get_message_text('help.tg.md'), parse_mode=telegram.ParseMode.MARKDOWN)


def start_searchcat(bot, update):
    data = {
        "cat":"все категории",
        "age":" ".join(["G", "PG", "PG-13","R"]),
        "type": "Все",
        "low_page": str(3),
        "sort":"по дате обнавления"
    }
    update.effective_message.reply_text(text=get_message_text("searchcat.tg.md").format(info = data), 
                                        parse_mode=telegram.ParseMode.MARKDOWN)

def searchcat(bot, update):
    data = {
        "cat":"все категории",
        "age":" ".join(["G", "PG", "PG-13","R"]),
        "type": "Все",
        "low_page": str(3),
        "sort":"по дате обнавления"
    }
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=get_message_text("searchcat.tg.md").format(info = data),
                        parse_mode=telegram.ParseMode.MARKDOWN, 
                        reply_markup=searchcat_menu())

def choose_age(bot, update):
    data = " ".join(["G", "PG", "PG-13","R"])
    query = update.callback_query
    bot.edit_message_text(chat_id=query.message.chat_id,
                        message_id=query.message.message_id,
                        text=get_message_text("choose_age.tg.md").format(data), 
                        parse_mode=telegram.ParseMode.MARKDOWN, 
                        reply_markup=choose_age_menu())

def searchcat_menu():
    base_button_list = [
        ["Выбрать категории", "ch_cat"],
        ["Выбрать возрастные категории", "ch_age"],
        ["Выбрать тип комикса", "ch_type"],
        ["Указать минимум страниц","ch_lw_pg"],
        ["Выбрать метод сортировки","ch_sort"]
    ]
    button_list = create_button_list(base_button_list)
    print(button_list)
    return telegram.InlineKeyboardMarkup(build_menu(button_list, 1))

def choose_age_menu():
    base_button_list = [
        ["NR", "age_nr"],
        ["G", "age_g"],
        ["PG", "age_pg"],
        ["PG-13", "age_pg13"],
        ["R", "age_r"],
        ["NC-17", "age_nc"],
        ["<- Вернуться в меню","srchcat"]
    ]
    button_list = create_button_list(base_button_list)
    return telegram.InlineKeyboardMarkup(build_menu(button_list, 1))

def test(bot, update):
    text = "*bold* _italic_ `fixed width font` [link](http://google.com)."
    bot.send_message(chat_id=update.message.chat_id,text=text, parse_mode=telegram.ParseMode.MARKDOWN)

