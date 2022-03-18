import telebot
import datetime
from telebot import types
import sqlite3

con = sqlite3.connect('price.db', check_same_thread=False)
cursorObj = con.cursor()
cursorObj.execute("""CREATE TABLE IF NOT EXISTS prices(name, value)""")
data = [('Эспрессо', 130), ('Фильтр 200', 130), ('Фильтр 300', 200), ('Американо', 130),
        ('Капучино 200', 130), ('Капучино 300', 160), ('Капучино 400', 185), ('Флэт Уайт', 150),
        ('Латте 300', 160), ('Латте 400', 185), ('Раф 300', 160), ('Раф 400', 190),
        ('Раф  арахис 300', 200), ('Раф  арахис 400', 230), ('Раф  с/к 300', 180), ('Раф  с/к 400', 220),
        ('Чай фруктовый', 100), ('Чай гречишный', 150), ('Чай масала', 170), ('Чай матча 200', 170),
        ('Чай матча 300', 210),
        ('Пабло латте', 250), ('Латте халва', 220), ('Чиабатта лосось-творожный сыр', 170), ('Чиабатта индейка', 170),
        ('Чиабатта цыпленок барбекю', 170), ('Чиабатта моцарелла-томаты', 170), ('Клаб сендвич мал', 140),
        ('Клаб сендвич бол', 280), ('Сендвич с курицей мал', 140), ('Сендвич с курицей бол', 280),
        ('Салат греческий', 160), ('Гранола', 150), ('Чизкейк', 150), ('Миндальный торт', 160), ('Наполеон', 140),
        ('Вуппи пай', 122), ('Брауни', 108), ('Маффины', 85), ('Макарон', 60)]
# cursorObj.executemany("INSERT INTO prices VALUES(?,?)", data)
sqlite3.connect(":memory:", check_same_thread=False)
con.commit()

bot = telebot.TeleBot('INSERT YOUR TOKEN')
now = datetime.datetime.now()
global final_price
final_price = 0
global price
global answer
final_box = []


@bot.message_handler(commands=['start'])
def start_message(message):
    today = now.day
    hour = now.hour
    if today == now.day and 6 <= hour < 12:
        bot.send_message(message.chat.id, 'Доброе утро, если вы хотите сделать заказ, напишите /order,  время работы '
                                          '-  /information, меню -/menu')
    elif today == now.day and 12 <= hour < 17:
        bot.send_message(message.chat.id, 'Добрый день, если вы хотите сделать заказ, напишите /order,  время работы '
                                          '-  /information, меню -/menu')
    elif today == now.day and 17 <= hour < 23:
        bot.send_message(message.chat.id, 'Добрый вечер, если вы хотите сделать заказ, напишите /order,  время работы '
                                          '-  /information, меню -/menu')


@bot.message_handler(commands=['information'])
def give_information(message):
    bot.send_message(message.chat.id, 'Мы работаем ежедневно с 8:00 до 22:00')


@bot.message_handler(commands=['order'])
def ordering(message):
    global final_price
    final_price = 0
    bot.send_message(message.chat.id, 'Что вы желаете? '
                                      'Необходимо написать вид напитка и мл, например: Капучино 200' ','
                                      'Клаб сендвич мал')

    @bot.message_handler(content_types=['text'])
    def make_order(message):
        coffee_menu(message)
        tea_menu(message)
        byauthor_menu(message)
        food_sandwiches(message)
        perekus_food(message)
        deserts_food(message)


@bot.message_handler(commands=['menu'])
def menu(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row('Напитки', 'Еда')
    keyboard.add()
    send = bot.send_message(message.chat.id,
                            'Выберите интересующую вас категорию', reply_markup=keyboard)
    bot.register_next_step_handler(send, menu_for)


def menu_for(message):
    if message.text == 'Напитки':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Кофе', 'Чай', 'Авторские')
        keyboard.row('Вернуться')
        keyboard.add()
        send = bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=keyboard)
        bot.register_next_step_handler(send, drinks_menu)
    elif message.text == 'Еда':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Сэндвичи', 'Перекус', 'Десерты')
        keyboard.add('Вернуться')
        send = bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=keyboard)
        bot.register_next_step_handler(send, food_menu)


