import telebot
from telebot import types
import random
bet = 0
cache_bank = 0
wheel_ring = ['Green','Red', 'Black', 'Red', 'Black', 'Red', 'Black',
              'Red', 'Black', 'Red', 'Black', 'Black', 'Red',                       #TODO:
              'Black', 'Red', 'Black', 'Red', 'Black', 'Red',                       #Ставка на сектор 2 к 1
              'Red', 'Black', 'Red', 'Black', 'Red', 'Black',                       #Несколько ставок на один прокрут
              'Red', 'Black', 'Red', 'Black', 'Black', 'Red',
              'Black', 'Red', 'Black', 'Red', 'Black', 'Red']
kostyl_bet_num = [i for i in range(0, 38)]
photo_roullete = open('D:\Projects\Python_projects\Telegram_bot_roulette\photos\sb.png', 'rb')



bot = telebot.TeleBot('6190163742:AAH0oRTL05UgpIRfj_6jeSOj59MKTR-daRA')

@bot.message_handler(commands=[ 'spin', 'start']) ##Старт
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Счет')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Сделать ставку')
    markup.row(btn2)
    btn3 = types.KeyboardButton('Внести депозит')
    markup.row(btn3)
    bot.register_next_step_handler(message, crossroad)
    bot.reply_to(message, "Здравствуйте, добро пожаловать в лотерею 'ЛАВАНДОС' ", reply_markup=markup)
@bot.message_handler(commands=['crossik'])
def crossroad(message): ##Перепутье
    global cache_bank
    depos = 0
    if message.text == 'Счет':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Счет')
        markup.add(btn1)
        btn2 = types.KeyboardButton('Сделать ставку')
        markup.add(btn2)
        btn3 = types.KeyboardButton('Внести депозит')
        markup.add(btn3)
        bot.send_message(message.chat.id, f'Ваш счет {cache_bank}')
        bot.reply_to(message, 'Хотите ли вы , сделать что-нибудь еще?', reply_markup=markup)
        bot.register_next_step_handler(message, crossroad)
    elif message.text == 'Внести депозит':
        bot.send_message(message.chat.id, 'Введите сумму вашего депозита')
        bot.register_next_step_handler(message,deposit)
    elif message.text == 'Сделать ставку':
        table_of_bets_bet(message)
        ##bot.register_next_step_handler(message, table_of_bets_bet)

@bot.message_handler(commands=['deposit'])
def deposit(message):
    global cache_bank
    if message.text.isnumeric():
        depos = int(message.text)
        cache_bank += depos
        bot.send_message(message.chat.id, f'Ваш счет {cache_bank}, вы успешно пополнили свой баланс')
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Счет')
        markup.add(btn1)
        btn2 = types.KeyboardButton('Сделать ставку')
        markup.add(btn2)
        btn3 = types.KeyboardButton('Внести депозит')
        markup.add(btn3)
        bot.reply_to(message, 'Хотите ли вы , сделать что-нибудь еще?', reply_markup=markup)
        bot.register_next_step_handler(message, crossroad)
    else:
        bot.send_message(message.chat.id, 'Введите корректную '
                                          'сумму депозита')
        bot.register_next_step_handler(message, crossroad)
@bot.message_handler(commands=['bet'])
def table_of_bets_bet(message):
    print('betik')
    global cache_bank, bet
    if cache_bank > 0:
        bot.send_message(message.chat.id, 'Введите вашу ставку')
        bot.register_next_step_handler(message, table_of_bets_bet_check)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, пополните баланс')
        bot.register_next_step_handler(message, crossroad)

def table_of_bets_bet_check(message):
    global bet, cache_bank
    if message.text.isdigit() :
        if int(message.text) <= cache_bank:
            bet = int(message.text)
            table_of_bets_callback(message)
            print('бэтик проверен')
    else:
        bot.send_message(message.chat.id, 'Введите корректно ставку')
        bot.register_next_step_handler(message, table_of_bets_bet)


