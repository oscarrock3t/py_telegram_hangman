import requests
from bs4 import BeautifulSoup


def msg(arg, hp=5):
    msg_to_bot = ''
    if arg == 'start':
        msg_to_bot = 'Здравствуй, сейчас ты будешь угадывать слово! Необходимо угадывать слово по буквам.'
        msg_to_bot += ' За 5 неправильных попыток ты проиграешь! Поехали!'
    elif arg == 'err':
        msg_to_bot = f'Упс! Попробуй другую букву.'
    elif arg == 'lose':
        msg_to_bot = 'Конец!'
    elif arg == 'again':
        pass
    elif arg == 'win':
        msg_to_bot = 'Молодцом! Ты победил!'
    elif arg == 'succ_char':
        msg_to_bot = 'Верно!'

    return msg_to_bot


def generate_word():
    response = requests.get('https://calculator888.ru/random-generator/sluchaynoye-slovo')
    soup = BeautifulSoup(response.text, 'html.parser')
    a = soup.find_all('div', id='bov')
    return a[0].getText().lower()