def drinks_menu(message):
    if message.text == 'Кофе':
        bot.send_photo(message.chat.id, open('materials/1.jpg', 'rb'))
        bot.send_message(message.chat.id, 'Если вам что-то понравилось сделайте заказ и напишите /order, для того '
                                          'чтобы вернуться напишите /menu :)')
    elif message.text == 'Чай':
        bot.send_photo(message.chat.id, open('materials/4.jpg', 'rb'))
        bot.send_message(message.chat.id,
                         'Если вам что-то понравилось сделайте заказ и напишите /order, для того чтобы вернуться '
                         'напишите /menu :)')
    elif message.text == 'Авторские':
        bot.send_photo(message.chat.id, open('materials/5.jpg', 'rb'))
        bot.send_message(message.chat.id,
                         'Если вам что-то понравилось сделайте заказ и напишите /order, для того чтобы вернуться '
                         'напишите /menu :)')
    elif message.text == 'Вернуться':
        menu(message)


def coffee_menu(message):
    global price
    global final_price
    if message.text.lower() == 'эспрессо':
        keyboard_espresso = types.InlineKeyboardMarkup(row_width=2)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_espresso.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/espresso.jpg', 'rb'),
                       reply_markup=keyboard_espresso)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Эспрессо'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'фильтр 200':
        keyboard_filtr = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/200ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_filtr.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/filtr.jpg', 'rb'),
                       reply_markup=keyboard_filtr)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Фильтр 200'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'фильтр 300':
        keyboard_filtr = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_filtr.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/filtr.jpg', 'rb'),
                       reply_markup=keyboard_filtr)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Фильтр 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'американо':
        keyboard_americano = types.InlineKeyboardMarkup(row_width=2)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_americano.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/americano.jpg', 'rb'),
                       reply_markup=keyboard_americano)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Американо'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'капучино 200' or message.text.lower() == 'капуч 200':
        keyboard_capuch = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/200ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_capuch.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/capuccino.jpg', 'rb'),
                       reply_markup=keyboard_capuch)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Капучино 200'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'капучино 300' or message.text.lower() == 'капуч 300':
        keyboard_capuch = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_capuch.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/capuccino.jpg', 'rb'),
                       reply_markup=keyboard_capuch)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Капучино 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'капучино 400' or message.text.lower() == 'капуч 400':
        keyboard_capuch = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_capuch.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/capuccino.jpg', 'rb'),
                       reply_markup=keyboard_capuch)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Капучино 400'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'флэт уайт' or message.text.lower() == 'флэт':
        keyboard_flat = types.InlineKeyboardMarkup(row_width=2)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_flat.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/flat-white.jpg.jpg', 'rb'),
                       reply_markup=keyboard_flat)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Флэт Уайт'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'латте 300':
        keyboard_latte = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_latte.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/latte.jpg', 'rb'),
                       reply_markup=keyboard_latte)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Латте 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'латте 400':
        keyboard_latte = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_latte.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/latte.jpg', 'rb'),
                       reply_markup=keyboard_latte)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Латте 400'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф 300':
        keyboard_raf = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf-kofe.jpg', 'rb'),
                       reply_markup=keyboard_raf)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф 400':
        keyboard_raf = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf-kofe.jpg', 'rb'),
                       reply_markup=keyboard_raf)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф 400'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф арахис 300':
        keyboard_raf_ar = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf_ar.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf_arahis.jpg', 'rb'),
                       reply_markup=keyboard_raf_ar)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф  арахис 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф арахис 400':
        keyboard_raf_ar = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf_ar.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf_arahis.jpg', 'rb'),
                       reply_markup=keyboard_raf_ar)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф  арахис 400'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф соленая карамель 300':
        keyboard_raf_sol = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf_sol.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf_sol_caramel.jpg', 'rb'),
                       reply_markup=keyboard_raf_sol)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф  с/к 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'раф соленая карамель 400':
        keyboard_raf_sol = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_raf_sol.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/raf_sol_caramel.jpg', 'rb'),
                       reply_markup=keyboard_raf_sol)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Раф  с/к 400'""")
        price = cursorObj.fetchall()
        price = list(price[0])