def table_of_bets_callback(message):
    print('выбираем ставку')
    bets = types.InlineKeyboardMarkup();
    bet_num = types.InlineKeyboardButton(text='Ставка на число', callback_data='num');  ##от 1 до 6. Выигрыш 6:1
    bets_color = types.InlineKeyboardButton(text='Ставка на цвет', callback_data='colorik');  ##лишь одна. 2х
    bets.row(bet_num, bets_color)
    bets_chet = types.InlineKeyboardButton(text='Ставка на четность', callback_data='mod');  ##лишь одна 2х
    bets_sector = types.InlineKeyboardButton(text='Ставка на сектор', callback_data='sector');  ##мб все таки уберем?
    bets.row(bets_chet, bets_sector)
    bot.send_message(message.chat.id, 'Выберите ставку', reply_markup=bets)

@bot.callback_query_handler(func=lambda call: True)
def callback_table_of_bets(call):
    # if call.data == "num":
    #     ##don't open
    #     nums = types.InlineKeyboardMarkup()
    #     num_1 = types.InlineKeyboardButton(text='1', callback_data='1')
    #     num_2 = types.InlineKeyboardButton(text='2', callback_data='2')
    #     num_3 = types.InlineKeyboardButton(text='3', callback_data='3')
    #     num_4 = types.InlineKeyboardButton(text='4', callback_data='4')
    #     num_5 = types.InlineKeyboardButton(text='5', callback_data='5')
    #     num_6 = types.InlineKeyboardButton(text='6', callback_data='6')
    #     num_7 = types.InlineKeyboardButton(text='7', callback_data='7')
    #     num_8 = types.InlineKeyboardButton(text='8', callback_data='8')
    #     num_9 = types.InlineKeyboardButton(text='9', callback_data='9')
    #     num_10 = types.InlineKeyboardButton(text='10', callback_data='10')
    #     num_11 = types.InlineKeyboardButton(text='11', callback_data='11')
    #     num_12 = types.InlineKeyboardButton(text='12', callback_data='12')
    #     num_13 = types.InlineKeyboardButton(text='13', callback_data='13')
    #     num_14 = types.InlineKeyboardButton(text='14', callback_data='14')
    #     num_15 = types.InlineKeyboardButton(text='15', callback_data='15')
    #     num_16 = types.InlineKeyboardButton(text='16', callback_data='16')
    #     num_17 = types.InlineKeyboardButton(text='17', callback_data='17')
    #     num_18 = types.InlineKeyboardButton(text='18', callback_data='18')
    #     num_19 = types.InlineKeyboardButton(text='19', callback_data='19')
    #     num_20 = types.InlineKeyboardButton(text='20', callback_data='20')
    #     num_21 = types.InlineKeyboardButton(text='21', callback_data='21')
    #     num_22 = types.InlineKeyboardButton(text='22', callback_data='22')
    #     nums.row(num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8, num_9, num_10, num_11,
    #              num_12, num_13)
    #     num_23 = types.InlineKeyboardButton(text='23', callback_data='23')
    #     num_24 = types.InlineKeyboardButton(text='24', callback_data='24')
    #     num_25 = types.InlineKeyboardButton(text='25', callback_data='25')
    #     num_26 = types.InlineKeyboardButton(text='26', callback_data='26')
    #     num_27 = types.InlineKeyboardButton(text='27', callback_data='27')
    #     num_28 = types.InlineKeyboardButton(text='28', callback_data='28')
    #     num_29 = types.InlineKeyboardButton(text='29', callback_data='29')
    #     num_30 = types.InlineKeyboardButton(text='30', callback_data='30')
    #     num_31 = types.InlineKeyboardButton(text='31', callback_data='31')
    #     num_32 = types.InlineKeyboardButton(text='32', callback_data='32')
    #     num_33 = types.InlineKeyboardButton(text='33', callback_data='33')
    #     num_34 = types.InlineKeyboardButton(text='34', callback_data='34')
    #     num_35 = types.InlineKeyboardButton(text='35', callback_data='35')
    #     num_36 = types.InlineKeyboardButton(text='36', callback_data='36')
    #     num_0 = types.InlineKeyboardButton(text='0', callback_data='0')
    #     nums.row(num_14, num_15, num_16, num_17, num_18, num_19, num_20, num_21, num_22,
    #              num_23, num_24, num_25, num_26, num_27, num_28, num_29, num_30, num_31,
    #              num_32, num_33, num_34, num_35, num_36)
    #     nums.row(num_0)
    #     bot.send_message(call.message.chat.id, 'Выберите цифру', reply_markup=nums)
    #
    #     ##При нажатии на кнопку в bets_on_nums добавляется число , максимум до 6
    #     ##Делаем 37 кнопок, при нажатии они изменяются
    if call.data == "num":
        bot.send_photo(call.message.chat.id, photo_roullete)
        bot.send_message(call.message.chat.id, 'Введите лот на который хотите поставить')
        bot.register_next_step_handler(call.message, bets_nums)
    # elif call.data == "colorik":
    #     bot.send_message(call.message, 'Сожалеем, но в данный момент ведутся технические работы, попробуйте другую ставку')
        # print('мы в цвете')
        # colors = types.ReplyKeyboardMarkup()
        # red = types.KeyboardButton('Красное')
        # black = types.KeyboardButton('Черное')
        # colors.row(red, black)
        # bot.send_message(call.message,text='Выберите поле на которое хотите сделать ставку', reply_markup=colors)
        # whell_roll_color()
        # colors = types.InlineKeyboardMarkup()
        # red_btn = types.InlineKeyboardButton(text='Красное поле', callback_data='red')
        # black_btn = types.InlineKeyboardButton(text='Черное поле', callback_data='black')
        # colors.row(red_btn, black_btn)
        # bot.send_message(call.message.chat.id, 'Укажите поле', reply_markup=colors)
        # ##whell_roll_color(call)
        # bot.register_next_step_handler(call.message.chat.id, whell_roll_color)



