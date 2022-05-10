import telebot, hangman


def check_insert_char(char, player, message):
    mess = ''
    if len(char) > 1 :
        char = char[0]
    if char in player['word']:
        mess = hangman.msg('succ_char') + '\n'
    else:
        mess = hangman.msg('err') + '\n'
        player['hp'] -= 1

    for idx, val in enumerate(player['word']):
        if val == char:
            player['user_try'][idx] = char
    mess += ' '.join(player['user_try'])

    mess += '\nКоличетсво попыток: ' + str(player['hp'])
    bot.send_message(message.chat.id, mess, parse_mode='html')


def joke(message):
    if message.text.lower() == 'мотивация':
        voice = open('./voices/motivation.ogg', 'rb')
        bot.send_voice(message.chat.id, voice)
        return


def log(message):
    print(message.date,
       message.from_user.first_name,
          message.from_user.last_name,
          'начал игру', message.text)


def add_player(message):
    players.setdefault(message.chat.id, dict())
    players[message.chat.id] = {'word': '',
                                'user_try': '',
                                'hp': 5,
                                'play' : True}


def add_quest(message):
    generated_word = hangman.generate_word()
    players[message.chat.id]['word'] = generated_word
    players[message.chat.id]['user_try'] = ['_' for _ in range(len(generated_word))]


def end_game(message, player):
    msg = ''
    if player['hp'] == 0:
        msg += hangman.msg('lose')
    elif player['word'] == ''.join(player['user_try']):
        msg += hangman.msg('win')

    if msg:
        msg += ' Загаданное слово было:\n' + player['word'].capitalize() + '\n'
        msg += 'Для новой игры введи /start'
        player['play'] = False
        bot.send_message(message.chat.id, msg, parse_mode='html')


def del_player(message):
    del players[message.chat.id]


token = '5135861591:AAF9lyHGaulc0pmuGMvgPwXUknojemahiRk'
bot = telebot.TeleBot(token)
players = dict()


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in players:
        bot.send_message(message.chat.id, 'Вы уже играете!\n Чтобы закончить или начать заново введите /end', parse_mode='html')
    else:
        bot.send_message(message.chat.id, hangman.msg('start'), parse_mode='html')
        add_player(message)
        add_quest(message)

    print(players)
    log(message)


@bot.message_handler(commands=['end'])
def end(message):
    if message.chat.id not in players:
        bot.send_message(message.chat.id, 'Вы не играете!\nЧтобы начать играть введите /start')
    else:
        bot.send_message(message.chat.id, 'Ну раз ты хочешь', parse_mode='html')
        del_player(message)

    print(players)
    log(message)

@bot.message_handler()
def get_user_text(message):
    if message.chat.id not in players:
        bot.send_message(message.chat.id, 'Чтобы начать играть напиши /start', parse_mode='html')
        return

    if message.text.isalpha():
        player = players[message.chat.id]
        user_input = message.text.lower()
        joke(message)
        check_insert_char(user_input, player, message)
        end_game(message, player)

        if not player['play']:
            del_player(message)

        log(message)
    else:
        bot.send_message(message.chat.id, 'Нужно ввести букву', parse_mode='html')


bot.polling(none_stop=True)