def tea_menu(message):
    global price
    global final_price
    if message.text.lower() == 'чай фруктовый' or message.text.lower() == 'фруктовый':
        keyboard_fruit_tea = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        add1 = types.InlineKeyboardButton(text='Добавить в корзину/400ml', callback_data='add1')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_fruit_tea.add(add, add1, delete, box)
        bot.send_photo(message.chat.id, open('materials/herbal-tea-roses.jpg', 'rb'),
                       reply_markup=keyboard_fruit_tea)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чай фруктовый'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'чай гречишный' or message.text.lower() == 'гречишный':
        keyboard_grech_tea = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_grech_tea.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/tea_grech.jpg', 'rb'),
                       reply_markup=keyboard_grech_tea)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чай гречишный'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'масала':
        keyboard_masala = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_masala.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/masala.jpg', 'rb'),
                       reply_markup=keyboard_masala)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чай масала'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'матча 200':
        keyboard_matcha = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/200ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_matcha.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/matcha.jpg', 'rb'),
                       reply_markup=keyboard_matcha)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чай матча 200'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'матча 300':
        keyboard_matcha = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_matcha.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/matcha.jpg', 'rb'),
                       reply_markup=keyboard_matcha)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чай матча 300'""")
        price = cursorObj.fetchall()
        price = list(price[0])


def byauthor_menu(message):
    global price
    global final_price
    if message.text.lower() == 'пабло латте' or message.text.lower() == 'пабло-латте':
        keyboard_pablo = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_pablo.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/pablo.jpg', 'rb'),
                       reply_markup=keyboard_pablo)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Пабло латте'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'латте халва' or message.text.lower() == 'латте-халва':
        keyboard_halva = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/300ml', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_halva.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/halva.jpg', 'rb'),
                       reply_markup=keyboard_halva)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Латте халва'""")
        price = cursorObj.fetchall()
        price = list(price[0])


def food_menu(message):
    if message.text.lower() == 'сэндвичи':
        bot.send_photo(message.chat.id, open('materials/sandwich.jpg', 'rb'))
        bot.send_message(message.chat.id,
                         'Если вам что-то понравилось сделайте заказ и напишите /order, для того чтобы вернуться '
                         'напишите /menu :)')
    elif message.text.lower() == 'перекус':
        bot.send_photo(message.chat.id, open('materials/perekus.jpg', 'rb'))
        bot.send_message(message.chat.id,
                         'Если вам что-то понравилось сделайте заказ и напишите /order, для того чтобы вернуться '
                         'напишите /menu :)')
    elif message.text.lower() == 'десерты':
        bot.send_photo(message.chat.id, open('materials/deserts.jpg', 'rb'))
        bot.send_message(message.chat.id,
                         'Если вам что-то понравилось сделайте заказ и напишите /order, для того чтобы вернуться '
                         'напишите /menu :)')

    elif message.text == 'Вернуться':
        menu(message)


def food_sandwiches(message):
    global price
    global final_price
    if message.text.lower() == 'чиабатта моцарелла-томаты' or message.text.lower() == 'чиабатта томаты-моцарелла':
        keyboard_sandwiches = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_sandwiches.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/chiabatta1.jpg', 'rb'),
                       reply_markup=keyboard_sandwiches)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чиабатта моцарелла-томаты'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'чиабатта индейка':
        keyboard_sandwiches = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_sandwiches.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/chiab3.png', 'rb'),
                       reply_markup=keyboard_sandwiches)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чиабатта индейка'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'чиабатта лосось-творожный сыр':
        keyboard_sandwiches = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_sandwiches.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/chiab4.jpg', 'rb'),
                       reply_markup=keyboard_sandwiches)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чиабатта лосось-творожный сыр'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'чиабатта цыпленок барбекю':
        keyboard_sandwiches = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_sandwiches.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/chiab2.jpg', 'rb'),
                       reply_markup=keyboard_sandwiches)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чиабатта цыпленок барбекю'""")
        price = cursorObj.fetchall()
        price = list(price[0])


