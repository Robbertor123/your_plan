from telebot import TeleBot, types
from datetime import date, timedelta, datetime
import json, threading, time

bot = TeleBot('7227847553:AAEDVszoRoUHIb0s7dEai3M4MNbgkvaUW44')
qaz = {}


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}! ')
    bot.send_message(message.chat.id, 'Этот бот-планировщик напомнит вам о ваших самых важных делах или меропиятиях')
    bot.send_message(message.chat.id, f'Нажмите на /schedule')


@bot.message_handler(commands=['schedule'])
def schedule(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('/help')
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     f'Для того чтобы добавить событие, введите команду /add, название, дату в формате "год-месяц-число" и время события через пробел. \n'
                     'Пример: /add Контрольная 2025-07-09 14:30', reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Команда /today выводит занятия на текущий день.\n'
                                      'Команда /tomorrow — занятия на завтра.\n'
                                      'Команда /week — расписание на всю неделю.\n'
                                      'Команда /add название дата время — сохраняет событие.\n'
                                      '/schedule — информационное сообщение о том, как добавить событие.')


@bot.message_handler(commands=['add'])
def add(message):
    a = (message.text).split()
    if len(a) == 4:
        z = message.from_user.id
        if z not in qaz:
            qaz[z] = {}
            qaz[z].update({f'{a[2]}': []})
            qaz[z][a[2]].append([f'{a[1]}', f'{a[3]}', False])
        else:
            if a[2] not in qaz[z]:
                qaz[z][a[2]] = []
                qaz[z][a[2]].append([f'{a[1]}', f'{a[3]}', False])
            else:
                qaz[z][a[2]].append([f'{a[1]}', f'{a[3]}', False])
        # print(qaz)
        with open('events.json', mode='w', encoding='utf-8') as write_file:
            json.dump(qaz, write_file)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/help')
        markup.add(btn1)
        bot.send_message(message.chat.id, f'Событие успешно добавлено',
                         reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('/schedule')
        markup.add(btn1)
        bot.send_message(message.chat.id, f'Неверное добавление события',
                         reply_markup=markup)


@bot.message_handler(commands=['today'])
def today(message):
    x = date.today().strftime('%Y-%m-%d')
    a = str(message.from_user.id)
    try:
        with open('events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Событий на сегодня не запланировано')
        return
    if a not in data or x not in data[a]:
        bot.send_message(message.chat.id, 'Событий на сегодня не запланировано')
        return
    ev = sorted(data[a][x], key=lambda p: p[1])
    for i in ev:
        bot.send_message(message.chat.id, f'{i[1]} - {i[0]}')


@bot.message_handler(commands=['tomorrow'])
def tomorrow(message):
    x = date.today() + timedelta(days=1)
    xx = x.strftime('%Y-%m-%d')
    a = str(message.from_user.id)
    try:
        with open('events.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Событий на сегодня не запланировано')
        return
    if a not in data or xx not in data[a]:
        bot.send_message(message.chat.id, 'Событий на сегодня не запланировано')
        return
    ev = sorted(data[a][xx], key=lambda p: p[1])
    for i in ev:
        bot.send_message(message.chat.id, f'{i[1]} - {i[0]}')


@bot.message_handler(commands=['week'])
def week(message):
    with open('events.json', 'r') as f:
        data = json.load(f)
    s = []
    sd = {0: ['пн'], 1: ['вт'], 2: ['ср'], 3: ['чт'], 4: ['пт'], 5: ['сб'], 6: ['вс']}
    x = date.today()
    q = x.weekday()
    qq = 6 - q
    for i in range(1, q + 1):
        s.append(str(x - i * timedelta(days=1)))
    for i in range(qq + 1):
        s.append(str(x + i * timedelta(days=1)))
    s.sort()
    for i in range(7):
        sd[i].append(s[i])
    kol = {}

    for k in data.keys():
        if str(k) == str(message.from_user.id):
            for i in data.values():
                for g in i.items():
                    for m in sd.values():
                        if m[1] not in kol:
                            if g[0] == m[1]:
                                if m[1] not in kol:
                                    kol[m[1]] = {}
                                    kol[m[1]].update({f'{m[0]}': []})
                                    kol[m[1]][m[0]].append(g[1])
                                else:
                                    kol[m[1]][m[0]].append(g[1])
    for i in sd.values():
        if i[1] in kol.keys():
            for j in kol.items():
                if i[1] == j[0]:
                    for k in j[1].values():
                        for m in k:
                            for w in m:
                                bot.send_message(message.chat.id, f'{i[1]} - {i[0]} - {w[0]} в {w[1]}')
        else:
            bot.send_message(message.chat.id, f'{i[1]} - {i[0]} - События отсутствуют')


def rexx():
    while True:
        x = datetime.now()
        q = x + timedelta(hours=1)
        try:
            with open('events.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}
        wsx = False
        for id, d in data.items():
            for i, j in d.items():
                if i != q.strftime('%Y-%m-%d'):
                    continue
                for ev in j:
                    n = ev[0]
                    m = ev[1]
                    if len(ev) < 3:
                        ev.append(False)
                    p = ev[2]
                    t = datetime.strptime(f'{i} {m}', '%Y-%m-%d %H:%M')
                    if not p and abs((t - q).total_seconds()) < 60:
                        bot.send_message(int(id), f'Напоминание: {n} начнется через час в {m}')
                        ev[2] = True
                        wsx = True
        if wsx:
            with open('events.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        time.sleep(60)


threading.Thread(target=rexx, daemon=True).start()
bot.polling(none_stop=True)