def whell_roll_color(message):
    global cache_bank, bet, wheel_ring
    if message.text == 'red':
        bot.send_message(message.chat.id, 'Вы выбрали красное поле')
        roll_of_whell = random.choice(wheel_ring)
        if roll_of_whell == 'Red':
            cache_bank += bet * 2
            bot.send_message(message.chat.id,f'Поздравляем, вы выиграли! Ваш баланс {cache_bank, roll_of_whell}')
        else:
            cache_bank -= bet * 2
            bot.send_message(message.chat.id,f'К сожалению, вы проиграли! Ваш баланс {cache_bank, roll_of_whell}')
    elif message.text == 'black':
        bot.send_message(message.chat.id, 'Вы выбрали черное поле')
        roll_of_whell = random.choice(wheel_ring)
        if roll_of_whell == 'Black':
            cache_bank += bet * 2
            bot.send_message(message.chat.id, f'Поздравляем, вы выиграли! Ваш баланс {cache_bank, roll_of_whell}')
        else:
            bot.send_message(message.chat.id, f'К сожалению, вы проиграли! Ваш баланс {cache_bank, roll_of_whell}')
    else:
        bot.send_message(message.chat.id, 'Что-то пошло не так, пожалуйтса, проверьте ваш баланс и '
                                                   'попробуйте снова')
        bot.register_next_step_handler(message, crossroad)

    # elif call.data == "mod":
    #     digits = types.InlineKeyboardMarkup();
    #     digit = types.InlineKeyboardButton(text='Четные числа', callback_data='chet')
    #     not_digit = types.InlineKeyboardButton(text='Нечетные числа', callback_data='nechet')         Я НЕ ПОНИМАЮ
    #     digits.row(digit, not_digit)
    #     bot.send_message(call.message.chat.id, 'укажите', reply_markup=digits)
    #     crossroad(call.message)
    # else:
    #     bot.send_message(call.message.chat.id, 'Error')