def perekus_food(message):
    global price
    global final_price
    if message.text.lower() == 'клаб сендвич мал' or message.text.lower() == 'клаб сэндвич мал':
        keyboard_clab = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/ мал', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_clab.add(add, delete, box)
        bot.send_photo(message.chat.id, open('C:/pythonProject/Lib/clab.jpg', 'rb'),
                       reply_markup=keyboard_clab)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Клаб сендвич мал'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'клаб сендвич бол' or message.text.lower() == 'клаб сэндвич бол':
        keyboard_clab = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/бол', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_clab.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/clab.jpg', 'rb'),
                       reply_markup=keyboard_clab)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Клаб сендвич бол'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'сендвич с курицей' or message.text.lower() == 'сэндвич с курицей':
        keyboard_sandwich = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину/ мал', callback_data='add')
        add1 = types.InlineKeyboardButton(text='Добавить в корзину/ бол', callback_data='add1')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_sandwich.add(add, add1, delete, box)
        bot.send_photo(message.chat.id, open('materials/sandw.jpg', 'rb'),
                       reply_markup=keyboard_sandwich)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Клаб сендвич бол'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'салат греческий' or message.text.lower() == 'греческий салат' or message.text.lower() == 'греческий':
        keyboard_salad = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_salad.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/salad.jpg', 'rb'),
                       reply_markup=keyboard_salad)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Салат греческий'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'гранола':
        keyboard_granola = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_granola.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/gtranola.jpg', 'rb'),
                       reply_markup=keyboard_granola)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Гранола'""")
        price = cursorObj.fetchall()
        price = list(price[0])


def deserts_food(message):
    global price
    global final_price
    if message.text.lower() == 'чизкейк':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/chizkieik.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Чизкейк'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'миндальный торт' or message.text.lower() == 'торт миндальный':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/mindal.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Миндальный торт'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'наполеон':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/tort-napoleon.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Наполеон'""")
        price = cursorObj.fetchall()
        price = list(price[0])


    elif message.text.lower() == 'вуппи пай' or message.text.lower() == 'вупи пай':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/vupi.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Вуппи пай'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'брауни':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/brauni.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Брауни'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'маффины' or message.text.lower() == 'маффин':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/maffiny.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Маффины'""")
        price = cursorObj.fetchall()
        price = list(price[0])

    elif message.text.lower() == 'макарон' or message.text.lower() == 'макаронс':
        keyboard_deserts = types.InlineKeyboardMarkup(row_width=1)
        add = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='add')
        delete = types.InlineKeyboardButton(text='Удалить из корзины', callback_data='delete')
        box = types.InlineKeyboardButton(text='Корзина', callback_data='box')
        keyboard_deserts.add(add, delete, box)
        bot.send_photo(message.chat.id, open('materials/macaron.jpg', 'rb'),
                       reply_markup=keyboard_deserts)
        cursorObj.execute("""SELECT value FROM prices WHERE name='Макарон'""")
        price = cursorObj.fetchall()
        price = list(price[0])


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    call_box(call)
    answer = ' '
    global price
    global final_price
    if call.data == 'add':
        bot.answer_callback_query(callback_query_id=call.id, text='Добавлено в корзину')
        final_price += price[0]
    elif call.data == 'delete':
        bot.answer_callback_query(callback_query_id=call.id, text='Удалено из корзины')
        final_price -= price[0]
    elif call.data == 'box':
        answer = 'Оформить заказ на сумму:' + ' ' + str(final_price) + ' ' + 'рублей(-ля)'
        keyboard_order = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard_order.add(yes, no)
        bot.send_message(call.message.chat.id, answer, reply_markup=keyboard_order)


def call_box(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Спасибо за заказ, ждем Вас!')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Если хотите сделать новый заказ напишите /order, посмотреть меню /menu')


bot.infinity_polling()