##Крутка по четности
# def wheel_chet_roll(call):
#     global bet, cache_bank, wheel_ring
#     roll_of_wheel = random.randint(0, 37)
#     if call.data == "chet":
#         if roll_of_wheel % 2 == 0:
#             cache_bank += bet * 2
#             bot.send_message(call.message.chat.id, f'Поздравляем вы выиграли! Ваш баланс {cache_bank}')
#             crossroad(call.message)
#         else:
#             cache_bank -= bet * 2
#             bot.send_message(call.message.chat.id, f'К сожалению, вы проиграли! Ваш баланс {cache_bank}')
#             crossroad(call.message)
#     elif call.data == "nechet":
#         if roll_of_wheel % 2 == 0:
#             cache_bank -= bet * 2
#             bot.send_message(call.message.chat.id, f'К сожалению, вы проиграли! Ваш баланс {cache_bank}')
#             crossroad(call.message)
#         else:
#             cache_bank += bet * 2
#             bot.send_message(call.message.chat.id, f'Поздравляем вы выиграли! Ваш баланс {cache_bank}')
#             crossroad(call.message)
#     else:
#         bot.send_message(call.message.chat.id, 'Произошла ошибка')





##Крутка по числу
@bot.message_handler(commands=['num_roll'])
def bets_nums(message):
    global cache_bank, bet
    if message.text.isdigit():
        global cache_bank, bet, wheel_ring
        roll_of_wheel = random.randint(0, 37)
        print(roll_of_wheel)
        if roll_of_wheel == int(message.text):
            bot.send_message(message.chat.id,'АХАХХАХА')
            cache_bank += bet * 6
        elif roll_of_wheel == 0:
            bot.send_message(message.chat.id, 'ЗИРО, ЛОШАРА ЕБАННАЯ')
            cache_bank += 0
            bot.register_next_step_handler(message, crossroad)
        else:
            cache_bank -= bet * 6
            bot.send_message(message.chat.id, f"Увы, вы проиграли. Ваш баланс {cache_bank}. Число , которое выпало {roll_of_wheel}. Желаете продолжить игру?")
            bot.register_next_step_handler(message, start)


# @bot.message_handler(commands=['roll'])
# def roll(message):
#     global bet
#     if message.text.isnumeric():
#         bot.reply_to(message, f"Ваша ставка {message.text}, выберите лот.")
#         bet = int(message.text)
#         bot.register_next_step_handler(message, whell_roll_color)
#
#     else:
#         bot.reply_to(message, 'Пожалуйста, введите вашу ставку')
#         bot.register_next_step_handler(message, roll)




#первая итерация
# def roll(message):
#     global cache_bank
#     count_of_wins = 0
#     count_of_lose = 0
#     count = 0
#     bankroll = int(message.text)
#     bot.reply_to(message, f"Ваша ставка {bankroll}")
#     pockets = ["Red"] * 18 + ["Black"] * 18 + ["Green"] * 2
#     while bankroll > 0:
#         roll = random.choice(pockets)
#         count += 1
#         if roll == "Red":
#             cache_bank += bankroll * 2
#             count_of_wins += 1
#         else:
#             bankroll -= 10
#             count_of_lose += 1
#     bot.reply_to(message, f"Ваш счет {cache_bank}, число выиграшей {count_of_wins}, число проигрышей{count_of_lose}"
#                           f", общее число проигрышей{count}")




# @bot.message_handler(content_types=['text'])
# def varriations_answers_to_message(message):
#     if message.text == "Hi":
#         bot.send_message(message.from_user.id, "Здарова")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Сегодня без помощи")
#     else:
#         bot.send_message(message.from_user.id, "че")

bot.polling(none_stop=True) #Запускаем бота безпрерывно
