
#from time import sleep
import re
import asyncio
from asyncio import sleep
from aiogram.types import ParseMode, callback_query
import aiogram
import sqlite3
from aiogram import Bot, Dispatcher, types
import random
from aiogram import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
#from aiogram import ParseMode, ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.middlewares import BaseMiddleware
from datetime import datetime, timedelta

storage= MemoryStorage()
bot = Bot(token="6083274117:AAGM7Wcs6Wg4fWmJg8RlkLureKV2kO8_h1Q")
dp = Dispatcher(bot, storage=storage)
connect = sqlite3.connect('bd')             #создание бд
c = connect.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, money integer, nik text, status text, inventory integer, strength integer, speed integer, reaction integer, energy integer, travel integer, predel integer, max_energy integer,  weapon text, armor text)')
c.execute('CREATE TABLE IF NOT EXISTS duh (id integer PRIMARY KEY, strength integer, speed integer, reaction integer, energy integer, craft integer)')
c.execute('CREATE TABLE IF NOT EXISTS sklad ( id integer, name text, quantity integer)')
c.execute('CREATE TABLE IF NOT EXISTS items (id_item integer PRIMARY KEY, name text, description text, class text)')
c.execute('CREATE TABLE IF NOT EXISTS mobs (id integer PRIMARY KEY, name text, loot text, health integer, damage integer, speed integer, strength integer, reaction integer)')
c.execute('CREATE TABLE IF NOT EXISTS skils (id integer, name text)')
c.execute('CREATE TABLE IF NOT EXISTS shop ( id integer, name text, quantity integer, price integer, class text)')
c.execute('CREATE TABLE IF NOT EXISTS craft (id integer, name text, recept text, result integer, time integer)')
#my_list = ['menu_kb()', 'citi_kb()', 'movies_kb()', 'friend_kb()', 'setting_kb()']
c.execute('''CREATE TABLE IF NOT EXISTS friends
                (user_id INTEGER, friend_id INTEGER, friend_name text)''')
# Функция добавления друга
def add_friend(user_id, friend_id, friend_name):

    c.execute("INSERT INTO friends (user_id, friend_id, friend_name) VALUES (?, ?, ?)", (user_id, friend_id, friend_name))
    connect.commit()

# Функция удаления друга
def remove_friend(user_id, friend_name):
    c.execute("select friend_id from friends where user_id=? AND friend_name = ? limit 1", (user_id, friend_name))
    info=c.fetchone()
    print(info, friend_name, user_id)
    c.execute("DELETE FROM friends WHERE user_id=? AND friend_name = ?", (user_id, friend_name))
    c.execute("DELETE FROM friends WHERE user_id=? AND friend_id=?", (info[0], user_id))
    connect.commit()

# Функция получения списка друзей
def get_friends(user_id):
    c.execute("SELECT friend_name FROM friends WHERE user_id=?", (user_id,))
    friends = c.fetchall()
    #if friends is None:
    #    return
    return [friend[0] for friend in friends]

#class Midlware(BaseMiddleware):
      #async def on_process_message(self, message: types.Message, data: dict, state: FSMContext)
battle={}
tasks={}
list = []
class Statess(StatesGroup):
    noduh= State()
    wait = State()
    do = State()
    admin= State()
    menu= State()
    battle= State()
    chatt= State()

async def coroutine1(chat_id, n):
        q=0
        qid=int(fid(chat_id)[8]/10)
        if n>qid:
              n=qid
        try:
            for i in range(n):

                await asyncio.sleep(2)
               # c.execute('update users set energy=energy-10 where id=?', (chat_id,))
                connect.commit()
                q+=1
                tasks[chat_id]['quant']=f'{q} {n}'   

            return q    
        except asyncio.CancelledError:
              return q    
              
async def coroutine2(chat_id, time):#(,speed)
        try:
              await asyncio.sleep(time)
              return
        except asyncio.CancelledError:
              return 1
        q=0
        times=7200-(54*speed)
        times=2#tut
        try:
            while True:
                  await asyncio.sleep(times)
                  ivents = [ivent1, ivent2, ivent3]
                  weights = [7, 3, 3]
                  function = random.choices(ivents, weights=weights)[0]
                  
                  await function(chat_id)
                  #await bot.send_message(chat_id, 'вы нашли')#эту строчку нужно удалить
                  q+=1
        except asyncio.CancelledError:
              q=q*times/3600
              c.execute('update users set travel=travel+? where id=?', (q, chat_id))
              connect.commit()
              
async def coroutine3(chat_id):
        q=fid(chat_id)
        q=q[11]-q[8]
        try:
            for i in range(int(q/10)):
                await asyncio.sleep(3)
                c.execute('update users set energy=energy+10 where id=?', (chat_id, ))
                connect.commit()
                print(99)
            print(7)
            c.execute('update users set energy=max_energy where id=?', (chat_id, ))
            connect.commit()
            return True
               
        except asyncio.CancelledError:
              print(9) 
              
async def coroutine4(chat_id, message_id, n):
        
        #qid=int(fid(chat_id)[0][9]/10)
    #    if n>qid:
#              n=qid
        await asyncio.sleep(5)
        q=battle[chat_id]
        try:
            
            while True:
                
                if q[n]['mob_hp']>0 and q['hp']>0:
                    
                    battle[chat_id]['hp']=q['hp']-q[n]['mob_damage']
                    #await bot.edit_message_text(chat_id=chat_id, message_id=message_id+n, text=f'{q["mob_name"]} здоровье: {q["mob_hp"]} ' , reply_markup=ikb)
                    time=datetime.now()-q['time']
                    minutes, seconds = divmod(time.total_seconds(), 60)
                    time=f' {int(minutes)} минут {int(seconds)} секунд'
                    i=1
                    damage=int(q[n]["mob_damage"])
                    while True:
                          try:
                                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]} (-{i* damage})')
             
            #    q+=1
                                await asyncio.sleep(1.5)
                                time=datetime.now()-q['time']
                                minutes, seconds = divmod(time.total_seconds(), 60)
                                time=f' {int(minutes)} минут {int(seconds)} секунд'
                                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]}')
                                await asyncio.sleep(3.5)
                                break
                          except  aiogram.utils.exceptions.MessageNotModified:
                                print('gg')
                                i+=1
                elif q['hp']>0:
                    
                    c.execute('update users set energy=? where id=?', (q["hp"], chat_id))
                    connect.commit()
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id+n, text=f'{q[n]["mob_name"]} pomer')
                    print(1)
                 
                    return 1
                else:break
            
            return 0
        except asyncio.CancelledError:
              print(00)
              
              
    
async def coroutine5(chat_id, name, quant, time):
        try:
            i=0
            while i < quant:
                await asyncio.sleep(2)#vrode zfes time? hz
                c.execute('select recept, result from craft where id=? and name=? limit 1', (chat_id, name))
                recept = c.fetchone()[0]
                resources = [item.strip() for item in recept.split(',')]
                print(resources)
                c.execute("SELECT name, quantity FROM sklad WHERE id=?", (chat_id, ))
                inventory_items=c.fetchall()
                inventory = {item[0]: item[1] for item in inventory_items}
                print(inventory)
                for resource in resources:
                    quantity, names = resource.split()
                    if names not in inventory or inventory[names] < int(quantity):
                          await bot.send_message(chat_id, f'Нехватает {names}')
                          return i
                    if inventory[names] == int(quantity):
                          c.execute('delete from sklad where name=? and id=?', (names, chat_id))
                    else:
                        c.execute('update sklad set quantity=quantity-? where name=? and id=?', (int(quantity), names, chat_id))
                connect.commit()   
                i+=1            
                tasks[chat_id]['quant']=f'{i} {quant}'   
            return i
        except asyncio.CancelledError:
              return i
              
async def ivent1(chat_id):
      N=random.choices([1, 2, 3, 4], weights=[40, 47, 10, 3])[0]
      print(N)
      location=f'Проходя по {random.choices(["тропе" , "лесу", "мрачной тропе"])[0]} вы замечаете '
      if N==1:
            
            await bot.send_message(chat_id, f'{location}блекс, подойдя ближе вы поняли что это был {random.choices(["кусок сломаного меча", "мусор", "кусочек стекла"])[0]}\nВы решили продолжить свои скитания...')
      elif N==2:
            money=random.randint(2, 16)
            await bot.send_message(chat_id, f'{location}{money} монет')
            c.execute('update users set money=money+? where id=?', (money, chat_id))
            
      elif N==3:
            money=random.randint(63, 119)
            await bot.send_message(chat_id, f'{location}мешочек в котором было {money} монет')
            c.execute('update users set money=money+? where id=?', (money, chat_id))
      else:
            money=random.randint(340, 620)
            await bot.send_message(chat_id, f'{location}несколько мешочков присыпаных землей\nЩищщ  вы собрали {money} монет')
            c.execute('update users set money=money+? where id=?', (money, chat_id))
      connect.commit()
      #c.execute('select ')
      #вы нашли монеты
async def ivent2(chat_id):
      N=random.choices([1, 2, 3, 4], weights=[40, 47, 10, 3])[0]
      loc='Вы наткнулись на поляну\n'
      if N==1:
          await bot.send_message(chat_id, f'{loc}Но  нечего интересного так и не нашли')
      elif N==2:
            await bot.send_message(chat_id, f'{loc}По итогу вы собрали несколько трав')#нужно сделать рандом на количество
      elif N==3:
            await bot.send_message(chat_id, f'{loc}Уже собираясь уходить вы замичаете что-то')
      else:
            await bot.send_message(chat_id, f'{loc}Чательно поискав вы назодите ...')
      #вы нашли поле с интересными травами
async def ivent3(chat_id):
       #      ikb.add(InlineKeyboardButton(text='Войти в пещеру', callback_data='next'))
      N=random.choices([1, 2, 3, 4], weights=[40, 47, 10, 3])[0]
      loc='Вы нашли пещеру\n'
      if N==1:
           await bot.send_message(chat_id, f'{loc}Но там нечего не было')
           return
      if chat_id in list:
                                    list.remove(chat_id)
                                    await bot.send_message(chat_id, 'Вы вышли из чата')#, reply_markup=do_kb())
      kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
      kb.add(KeyboardButton('Войти'), KeyboardButton('Уйти'))
      if N==2:
           await bot.send_message(chat_id, f'{loc}dange1', reply_markup=kb)#мб можно удплять сообщения через пол часа. но нету мессадж ид, можно запихнуть что бы удалять сообщение перед отправкой нового в путешествии, нг тоже там свои нюансы, хз
           return 'dange1 1'
      if N==3:
            await bot.send_message(chat_id, f'{loc}dange2', reply_markup=kb)
            return 'dange2 1'
      else:
            await bot.send_message(chat_id, f'{loc}dange3', reply_markup=kb)
            return 'dange3 1'
      #await bot.send_message(chat_id, f'Вы нашли пещеру')
      #вы нашли пещеру(мб с рудой и мобамиили только с рудой или только с мобами)
async def ivent4(chat_id):
      N=random.choices([1, 2, 3, 4], weights=[40, 47, 10, 3])[0]
      kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
      if N==1:
            await bot.send_message(chat_id, 'В далеке вы замеиили групу людей\nНемного подумав вы решили их обойти' )
            return
      if chat_id in list:
                                    list.remove(chat_id)
                                    await bot.send_message(chat_id, 'Вы вышли из чата')
      if N==2:
           # ikb= InlineKeyboardMarkup(row_width=3)
            #ikb.add(InlineKeyboardButton(text='Напасть', callback_data='next'), InlineKeyboardButton(text='Уйти', callback_data='run1'))
            kb.add(KeyboardButton('Напасть'), KeyboardButton('Уйти'))
            N=random.choices([2, 3, 4, 5], weights=[40, 47, 10, 3])[0]
            await bot.send_message(chat_id, f'Вы замечаете дым от костра. Подойдя вы поняли что это разбойники устрили себе привал. \nВсего вы насчитали {N} разбойников', reply_markup=kb)
            return f'banda{N} 1'
      elif N==3:
         #   ikb= InlineKeyboardMarkup(row_width=3)
            #ikb.add(InlineKeyboardButton(text='Напасть', callback_data='next'), InlineKeyboardButton(text='Попробовать сбежать', callback_data='run2')).add( InlineKeyboardButton(text='Отдать монеты', callback_data='loss_money'), InlineKeyboardButton(text='Отказатся', callback_data='loss_hp'))
            kb.add(KeyboardButton('Напасть'), KeyboardButton('Попробовать сбежать'), KeyboardButton('Отдать монеты'))
            await bot.send_message(chat_id, 'Вы попали в засаду. Вас окружило шестеро разбойников.\n Тебе приказали отдать 70% монет в качестве "налога"', reply_markup=kb)
            return 'banda6 1'
      else:
            c.execute(f'select * from sklad where id={chat_id}')
            item=random.choices(c.fetchall())[0]
            n=random.randint(1, item[1])#там где айьем1 хз, там должно быть количество предмета, но я не знаю точно что количество под индексом 1...я спать, бб
            await bot.send_message(chat_id, f'°-°\nНа тебя выбежало четверо разбойников, пока трое переводили твое внимание на себя четвертый смог украсть у тебя {n} {item[0]}\nВсе произошло так быстро что ты сразу так и не понял(а) что произошло, а разбойники уже скрылись.')
            if n<item[1]:
                  c.execute(f'update sklad set quantity=quantity-n where id={chat_id} and name=?', (item[0]))
            else:
                  c.execute(f'delete from sklad where name=? and id={chat_id}', (item[0]))
            connect.commit()
            #пон, слишком сложно-#типл заснул, а другие игроки могут его найти  и решиьь обаоруют они его или зашитчт пока онтне проснется
            #await bot.send_message(chat_id, 'Почуствовав некую усталость вы решили немного поспать')
           # sleep_list.append(chat_id)
           # c.execute(f'select speed from users where id={chat_id} limit 1')
          #  await asyncio.sleep(7200-54*c.fetchone()[0])
         #   sleep_list.remove(chat_id)
      #на вас напали разбойники
async def ivent5(chat_id):#можно дать аообщение с классами предметов и потоп ввбрать 5 самыз дорогих из этого класа и дкм ткидку в 20% либо еще чет можно придумать
    #  N=random.choices(['Сферы', 'Оружие', 'Другое', 'Одежда', 'Ресурсы'])[0]
#      print(N)
   #   c.execute('SELECT DISTINCT name FROM shop where class=?', (N, ))
   #   q=c.fetchall()
     # if not q :
       #       await bot.send_message(chat_id, 'Вы встретили торговца, но он уже все распродал')
      #        return
      kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
      kb.add(KeyboardButton('Взгленуть'), KeyboardButton('Уйти'))
      #ikb= InlineKeyboardMarkup(row_width=3)
      #for i in q:
        #    c.execute('SELECT price FROM shop WHERE name = ? ORDER BY price ASC LIMIT 1', (i[0], ))
            #ikb.add(InlineKeyboardButton(text=f'{i[0]} - {int(c.fetchone()[0]*70/100)}', callback_data='by'))#вообще нужно записать в спивок а дальше вызвать функцию по типу чанков только для индайн клавиатуры, у меня такой  сечас нету.
      await bot.send_message(chat_id, 'Вы встретили торговца\nОн предложил вам взгленуть на его товары', reply_markup=kb)
      return 'shop'
      #мб вы встретили торговца и mоzeте что-то купить
async def ivent6(chat_id):
      #поидеи сделать нескольно вприантов, и в разных вариантах разные дейтвия приедут либо к награде либо к меньщей награду либо к какойто потери либо к силтной потере
      await bot.send_message(chat_id, 'текст')
      # вы увидели как кто-то работает с печью
def shop_kb():
    shop_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    shop_kb.add(KeyboardButton('Оружие'), KeyboardButton('Одежда'), KeyboardButton('Сферы')). add(KeyboardButton('Ресурсы'), KeyboardButton('Продать'), KeyboardButton('Другое')).add(KeyboardButton('Назад'))
    return shop_kb
def chat_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Назад'))
    return kb
def friend_kb(chat_id):
    c.execute('UPDATE users SET status = "friends" WHERE id = ?', (chat_id, ))
    connect.commit()
    friends = get_friends(chat_id)
    kb_group = [KeyboardButton(f'{friend}') for friend in friends]
    return chunks(kb_group, 3)
def menu_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Город'), KeyboardButton('Действия'), KeyboardButton('Друзья')).add(KeyboardButton('Настройки'), KeyboardButton('Профиль'))
    return kb
def citi_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Рейтинг'), KeyboardButton('Ивенты'), KeyboardButton('Кузня')).add(KeyboardButton('Торговый квартал'), KeyboardButton('Чат'), (KeyboardButton('Работа'))).add(KeyboardButton('Назад'))
    return kb
def movies_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Путешествие'), KeyboardButton('Тренировка'), KeyboardButton('Поглошение енергии')).add(KeyboardButton('Назад'))
    return kb

def quant_kb(q):#quantity==q
      kb =ReplyKeyboardMarkup(resize_keyboard=True)
      if q==1:
            kb.add(KeyboardButton('1'))
      elif q==2:
              kb.add(KeyboardButton('1'), KeyboardButton('2'))
      elif q>2:
              kb.add(KeyboardButton('1'), KeyboardButton(f'{int(q/2)+1}'), KeyboardButton(f'{q}'))
      kb.add(KeyboardButton('Назад'))
      return kb
def chunks(spisok, size):# имба крч, даешь список из кнопок, и сколько их нужео в ряде, тебе кают клавиатуру с несколькими рядами
    group=[spisok[i:i+size] for i in range(0, len(spisok), size)]
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Назад'))
    if size==3:
          kb.add(KeyboardButton('Добавить'))
    for g in group:
        kb.row(*g)
    return kb

def chunks_ikb(spisok, size):#абалдетб если будет раюотать, но скорее всего не будет), нужео поменять там где я выдаю список с лутом и сферами
    group=[spisok[i:i+size] for i in range(0, len(spisok), size)]
    ikb= InlineKeyboardMarkup(row_width=3)
    for g in group:
        stroka=[]
        for dat in g:
              stroka.append(InlineKeyboardButton(text=dat, callback_data=dat))#если не юудет раюотать можно ужалмть инлайн кейюоард буттон, и оставить тольнл техт и калбек, но хз, может онг добавиь сразц 2 записи в список(изза того чтл между текстом и калбеком запятая)
        ikb.row(*stroka)
    return ikb
    
def setting_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Сменить никнейм'), KeyboardButton('hz')).add(
        KeyboardButton('Назад'))
    return kb
def profile_kb():
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Инвентарь')).add(KeyboardButton('Назад'))
    return kb
#def dange_kb(): kb=ReplyKeyboardMarkup(resize_keyboard=True)
#    kb.add(KeyboardButton(''), KeyboardButton('')).add(KeyboardButton('Назад'))
 #   return kb
def delete_ikb():
    ikb= InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text='Удалить сообщение', callback_data='delete'))
    return ikb
def fid(fid):
    c.execute(f'SELECT * FROM users WHERE id = {fid} limit 1')
    return c.fetchone()
startt = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
startt.add(KeyboardButton('/help'), KeyboardButton('Faq')).add(KeyboardButton('/menu'))

def add_sklad(chat_id, item, q):
    c.execute('select * from sklad where id=? and name=? limit 1' , (chat_id, item))#дописал лимит 1, дело было ночью, хз можнт не надо было 
    
    if c.fetchone() is not None:
        c.execute("UPDATE sklad SET quantity=quantity+? WHERE id = ? and name = ?", (q, chat_id, item))
        connect.commit()
        print(88)
    else:
        
        c.execute("INSERT INTO sklad (id, name, quantity) VALUES (?, ?, ?)", (chat_id, item, q))
        connect.commit()
        print(77)
def do_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Информаця')).add(KeyboardButton('Настройки'), KeyboardButton('Друзья'), KeyboardButton('Профиль')).add(KeyboardButton('Чат'))
    return kb
def atak_ikb():
    ikb=InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text='Атаковать', callback_data='ataka'),  InlineKeyboardButton(text='Уворот', callback_data='run'))
    return ikb
#первая цифра это этаж,лвл, а следуйший список это список мобов, точнее их ид
sleep_list=[]
danges={'dange1': {
    1: [1], 
    2: [1, 2], 
    3: [1, 2, 3]
}, 
    'dange2': {1: [3], 2: [3, 3], 3: [3, 3, 3] }, 
    'dange3': {1: [1], 2: [1, 3], 3: [1, 1, 3] }, 
    'banda2': {1: [1, 1]}, 
    'banda3': {1: [1, 1, 1]}, 
    'banda4': {1: [1, 1, 1, 1]}, 
    'banda5': {1: [1, 1, 1, 1], 2: [1]}, 
    'banda6': {1: [1, 1, 1, 1], 2: [1, 1]}
    }

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    # Получаем информацию о фото
    photo = message.photo[-1]  # Берем последнюю доступную версию фото
    print(photo)
    photo_id = photo.file_id

    # Отправляем фото пользователю вместе с его описанием
    await bot.send_photo(chat_id=message.from_user.id, photo=photo_id, caption=photo_id)

@dp.callback_query_handler(lambda c: c.data == 'ending', state=Statess.do)
async def process_callback_button(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        chat_id=callback_query.message.chat.id
        if data['movie']=='travel':
              data['movie']='go_home'
              await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id, text='Вы отправились домой')
              return
        data['last'] = 'menu_kb()'
        data['last_message'] = ''
        del data['movie']
        print(data)
    if chat_id in tasks:
        task = tasks[chat_id]['coroutine']
        task.cancel()
        # tasks.pop(message.chat.id)
    await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id, text='вы отменили все свои действия')
    await callback_query.answer('пон')
    await Statess.menu.set()#////////////////////////////еще нужно постваиьь какуэто провкрку, так как чкд может сохранитб это сообщение а потом в бою нажать , юл ладно это бред усталого человека, я не удалил потому что мб нет. но когда в бою то у тебя включен статус боя а не децствий так что оно сюда не зайдет
   # print(chat_id, message_id)
    c.execute('UPDATE users SET status = "menu" WHERE id = ?', (callback_query.message.chat.id, ))
    connect.commit()
    #await bot.send_message(message_id , 'Сейчас вы на работе {quant[0]}/{quant[1]}\n{time}')
    #await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Вы завершили все свои действия', reply_markup=menu_kb())
        # tasks.pop(message.chat.id)

@dp.callback_query_handler(lambda c: c.data == 'by', state=Statess.do)#если что то это не работет
async def process_callback_button(callback: types.CallbackQuery, state: FSMContext):
    chat_id=callback.message.chat.id
    n=callback.data.text.split(' - ')
    c.execute(f'select money from users where id={chat_id} limit 1')
    if int(n[1])>c.fetchone()[0]:
          await bot.send_message(chat_id, f'Вам нехватает монет для покупки {n[0]}')
          return
    last_ikb = callback.message.reply_markup.inline_keyboard
    add_sklad(chat_id, n[0], 1)
    c.execute(f'update users set money = money-{int(n[1])} where id={chat_id} limit 1')
    connect.commit()
    for row in last_ikb:
                    if row[0].text == f'{callback.text}':
                            del row[0]
    await bot.edit_message_text(chat_id=chat_id, message_id=callback_query.message.message_id, text=f'Вы преобрели {n[0]}', reply_markup=last_ikb)
    
#@dp.message_handler()
#async def menu(message: types.Message, state: FSMContext):
    #chat_id=message.chat.id
    #add_sklad(chat_id, f'{message.text}', 1)
    
@dp.message_handler(Text(equals='Информаця'), state=Statess.do)
async def menu(message: types.Message, state: FSMContext):
    chat_id=message.chat.id
  #  if len(tasks[chat_id])==3:
    #    quant=tasks[chat_id]['quant'].split()
    time= tasks[chat_id]['time']-datetime.now()
    hours, remainder = divmod(time.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    ikb=InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text='Завершить', callback_data='ending'), InlineKeyboardButton(text='Удалить сообщение', callback_data='delete')) #kb=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Завершить')).add(KeyboardButton('Назад'))
    async with state.proxy() as data:
        do=data['movie']
        data['last']='do_kb()'
    time=f'Осталось: {int(hours)} часов {int(minutes)} минут {int(seconds)} секунд'#если в путишествии норм пишется, типо целые числа, то и тут убрать фкнкцию инт
    if do=='Работа':
        quant=tasks[chat_id]['quant'].split()
        await message.answer(f'Сейчас вы на работе {quant[0]}/{quant[1]}\n{time}', reply_markup=ikb)
    elif do == 'travel':#еслии я не запускаю корутину тг можно просто в таск звписать время...
        time= datetime.now()- tasks[chat_id]['time']
        hours, remainder = divmod(time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        await message.answer(f'Ты уже путишествуешь {hours} часов {minutes} минут {seconds} секунд', reply_markup=ikb)
    elif do == 'craft':
        quant=tasks[chat_id]['quant'].split()
        await message.answer(f'Вы сейчас создаете предмет {quant[0]}/{quant[1]}\n{time}', reply_markup=ikb)
    elif do=='energy':
        c.execute('select energy, max_energy from users where id=? limit 1', (message.chat.id, ))
        inf=c.fetchone()
        await message.answer(f'Сейчас вы востанавливаете енергию {int(inf[0]/10)}/{int(inf[1]/10)}\n{time}',
                             reply_markup=ikb)
    else:
        quant=tasks[chat_id]['quant'].split()
        await message.answer(f'Сейчас вы Тренируетесь {quant[0]}/{quant[1]}\n{time}',
                             reply_markup=ikb)
                             
@dp.callback_query_handler(lambda c: c.data == 'loot', state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext):
    chat_id=callback.message.chat.id
    message_id=callback.message.message_id
    async with state.proxy() as data:
                    loot=data['loot'].split(',')
                    print(loot)
    ikb=InlineKeyboardMarkup(row_width=3)
    for buttonn in loot:
          print(buttonn)
          if buttonn=='':
                break
          ikb.add(InlineKeyboardButton(text=f'{buttonn}', callback_data=f'{buttonn}'))
    ikb.add(InlineKeyboardButton(text='❌', callback_data='close'))
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='👀', reply_markup=ikb)

@dp.message_handler(state=Statess.do)
async def menu(message: types.Message, state: FSMContext):
     chat_id=message.chat.id
     mtext=message.text
     message_id=message.message_id
     async with state.proxy() as data:
                    dat=data['last']
     if mtext=='Взгленуть' and dat=='shop':
            async with state.proxy() as data:
                    data['last']='do_kb()'
            N=random.choices(['Сферы', 'Оружие', 'Другое', 'Одежда', 'Ресурсы'])[0]
            print(N)
            c.execute('SELECT DISTINCT name FROM shop where class=?', (N, ))
            q=c.fetchall()
            if not q :
                    await bot.send_message(chat_id, 'Он посмотрел на оставшийся товар и осознал что уже всё распродал, извенился и подарил вам сферу', reply_markup=do_kb())
                    add_sklad(chat_id, "Сфера", 1)
                    return
            ikb= InlineKeyboardMarkup(row_width=3)
            for i in q:
                  c.execute('SELECT price FROM shop WHERE name = ? ORDER BY price ASC LIMIT 1', (i[0], ))
                  ikb.add(InlineKeyboardButton(text=f'{i[0]} - {int(c.fetchone()[0]*70/100)}', callback_data='by'))
            await bot.send_message(chat_id, N, reply_markup=ikb)
     elif mtext=='Уйти':
            async with state.proxy() as data:
                    data['last']='do_kb()'
            await bot.send_message(chat_id, 'Вы продолжили свои скитания', reply_markup=do_kb())
     if len(dat.split())!=2:
           await message.answer('ne pon')
           return
     if mtext=='Напасть' or mtext=='Войти':
          if chat_id not in battle:
               await Statess.battle.set()
               c.execute('select energy from users where id=?', (chat_id, ))
               hp=c.fetchone()[0]
               battle[chat_id]={'time': datetime.now(), 'hp': hp, 'time_atak': 1, 'ataka': 1, 'dodge': 1}# здемь нужно обратится к бд и из бд взять кодичесто проаодимых атак 
               async with state.proxy() as data:
                     data['last_message']=message_id
                     dat=data['last'].split()
                     data['movie']='battle'
          else:
               await message.answer('tu uge v boyu')
               await bot.delete_message(chat_id, message_id)
               return
          dange=dat[0]
          lvl=int(dat[1])
          coroutines=[]
          count_mobs={}
          mobs=danges[dange][lvl]
          print(len(danges[dange][lvl]), mobs)
          q=battle[chat_id]
          time=datetime.now()-q['time']
          minutes, seconds = divmod(time.total_seconds(), 60)
          time=f' {int(minutes)} минут {int(seconds)} секунд'
          await bot.send_message(chat_id=chat_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]}')
          del time, minutes, seconds
          for i in range(len(danges[dange][lvl])):
                   n=i+1
                   c.execute('select * from mobs where id=? limit 1', (random.choice(mobs), ))
                   mob=c.fetchone()
                   battle[chat_id][n] = {
                       'coroutine': asyncio.create_task(coroutine4(chat_id, message.message_id+1, n)),
                       'mob_name': mob[1], 
                       'mob_hp': mob[3],
                       'mob_damage': mob[4]}
                   ikb=InlineKeyboardMarkup(row_width=3)
                   ikb.add(InlineKeyboardButton(text='Атаковать', callback_data=f'{n}'),  InlineKeyboardButton(text='Уворот', callback_data='dodge'))
                   await bot.send_message(chat_id, f' {mob[1]}, здоровье: {mob[3]}' , reply_markup=ikb)
                   if mob[1] in count_mobs:
                         count_mobs[mob[1]]+=1
                   else:
                         print('add mob in mobbbs')
                         count_mobs[mob[1]]=1
                   print(count_mobs)
                   coroutines.append(battle[chat_id][n]['coroutine'])
          loott={}
          for mobb in count_mobs:
                print(mobb)
                c.execute(f'select loot from mobs where name="{mobb}" limit 1')
                lot=c.fetchone()[0].split(',')
                if lot !='':
                      for loot in lot:
                            loot=loot.split('-')
                            if loot[0] not in loott:
                                  loott[loot[0]]= int(loot[1])*count_mobs[mobb]
                            else:
                                  loott[loot[0]]=loott[loot[1]]+int(loot[1])*count_mobs[mobb]
          async with state.proxy() as data:
               data['loot']=''
               for loot in loott:
                     data['loot']=data['loot']+f'{loot} - {loott[loot]},'
          del count_mobs
          del loott
          info=await asyncio.gather(*coroutines)
          print(info)
          for inf in info:
               if inf is None or inf==0:
                   for n in range(len(battle[chat_id])-5):
                              i=n+1
                              battle[chat_id][i]['coroutine'].cancel()
                        
                              await bot.delete_message(chat_id, message_id+i)
                   await bot.send_message(chat_id, 'Вы погибли')    #а еще нужно обновить енергию до 0
                   tasks[chat_id].cancel()
                   tasks.pop(chat_id)
                   battle.pop(chat_id)
                   return
          if len(danges[dange])==lvl:
              time=datetime.now()-q['time']
              minutes, seconds = divmod(time.total_seconds(), 60)
              time=f' {int(minutes)} минут {int(seconds)} секунд'
              await bot.send_message(chat_id, f'win, time: {time}', reply_markup=citi_kb())
              await Statess.menu.set()
              battle.pop(chat_id)
              async with state.proxy() as data:
                   del data['loot']
                   data['movie']='travel'
              return
          async with state.proxy() as data:
                    data['last']=f'{dange} {lvl+1}'
          ikb2=InlineKeyboardMarkup(row_width=3)
          ikb2.add(InlineKeyboardButton(text='Идти дальshе', callback_data=f'next'),  InlineKeyboardButton(text='Сферы', callback_data='Сферы'), InlineKeyboardButton(text='Лутец', callback_data=f'loot'))
          await bot.send_message(chat_id, 'next', reply_markup=ikb2)
     elif mtext=="Попробовать сбежать":
         async with state.proxy() as data:
                    data['last']='do_kb()'
         c.execute(f'select speed from users where id={chat_id} limit 1')
         if c.fetchone()[0]>60:
                  N=random.randint(1, 2)
                  if N==1:
                        await bot.send_message(chat_id, 'Вам удалось сбежать', reply_markup=do_kb())
                        return
         if chat_id not in battle:
                await Statess.battle.set()
                c.execute('select energy from users where id=?', (chat_id, ))
                hp=c.fetchone()[0]
                battle[chat_id]={'time': datetime.now(), 'hp': hp, 'time_atak': 1, 'ataka': 1, 'dodge': 1}# здемь нужно обратится к бд и из бд взять кодичесто проаодимых атак 
                async with state.proxy() as data:
                     data['last_message']=message_id
                     dat=data['last'].split()
                     data['movie']='battle'
         else:
               async with state.proxy() as data:
                    dat=data['last'].split()
                    last_messag=data['last_message']
                    print(last_messag)
                    data['last_message']=message_id
               await bot.delete_message(chat_id, last_messag)
               for i in range(len(battle[chat_id])-5):
                    del battle[chat_id][i+1]
                    print(i)
                    await bot.delete_message(chat_id, last_messag+i+1)
         dange=dat[0]
         lvl=int(dat[1])
         coroutines=[]
         count_mobs={}
         mobs=danges[dange][lvl]
         print(len(danges[dange][lvl]), mobs)
         q=battle[chat_id]
         time=datetime.now()-q['time']
         minutes, seconds = divmod(time.total_seconds(), 60)
         time=f' {int(minutes)} минут {int(seconds)} секунд'
         await bot.send_message(chat_id=chat_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]}')          
         for i in range(len(danges[dange][lvl])):
                   n=i+1
                   c.execute('select * from mobs where id=? limit 1', (random.choice(mobs), ))
                   mob=c.fetchone()
                   battle[chat_id][n] = {
                       'coroutine': asyncio.create_task(coroutine4(chat_id, message.message_id+1, n)),
                       'mob_name': mob[1], 
                       'mob_hp': mob[3],
                       'mob_damage': mob[4]}
                   ikb=InlineKeyboardMarkup(row_width=3)
                   ikb.add(InlineKeyboardButton(text='Атаковать', callback_data=f'{n}'),  InlineKeyboardButton(text='Уворот', callback_data='dodge'))
                   await bot.send_message(chat_id, f' {mob[1]}, здоровье: {mob[3]}' , reply_markup=ikb)
                   if mob[1] in count_mobs:
                         count_mobs[mob[1]]+=1
                   else:
                         print('add mob in mobbbs')
                         count_mobs[mob[1]]=1
                   print(count_mobs)
                   coroutines.append(battle[chat_id][n]['coroutine'])
         loott={}
         for mobb in count_mobs:
                print(mobb)
                c.execute(f'select loot from mobs where name="{mobb}" limit 1')
                lot=c.fetchone()[0].split(',')
                if lot !='':
                      for loot in lot:
                            loot=loot.split('-')
                            if loot[0] not in loott:
                                  loott[loot[0]]= int(loot[1])*count_mobs[mobb]
                            else:
                                  loott[loot[0]]=loott[loot[1]]+int(loot[1])*count_mobs[mobb]
         async with state.proxy() as data:
               data['loot']=''
               for loot in loott:
                     data['loot']=data['loot']+f'{loot} - {loott[loot]},'
         del count_mobs
         del loott
         info=await asyncio.gather(*coroutines)
         print(info)
         for inf in info:
               if inf is None or inf==0:
                   for n in range(len(battle[chat_id])-5):
                              i=n+1
                              battle[chat_id][i]['coroutine'].cancel()
                        
                              await bot.delete_message(chat_id, message_id+i)
                   await bot.send_message(chat_id, 'Вы погибли')    #а еще нужно обновить енергию до 0
                   tasks[chat_id].cancel()
                   tasks.pop(chat_id)
                   battle.pop(chat_id)
                   return
         if len(danges[dange])==lvl:
              time=datetime.now()-q['time']
              minutes, seconds = divmod(time.total_seconds(), 60)
              time=f' {int(minutes)} минут {int(seconds)} секунд'
              await bot.send_message(chat_id, f'win, time: {time}', reply_markup=citi_kb())
              await Statess.menu.set()
              battle.pop(chat_id)
              async with state.proxy() as data:
                   del data['loot']
                   data['movie']='travel'
              return
         async with state.proxy() as data:
                    data['last']=f'{dange} {lvl+1}'
         ikb2=InlineKeyboardMarkup(row_width=3)
         ikb2.add(InlineKeyboardButton(text='Идти дальshе', callback_data=f'next'),  InlineKeyboardButton(text='Сферы', callback_data='Сферы'), InlineKeyboardButton(text='Лутец', callback_data=f'loot'))
         await bot.send_message(chat_id, 'next', reply_markup=ikb2)
     elif mtext=='Отдать монтеты':
            async with state.proxy() as data:
                    data['last']='do_kb()'
            c.execute(f'update set money=money*30/100 from users whete id={chat_id} limit 1')
            connect.commit()
            await message.answer('Тебя поблагодорили и позвоили пройти дальше)', reply_markup=do_kb())
     elif mtext=='Отказатся':
            async with state.proxy() as data:
                    data['last']='do_kb()'
            c.execute(f'select energy from users where id={chat_id} limit 1')
            q=c.fetchone()[0]
            if q>70:
                  c.execute(f'update set energy=energy-70 from users where id={chat_id} limit 1')
                  connect.commit()
                  await message.answer(f'Вы потеряли 7 едениц енергии.\n Осталось {int((q-70)/10)}', reply_markup=do_kb())
                  return
            await Statess.noduh.set()
            async with state.proxy() as data:
                    data['movie']='die'
            c.execute(f'update set energy=0 from users where id={chat_id} limit 1')
            connect.commit()
            await message.answer('Вы погибли')
@dp.message_handler(Text(equals='Данж'), state='*')
async def menu(message: types.Message, state: FSMContext):
    ikb=InlineKeyboardMarkup(row_width=3)
    ikb.add(InlineKeyboardButton(text='ining', callback_data=f'next'),  InlineKeyboardButton(text='т', callback_data='run'))
    chat_id=message.chat.id
    message_id= message.message_id
    await Statess.battle.set()
    await message.answer('go', reply_markup=ikb)
    async with state.proxy() as data:
                    data['last']='dange1 1'
    return
@dp.callback_query_handler(lambda c: c.data == 'close', state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext):
         chat_id=callback.message.chat.id
         message_id=callback.message.message_id
         ikb=InlineKeyboardMarkup(row_width=3)
         ikb.add(InlineKeyboardButton(text='dalshe', callback_data=f'next'),  InlineKeyboardButton(text='Сферы', callback_data='Сферы'), InlineKeyboardButton(text='loot', callback_data='loot'))
         await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='next', reply_markup=ikb)
         
@dp.callback_query_handler(lambda c: c.data == 'Сферы', state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext):
         chat_id=callback.message.chat.id
         message_id=callback.message.message_id
         c.execute('select name from items where class = "Сферы"')
         q=c.fetchall()
         print(q)
         ikb=InlineKeyboardMarkup(row_width=3)
         for i in q:
               print(i)
               c.execute(f'select * from sklad where name ="{i[0]}" and id={chat_id}')
               info=c.fetchone()
               print(info)
               if q:
                     ikb.add(InlineKeyboardButton(text=f'{info[1]} - {info[2]}', callback_data=f'{info[1]} - {info[2]}'))
         ikb.add(InlineKeyboardButton(text='❌', callback_data=f'close'))
         await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='°-°', reply_markup=ikb)
         
@dp.message_handler(state=Statess.battle)
async def menu(message: types.Message, state: FSMContext):
    await message.answer(f'tu tupoi? ti v bitve,{message.message_id}')
    chat_id= message.chat.id
    messag=message.message_id
    await bot.delete_message(chat_id=chat_id, message_id=messag)
    await asyncio.sleep(1)
    await bot.delete_message(chat_id=chat_id, message_id=messag+1)
    
@dp.callback_query_handler(lambda c: c.data == 'next', state=[Statess.battle, Statess.do, ])
async def cl_start(callback: types.callback_query, state: FSMContext):
         chat_id=callback.message.chat.id
         message_id=callback.message.message_id
         #await bot.edit_message_text(chat_id, mesage_id, 'idu tuda...')
        # async with state.proxy() as data:
                #    dat=data['movie'].split()
                   # last_messag=data['last_message']
                    #data['last_message']=message_id
         if chat_id not in battle:#млжно добавить and get_stste==do:
               await Statess.battle.set()
               c.execute('select energy from users where id=?', (chat_id, ))
               hp=c.fetchone()[0]
               battle[chat_id]={'time': datetime.now(), 'hp': hp, 'time_atak': 1, 'ataka': 1, 'dodge': 1}# здемь нужно обратится к бд и из бд взять кодичесто проаодимых атак 
               async with state.proxy() as data:
                     data['last_message']=message_id
                     dat=data['last'].split()
               #     data['movie']='dange1 1'
             #  dat='dange1 1'.split()
         else:
               async with state.proxy() as data:
                    dat=data['last'].split()
                    last_messag=data['last_message']
                    print(last_messag)
                    data['last_message']=message_id
               await bot.delete_message(chat_id, last_messag)
               for i in range(len(battle[chat_id])-5):
                    del battle[chat_id][i+1]
                    print(i)
                    await bot.delete_message(chat_id, last_messag+i+1)
                    
         dange=dat[0]
         lvl=int(dat[1])
         coroutines=[]
         count_mobs={}
         mobs=danges[dange][lvl]
         print(len(danges[dange][lvl]), mobs)
         q=battle[chat_id]
         time=datetime.now()-q['time']
         minutes, seconds = divmod(time.total_seconds(), 60)
         time=f' {int(minutes)} минут {int(seconds)} секунд'
      #   await bot.delete_message(chat_id, message_id-1)
       #  await bot.send_message(chat_id, f'Время: {time}\nМоё здоровье: {q["hp"]}', reply_markup=types.ReplyKeyboardRemove())
         await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]}')          
      #   await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Время: {time}\nМоё здоровье: {q["hp"]}', reply_markup=types.ReplyKeyboardRemove())
         for i in range(len(danges[dange][lvl])):
                   n=i+1
                   c.execute('select * from mobs where id=? limit 1', (random.choice(mobs), ))
                   mob=c.fetchone()
                   battle[chat_id][n] = {
                       'coroutine': asyncio.create_task(coroutine4(chat_id, message_id, n)),
                       'mob_name': mob[1], 
                       'mob_hp': mob[3],
                       'mob_damage': mob[4]}
                   ikb=InlineKeyboardMarkup(row_width=3)
                   ikb.add(InlineKeyboardButton(text='Атаковать', callback_data=f'{n}'),  InlineKeyboardButton(text='Уворот', callback_data='dodge'))
                   await bot.send_message(chat_id, f' {mob[1]}, здоровье: {mob[3]}' , reply_markup=ikb)
                   if mob[1] in count_mobs:
                         count_mobs[mob[1]]+=1
                   else:
                         print('add mob in mobbbs')
                         count_mobs[mob[1]]=1
                   print(count_mobs)
                   coroutines.append(battle[chat_id][n]['coroutine'])
         #kb=ReplyKeyboardMarkup(resize_keyboard=True)
        # kb.add(KeyboardButton('Первый сил и третьий'))
      #   await bot.send_message(chat_id,'начинаем', reply_markup=kb)
       #  await bot.delete_message(chat_id, message_id+len(danges[dange][lvl])+1)
         loott={}
         for mobb in count_mobs:
                print(mobb)
                c.execute(f'select loot from mobs where name="{mobb}" limit 1')
                lot=c.fetchone()[0].split(',')
                if lot !='':
                      for loot in lot:
                            loot=loot.split('-')
                            if loot[0] not in loott:
                                  loott[loot[0]]= int(loot[1])*count_mobs[mobb]
                            else:
                                  loott[loot[0]]=loott[loot[1]]+int(loot[1])*count_mobs[mobb]
         async with state.proxy() as data:
               data['loot']=''
               for loot in loott:
                     data['loot']=data['loot']+f'{loot} - {loott[loot]},'
         del count_mobs
         del loott
         info=await asyncio.gather(*coroutines)
         print(info)
         for inf in info:
               if inf is None or inf==0:
                   for n in range(len(battle[chat_id])-5):
                              i=n+1
                              battle[chat_id][i]['coroutine'].cancel()
                        
                              await bot.delete_message(chat_id, message_id+i)
                   await bot.send_message(chat_id, 'Вы погибли')    #а еще нужно обновить енергию до 0
                   tasks[chat_id].cancel()
                   tasks.pop(chat_id)
                   battle.pop(chat_id)
                   return
         # async with state.proxy() as data:
                # data['movie']=f'dange1 {lvl+1}'
         if len(danges[dange])==lvl:
              time=datetime.now()-q['time']
              minutes, seconds = divmod(time.total_seconds(), 60)
              time=f' {int(minutes)} минут {int(seconds)} секунд'
              await bot.send_message(chat_id, f'win, time: {time}', reply_markup=citi_kb())
              await Statess.menu.set()
              battle.pop(chat_id)
              async with state.proxy() as data:
                   del data['loot']
                   data['movie']='travel'
              return
         async with state.proxy() as data:
                    data['last']=f'{dange} {lvl+1}'
         ikb2=InlineKeyboardMarkup(row_width=3)
         ikb2.add(InlineKeyboardButton(text='Идти дальshе', callback_data=f'next'),  InlineKeyboardButton(text='Сферы', callback_data='Сферы'), InlineKeyboardButton(text='Лутец', callback_data=f'loot'))
         await bot.send_message(chat_id, 'next', reply_markup=ikb2)

@dp.callback_query_handler( state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext):
    chat_id=callback.message.chat.id
    message_id=callback.message.message_id

    
@dp.callback_query_handler(lambda c: c.data == 'dodge', state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext):
         chat_id=callback.message.chat.id
         if battle[chat_id]['dodge'] != 1:
               await callback.answer('Подождите 10 секунд с последнего уворота')
               return
         battle[chat_id]['dodge']=0
         await callback.answer('gg')
         c.execute(f'select reaction from users where id ={chat_id} limit 1')
         
         n=c.fetchone()[0]
         print(n)
         if n>90:
               n=90
         i=1
         q=battle[chat_id]
         print(q)
         damage=[]
         while i<len(battle[chat_id])-4:
              r=random.randint(1,100)
              damage.append(q[i]['mob_damage'])
              c.execute('select speed from mobs where name=? limit 1', (q[i]['mob_name'], ))
              
              if c.fetchone()[0]<n:
                    if r>n:
                          battle[chat_id][i]['mob_damage']=int(q[i]['mob_damage']/2)
                    else:
                          battle[chat_id][i]['mob_damage']=0
              else:
                   if r<=n: battle[chat_id][i]['mob_damage']=int(q[i]['mob_damage']/2)
              
              i+=1
         print(battle[chat_id], q)
         await asyncio.sleep(2)
         i=1
         print(len(battle[chat_id])-4, len(damage), damage)
         while i<len(damage)+1:
               print(i)
               battle[chat_id][i]['mob_damage']=damage[i-1]
               i+=1
         del i, q, n, r
         print(battle[chat_id])
         await asyncio.sleep(8)
         battle[chat_id]['dodge']=1
         print(battle[chat_id])
         
@dp.callback_query_handler( state=Statess.battle)
async def cl_start(callback: types.callback_query, state: FSMContext): 
    n=callback.data
    chat_id=callback.message.chat.id
    message_id=callback.message.message_id
    q=battle[chat_id]
    ikb=InlineKeyboardMarkup(row_width=3)
   
    if not n.isdigit():
          spl = n.split(' - ')
          if spl[0].split()[0]=='Сфера':
                last_ikb = callback.message.reply_markup.inline_keyboard
                for row in last_ikb:
                    if row[0].text == f'{n}':
                        count = int(spl[1])
                        if count > 1:
                            c.execute("UPDATE sklad SET quantity=quantity-1 WHERE id = ? and name = ?", (chat_id, spl[0]))
                            connect.commit()
                            ikb.add(InlineKeyboardButton(text=f'{spl[0]} - {count - 1}',
                                                         callback_data=f'{spl[0]} - {count - 1}'))
                        else:
                            c.execute('delete from sklad where id=? and name=?', (chat_id, spl[0]))
                            connect.commit()
                    elif row[0].text != '❌':
                        ikb.add(InlineKeyboardButton(text=f'{row[0].text}', callback_data=f'{row[0].text}'))
          else:

              if int(spl[1])>1:
                  async with state.proxy() as data:
                        dat=data['loot'].split(f'{n}')
                        data['loot']=dat[0]+f'{spl[0]} - {int(spl[1])-1}'+dat[1]
                        dat=data['loot'].split(',')
              else:
                   async with state.proxy() as data:
                        dat=data['loot'].split(f'{n},')
                        data['loot']=dat[0]+dat[1]
                        dat=data['loot'].split(',')
              add_sklad(chat_id, 'Сфера', 2)
              add_sklad(chat_id, spl[0], 1)
              for button in dat:
                     if button=='':
                           break
                     ikb.add(InlineKeyboardButton(text=f'{button}', callback_data=f'{button}'))
          ikb.add(InlineKeyboardButton(text='❌', callback_data='close'))
          await callback.message.edit_reply_markup(reply_markup=ikb)
          
          return
    n=int(n)
    ikb.add(InlineKeyboardButton(text='Атаковать', callback_data=f'{n}'),  InlineKeyboardButton(text='Уворот', callback_data='dodge'))
    if q['time_atak']<1:
          await callback.answer('подожите')
          return
    print(battle[chat_id]['time_atak'],'///////////////////////////')
    if q['time_atak']>q['ataka']:
          battle[chat_id]['time_atak']=q['ataka']
    
    battle[chat_id][n]['mob_hp']-=20
    battle[chat_id]['time_atak']-=1
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'{q[n]["mob_name"]}, здоровье: {q[n]["mob_hp"]}, {message_id}', reply_markup=ikb)
    await callback.answer('gg')
    await asyncio.sleep(5)
    battle[chat_id]['time_atak']+=1

@dp.message_handler(Text(equals='/info'), state='*')
async def menu(message: types.Message, state: FSMContext):
      c.execute('select * from items')
      q=c.fetchall()
      c.execute('select * from mobs')
      await message.answer(f'''/addi id name description class
{q}
/addm id name loot health damage speed strenge reaction
{c.fetchall()}
/delm potom vvidesh id
/deli...''')
@dp.message_handler(Text(equals='/addi'), state='*')
async def menu(message: types.Message, state: FSMContext):
        if message.chat.id==1079720309:
            async with state.proxy() as data:
                  data['admin']='i'
            await Statess.admin.set()
            
@dp.message_handler(Text(equals='/addm'), state='*')
async def menu(message: types.Message, state: FSMContext):
    if message.chat.id==1079720309:
            async with state.proxy() as data:
                  data['admin']='m'
            await Statess.admin.set()
            
@dp.message_handler(Text(equals='/delm'), state='*')
async def menu(message: types.Message, state: FSMContext):
    if message.chat.id==1079720309:
            async with state.proxy() as data:
                  data['admin']='dm'
            await Statess.admin.set()
            c.execute('select * from mobs')
            await message.answer(f'{c.fetchall()}')

@dp.message_handler(Text(equals='/deli'), state='*')
async def menu(message: types.Message, state: FSMContext):
    if message.chat.id==1079720309:
            async with state.proxy() as data:
                  data['admin']='di'
            await Statess.admin.set()
            c.execute('select * from items')
            await message.answer(f'{c.fetchall()}')

@dp.message_handler( state=Statess.admin)
async def menu(message: types.Message, state: FSMContext):
        if message.text =='Назад':
              await Statess.menu.set()
              return
        q=c.fetchall()
        print(q)
        await message.answer(f'{q}')
        text=message.text.split()
        async with state.proxy() as data:
                  if data['admin']=='m':
                      c.execute("INSERT INTO mobs (id, name, loot, health, damage, speed, strength, reaction) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (text[0], text[1], text[2], text[3], text[4], text[5], text[6], text[7]))
                      connect.commit()
                  elif data['admin']=='i':
                      c.execute("INSERT INTO items (id_item, name, description, class) VALUES (?, ?, ?, ?)",
              (text[0], text[1], text[2], text[3]))
                      connect.commit()
                  elif data['admin']=='dm':
                        c.execute('delete from mobs where id=?', (text[0], ))
                  elif data['admin']=='di':
                        c.execute('delete from items where id_item=?', (text[0], ))
                  data['admin']=''
                  c.execute('select * from mobs')
                  q=c.fetchall()
                  print(q)
                  await message.answer(f'{q}')

@dp.message_handler(Text(equals='Назад'), state='*')
async def menu(message: types.Message, state: FSMContext):
    s=str(await state.get_state())# , если често хз зачем, но там ниже есть  1 или 2 использований
    async with state.proxy() as data:
        dat=data['last']
        data['last_message']=''
    if dat=='menu_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await Statess.menu.set()
        await message.answer('Вы вернулись назад', reply_markup=menu_kb())
    elif dat=='shop_kb()':
        async with state.proxy() as data:
            data['last'] = 'citi_kb()'
            data['last_message']=''
        await message.answer('Вы вернулись назад', reply_markup=shop_kb())
        c.execute('update users set status= "shop" where id=?', (message.chat.id, ))
        connect.commit()
    elif dat=='citi_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await Statess.menu.set()
        if message.chat.id in list:
            list.remove(message.chat.id)
        await message.answer('Вы вернулись назад', reply_markup=citi_kb())
    elif dat=='do_kb()':
        if message.chat.id in list:
            list.remove(message.chat.id)
        await Statess.do.set()
        await message.answer('Вы вернулись назад', reply_markup=do_kb())
    elif dat=='movies_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=movies_kb())
    elif dat=='friend_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=friend_kb(message.chat.id))
    elif dat=='setting_kb()':
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        await message.answer('Вы вернулись назад', reply_markup=setting_kb())
    elif dat=='profile_kb()':
            info=fid(message.chat.id)
            async with state.proxy() as data:
                if s=='Statess:do':
                     data['last']= 'do_kb()'
                else:
                       data['last']='menu_kb()'
            await message.answer(f'''Профиль пользователя
Ник: {info[2]}
ID: {info[0]}

┌ Общая мощь :{info[10]}
├ Енергия: {info[8]/10}/{int(info[11]/10)}
├ Сила: {info[5]}
├ Скорость: {info[6]}
└ Реакция: {info[7]}

Время путишествий: {info[9]}

┌ 👥 Друзья
└ Количество: {len(get_friends(message.chat.id))}

┌ 🎈 Инвентарь
└ Предметов: {info[4]}''',  reply_markup=profile_kb())

@dp.message_handler(state=Statess.chatt)
async def menu(message: types.Message):
    if message.from_user.username:
        link = f'https://t.me/{message.from_user.username}'
    else:
        link = ''
    nik=fid(message.chat.id)[2]
    for chat_id in list:
        await bot.delete_message(message.chat.id, message.message_id)
        try:
            await bot.send_message(chat_id, f'[{nik}]({link}): {message.text}', parse_mode=types.ParseMode.MARKDOWN)
        except Exception as e:
            print(f'Error sending message to chat_id {chat_id}: {e}')

@dp.message_handler(commands='start')
async def start(message: types.Message):
    # kb.add(help)
    chat_id=message.chat.id
    c.execute('SELECT * FROM users WHERE id = ? limit 1', (chat_id, ))
    # c.execute('delete from ctc')
    # c.execute('delete from users')
    # connect.commit()
    fid = c.fetchone()
    print(fid)
    if not fid:
       q=10*random.randint(16, 21)
       fid = message.chat.id
       c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (fid, 100, message.from_user.first_name, '', 0, 0, 0, 0, q, 0, 0, q, '', ''))
       # c.execute('DELETE FROM ctc')
       connect.commit()
       await Statess.noduh.set()
       c.execute('INSERT INTO duh VALUES (?, ?, ?, ?, ?, ?);', (chat_id, 10, 0, 0, 0, 0))
       connect.commit()

    print(fid)
    #if fid(message.chat.id)[0]==0:
    #11111111111111111111111111111111111111111111111111111111111111111111111111111
       # startt.add(KeyboardButton('Проявить совего духа☀️🌑'))
    #else : return
    #await bot.send_message(chat_id=message.chat.id, text="""приветствую тебя message.from_user.first_name, это бот с духами .... По типу тамагочи.
#Faq - информация по боту
#Проявить совего духа - случайным образом выдать духа (если его нету)
#ну начало примерно такое)""", reply_markup=startt)

@dp.message_handler(Text(equals='Проявить совего духа☀️🌑'), state=Statess.noduh)
async def duh(message: types.Message):
        duh = InlineKeyboardMarkup(row_width=3)
        i1 = InlineKeyboardButton(text='1', callback_data='1')
        i2 = InlineKeyboardButton(text='2', callback_data='2')
        i3 = InlineKeyboardButton(text='3', callback_data='3')
        duh.add(i1)
        await bot.send_message(chat_id=message.chat.id, text='Вы вошли Храм вечного сияния ', reply_markup=startt)
        ran= random.randint(1, 3)
        if ran == 2:
            duh.add(i2)
            await sleep(60)
        elif ran== 3 :
            duh.add(i2, i3)
            await sleep(120)
        await sleep(60)
        await bot.send_message(chat_id=message.chat.id, text=' духи которых ты заинтересовал', reply_markup=duh)

@dp.message_handler(Text(equals='Город'), state=Statess.menu)#''''''''''''''''''''''''''''''''''''''''''''''''''
async def citi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    await message.answer('Вы вошли в город', reply_markup=citi_kb())

@dp.message_handler(Text(equals='Рейтинг'), state=Statess.menu)
async def top(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    # Выполняем SQL-запрос с функцией ORDER BY и LIMIT для получения 10 самых больших значений столбца "column_name" из таблицы "table_name", включая также идентификаторы "id"
    c.execute("SELECT id, predel FROM users ORDER BY predel DESC LIMIT 10")
    # Извлекаем результат запроса
    top = c.fetchall()
    message_text = 'Топ-10 пользователей:\n\n'
    for i, top in enumerate(top, start=1):
        fid, strength = top
        user = await bot.get_chat(fid)
        message_text += f'{i}. {user.first_name}, Сила: {strength}\n'
    
    await message.answer(f'{message_text}', reply_markup=chat_kb(), parse_mode='HTML')

@dp.message_handler(Text(equals='Ивенты'), state=Statess.menu)
async def ivent(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    ivent_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    ivent_kb.add(KeyboardButton('Принять квест'), KeyboardButton('Данж')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=ivent_kb)

@dp.message_handler(Text(equals='Кузня'), state=Statess.menu)
async def dom(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    chat_id=message.chat.id
    c.execute('select name from craft where id=?', (chat_id, ))
    q=c.fetchall()
    if q is None:
                    await message.answer('Навыков создания не найдено.', reply_markup=chat_kb())
                    return
    buttons = [KeyboardButton(f'{names[0]}') for names in q]
    await message.answer('vibery', reply_markup=chunks(buttons, 2))
    c.execute('update users set status="craft" where id=?', (chat_id, ))
    connect.commit()

@dp.message_handler(Text(equals='Торговый квартал'), state=Statess.menu)
async def shop(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'
    c.execute('update users set status="shop" where id=?', (message.chat.id, ))
    connect.commit()
    await message.answer('Вы да', reply_markup=shop_kb())

@dp.message_handler(Text(equals='Чат'), state=Statess.menu)
async def chatt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last'] = 'citi_kb()'
    await Statess.chatt.set()
    c.execute('UPDATE users SET status = "chat" WHERE id = ?', (message.chat.id, ))
    connect.commit()
    global list
    await message.answer( f'Игроков в чате -  {len(list)}', reply_markup=chat_kb())
    list.append(message.chat.id)
    q=fid(message.chat.id)
    for i in list:
        await bot.send_message(i, f'{q[2]} присойденился к чату')
   

"""@dp.message_handler(Text(equals='Работа'), state=Statess.menu)
async def dange(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['movie'] = 'Работа'
        data['last']= 'citi_kb()'
    await Statess.wait.set()
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('1'), KeyboardButton('3'), KeyboardButton('6')).add(KeyboardButton('Назад'))
    await message.answer('rabota', reply_markup=kb)"""

@dp.message_handler(Text(equals='Действия'), state=Statess.menu)#''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
async def movie(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'menu_kb()'
    await message.answer('Выберете дейвтие', reply_markup=movies_kb())

@dp.message_handler(Text(equals='Тренировка'), state=Statess.menu)
async def work(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'movies_kb()'
    work_kb=ReplyKeyboardMarkup(resize_keyboard=True)
    work_kb.add(KeyboardButton('Сила'), KeyboardButton('Реакция'), KeyboardButton('Скорость')).add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в город', reply_markup=work_kb)

@dp.message_handler(lambda message: message.text in ['Работа', 'Сила', 'Реакция', 'Скорость', 'Путешествие', 'Поглошение енергии'], state=Statess.menu)
async def d(message: types.Message, state: FSMContext):
    chat_id=message.chat.id
    #q=fid(message.chat.id)[0]
  #  if q[9]==0:
     #     await message.answer('Чел, иди востанови енергию, а то она на 0')
    q=fid(chat_id)[8]
    q=int(q/10)
    
    if message.text=='Путешествие':
             c.execute('select speed from users where id=? limit 1', (chat_id, ))
             speed=c.fetchone()[0]
             await Statess.do.set()
             await message.answer('Вы начали свое путeшествие', reply_markup=do_kb())
             async with state.proxy() as data:
                 data['movie'] = 'travel'
                 data['last']='bo_kb()'
             q=0
             times=7200-(54*speed)
             times=2#tut
             tasks[chat_id]={'time': datetime.now()}
             while True:
                  await asyncio.sleep(times)
                  while True:
                        async with state.proxy() as data:
                              print(100000000, data['movie'])
                              if data['movie'] =='battle':
                                    await asyncio.sleep(times)
                              else: 
                                    break
                  async with state.proxy() as data:
                             if data['movie']=='go_home':
                                   await Statess.menu.set()
                                   del data['movie']
                                   await bot.send_message(chat_id, 'Вы вернулись домой', reply_markup=menu_kb())
                                   break
                             dat=data['last'].split()
                             if len(dat)==2:
                                   if dat[0]=='banda6':
                                         c.execute(f'select speed from users where id={chat_id} limit 1')
                                         if c.fetchone()[0]>60:
                                               await bot.send_message(chat_id, 'Вам удалось сбежать', reply_markup=do_kb())
                                         else:
                                               await bot.send_message(chat_id, 'Вы отдали деньги и пошли дальше', reply_markup=do_kb())
                                               c.execute(f'update users set money=(money*30/70) where id={chat_id}')
                                               connect.commit()
                                   else:
                                         await message.answer('Вы пошли дальше', reply_markup=do_kb())
                             elif dat[0]=='shop':
                                   await message.answer('Вы пошли дальше', reply_markup=do_kb())
                             data['last']='do_kb()'
                  ivents = [ivent1, ivent2, ivent3, ivent4, ivent5, ivent6]
                  weights = [1, 1, 1, 3, 1, 1]
                  function = random.choices(ivents, weights=weights)[0]
                  inf=await function(chat_id)
                  if inf is not None:
                              async with state.proxy() as data:
                                   data['last'] = inf#//////////////////////////////////////обезательно нужно переделать, я не смогу выйти например в чат написать, что " ого мне выпал редкий шанс спустится в подземелье"
                              
                              await Statess.do.set()
                              #tasks[chat_id] = asyncio.create_task(coroutine2(chat_id, times))
                             # n=await tasks[chat_id]
                             # if n is not None:
                                  #  await Statess.menu.set()
                                    #return
                  #await bot.send_message(chat_id, 'вы нашли')#эту строчку нужно удалить
                  q+=1
             q=q*times/3600
             c.execute('update users set travel=travel+? where id=?', (q, chat_id))
             connect.commit()
            # tasks[chat_id] = asyncio.create_task(coroutine2(chat_id, c.fetchone()[0]))
             return
         
    if message.text=='Поглошение енергии' :
         await Statess.do.set()
         c.execute('select energy, max_energy from users where id=? limit 1', (chat_id, ))
         inf=c.fetchone()
         hour=int((inf[1]-inf[0])/10)
         await message.answer('Вы energy', reply_markup=do_kb())
         async with state.proxy() as data:
                 data['movie'] = 'energy'
                 data['last']='bo_kb()'
         tasks[chat_id] = {'coroutine': asyncio.create_task(coroutine3(chat_id)), 'time': datetime.now() + timedelta(hours=hour)}
         full=await tasks[chat_id]['coroutine']
         if chat_id in tasks:
                #task = tasks[chat_id]
                tasks.pop(chat_id)
         if str(await state.get_state())== 'Statess:chatt':
             await Statess.chatt.set()
             q=chat_kb()
         else:
             await Statess.menu.set()
             q=menu_kb()
         async with state.proxy() as data:
              data['last'] = 'menu_kb()'
         if full is None:
               await message.answer('Вы отменили востановлкние', reply_markup=menu_kb())
               return
         await bot.send_message(chat_id, 'Ваша енергия полностью востановлена', reply_markup=q)
         return
    if q==0:
          await message.answer('У тебя совсем не осталось енергии для для этого')
          return
    
    await Statess.wait.set()
    await message.answer('Напиши сколько времени(часов)', reply_markup=quant_kb(q))
    async with state.proxy() as data:
        data['movie'] = message.text
        data['last']='movies_kb()'
        if message.text=='Работа':
            data['last']= 'citi_kb()'
    
    print(Statess)

@dp.message_handler(state=Statess.wait)
async def da(message: types.Message, state: FSMContext):
    print('wait')
    chat_id=message.chat.id
    info=fid(chat_id)
    q=int(info[8]/10)#количество енкргии на данный момент, так как при выполнении действий минисуется енергия
    if message.text.isdigit()== True and 0 < int(message.text) <= q:
        async with state.proxy() as data:
            dat = data['movie']
            if data['movie']=='Сила':
                move='strength'
            elif data['movie']=='Реакция':
                move= 'reaction'
            elif data['movie'] == 'Скорость':
                move = 'speed'
          #  if data['movie'] == 'Поглошение енергии':
            #    move = 'energy'
             #   data['movie']== 'Енергия'
            elif data['movie'] == 'Работа':
                move = 'money'
            data['last']= 'do_kb()'
        await message.answer('теперь вы заняты', reply_markup=do_kb())
        await Statess.do.set()
        messag=int(message.text)
        
        if chat_id not in tasks:
            tasks[chat_id] = {
                'coroutine': asyncio.create_task(coroutine1(chat_id, messag)),
                'time': datetime.now() + timedelta(hours=messag),
                'quant': f'0 {messag}'


}
        print(tasks[chat_id])
          #  tasks[chat_id] = asyncio.create_task(coroutine1(chat_id, messag))
    #    else :
              # await message.answer('Вы уже чем-то заняты...')
        #       return
        print(77)
        j=await tasks[chat_id]['coroutine']
        tasks.pop(chat_id)
        if str(await state.get_state())== 'Statess:chatt':
            await Statess.chatt.set()
            q=chat_kb()
        else:
               await Statess.menu.set()
               q=menu_kb()
        async with state.proxy() as data:
            data['last'] = 'menu_kb()'
        c.execute(f'select "{move}" from users where id={chat_id} limit 1')#, (move, chat_id))
        a=c.fetchone()[0]
        print(move, a)
        if move == 'money':
            j=j*random.randint(5, 10)
            await message.answer(f'вы заработали {j}', reply_markup=q)
            c.execute(f'UPDATE users SET money = money+{j} WHERE id = {chat_id}')#, (move, move, j, chat_id))
            connect.commit()
            return
        elif a+j<110:
            c.execute(f'UPDATE users SET "{move}" = "{move}"+{j} WHERE id = {chat_id}')
            #c.execute('UPDATE users SET ? = ?+? WHERE id = ?', (move, move, j, chat_id))
            connect.commit()
           #dat = data['movie']
            await message.answer(f'Вы закончили, теперь ваша {dat}: {a + j}', reply_markup=q)
        else:
            c.execute(f'UPDATE users SET "{move}" = {110} WHERE id = {chat_id}')
            connect.commit()
            #async with state.proxy() as data:
               # dat=data['movie']
            await message.answer(f'Вы закончили, теперь ваша {dat}: {110}.Похоже что это предел', reply_markup=q)

        
        
    else:
        await message.answer(f'Попробуй ввести число от 1 до {q}', reply_markup=chat_kb())
        await Statess.wait.set()
 #   async with state.proxy() as data:
     #   data['last'] = 'menu_kb()'
    print(fid(message.chat.id))

@dp.message_handler(Text(equals='Друзья'), state="*")#''''''''''''''''''''''''''''''''''''''''''''
async def friend(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if str(await state.get_state())=='Statess:do':
              data['last']= 'do_kb()'
        else:
              data['last']= 'menu_kb()'
        data['last_message']= ' '
    await message.answer('Ваши друзья', reply_markup=friend_kb(message.chat.id))

@dp.message_handler(Text(equals='Профиль'), state="*")#''''''''''''''''''''''''''''''''''''''''
async def profile(message: types.Message, state: FSMContext):
    chat_id=message.chat.id
    info=fid(chat_id)
 #   c.execute(f'select * from duh where id={chat_id}')
#    print(c.fetchone()[5])
   # c.execute(f'select * from duh where id={chat_id}')
  #  print(c.fetchall()[0][5])
    async with state.proxy() as data:
            if str(await state.get_state())=='Statess:do':
                data['last']= 'do_kb()'
            else : data['last']='menu_kb()'
    c.execute('select * from duh where id=? limit 1', (chat_id, ))
    q=c.fetchone()
    print(q)
    update=int(info[5]+info[5]*q[1]/100)+int(info[6]+info[6]*q[2]/100)+int(info[7]+info[7]*q[3]/100)
    c.execute('update users set predel=? where id=?', (update, chat_id))
    connect.commit()
    await message.answer(f'''Профиль пользователя
Ник: {info[2]}
ID: {info[0]}
монет: {info[1]}
┌ Общая мощь :{update}
├ Енергия: {info[8]/10}/{int(info[11]/10)}
├ Сила: {int(info[5]+info[5]*q[1]/100)}  | ({info[5]}+{q[1]}%)
├ Скорость: {int(info[6]+info[6]*q[2]/100)}  | ({info[6]}+{q[2]}%)
└ Реакция: {int(info[7]+info[7]*q[3]/100)}   | ({info[7]}+{q[3]}%)

Время путишествий: {info[9]}

┌ 👥 Друзья
└ Количество: {len(get_friends(message.chat.id))}

┌ 🎈 Инвентарь
├ Предметов: {info[4]}
├ Оружие: {info[12]}
└ Одежда: {info[13]}
''',  reply_markup=profile_kb())

@dp.message_handler(Text(equals='Инвентарь'), state="*")#''''''''''''''''''''''''''''''''''''''''
async def profile(message: types.Message, state: FSMContext):
    chat_id=message.chat.id
    c.execute('update users set status="invent" where id=?', (chat_id, ))
    connect.commit()
    async with state.proxy() as data:
                data['last_message'] = ''
    add_sklad(message.chat.id, 'o', 1)
    c.execute('select name, quantity from sklad where id=?', (chat_id, ))
    info = c.fetchall()
    if not info:
        await message.answer('netu', reply_markup=chat_kb())
        return
    info = sorted(info, key=lambda x: x[1])
    buttons = [KeyboardButton(f'{name} ({quantity})') for name, quantity in info]
    await message.answer(f'da', reply_markup=chunks(buttons, 4))

@dp.message_handler(Text(equals='Настройки'), state="*")#''''''''''''''''''''''''''''
async def setting(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if str(await state.get_state())=='Statess:do':
            data['last']= 'do_kb()'
        else : data['last']='menu_kb()'
    await message.answer('Настроики', reply_markup=setting_kb())

@dp.message_handler(Text(equals='Сменить никнейм'), state="*")
async def nik(message: types.Message, state: FSMContext):
    c.execute('UPDATE users SET status = "edit_nik" WHERE id = ?', (message.chat.id, ))
    connect.commit()
    kb= ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Отмена'))
    await message.answer('Введи новый никнейм', reply_markup=kb)

@dp.message_handler(Text(equals='Подземелье'), state=Statess.menu)
async def dange(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last']= 'citi_kb()'

    #await message.answer('Вы вошли в подземелье', reply_markup=dange_kb())


@dp.message_handler(Text(equals='Чат'), state=Statess.do)
async def menu(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last'] = 'do_kb()'
    await Statess.chatt.set()
    c.execute('UPDATE users SET status = "chat" WHERE id = ?', (message.chat.id, ))
    connect.commit()
    global list
    list.append(message.chat.id)
    kb=ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Назад'))
    await message.answer('Вы вошли в чат', reply_markup=kb)

#@dp.message_handler(commands='menu')
#async def menu(message: types.Message):
#    if str(await state.get_state())=='Statess:do':
#        await message.answer('menu', reply_markup=do_kb())
#        return
#    await Statess.menu.set()
#    c.execute(f'UPDATE users SET status = "menu" WHERE id = {message.chat.id}')
#    connect.commit()
#    await message.answer('menu', reply_markup=menu_kb())
    
@dp.message_handler(commands='help')
async def help(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/help'), KeyboardButton('/stats'), KeyboardButton('/menu'))
    await bot.send_message(message.chat.id, """/start - ....
/stats - 
/menu ...""", reply_markup=kb)
    await message.delete()
    
@dp.message_handler(Text(equals='Меню'), state=Statess.noduh)
async def menu(message: types.Message):
    await Statess.menu.set()
    c.execute('UPDATE users SET status = "menu" WHERE id = ?', (message.chat.id, ))
    connect.commit()
    await message.answer('Главное меню', reply_markup=menu_kb())
    
@dp.message_handler(state=Statess.do)
async def menu(message: types.Message):
    c.execute('UPDATE users SET status = "do" WHERE id = ?', (message.chat.id, ))
    connect.commit()
    await message.answer('Главное меню', reply_markup=do_kb())

@dp.message_handler(content_types=types.ContentType.TEXT, state='*')
async def menu(message: types.Message, state: FSMContext):
    chat_id=message.chat.id
    mtext=message.text
    name=mtext.split(' (')[0]
    if mtext.split()[0]=='/add':
          add_sklad(chat_id, mtext.split()[1], 1)
    if await state.get_state() is None:
           c.execute(f'delete from craft')
           connect.commit()
           c.execute("INSERT INTO craft (id, name, recept, result, time) VALUES (?, ?, ?, ?, ?)", (chat_id, 'pon', '1 o', 2, 60))
           await message.answer('Главное меню', reply_markup=menu_kb())
           await Statess.menu.set()
           c.execute('UPDATE users SET status = "menu" WHERE id = ?', (chat_id, ))
           connect.commit()
           async with state.proxy() as data:
               data['last']= 'menu_kb()'
               data['last_message']=''
          # asyncio.create_task(coroutine3(chat_id))
           return
    
    info=fid(chat_id)
    c.execute('select id from users')
    print(c.fetchall(), info)
    if info[3]=='friends':
        print(22)
        async with state.proxy() as data:
            last=data['last_message']

        if mtext == 'Добавить':
            await message.answer('Введите ID друга')
        elif last== 'Добавить' :
            if mtext.isdigit():
                c.execute('select user_id from friends where user_id=? and friend_id=?', (chat_id, mtext))
                inf= c.fetchone()
                c.execute('select id from users where id=?', (mtext, ))
                if inf is None:
                    print('add')
                    if c.fetchone() is None:
                        await message.answer('Такого пользователя не существует')
                        print(132)
                        return
                    inline_keyboard = types.InlineKeyboardMarkup()
                    inline_keyboard.add(types.InlineKeyboardButton(text='da', callback_data='add_friend_yes'))
                    inline_keyboard.add(types.InlineKeyboardButton(text='net', callback_data='add_friend_no'))
                    await bot.send_message(chat_id=int(mtext), text='Вам пришел запрос в друзья')
                    await bot.send_message(chat_id=int(mtext), text=f'{info[2]} {info[0]}', reply_markup=inline_keyboard)
                    await message.answer('Запрос отправлен', reply_markup=friend_kb(info[0]))
                    
                else: await message.answer('Этот пользователь уже у вас в друзьях')
            #возможно здесь нужно обновить ласт мессадж
            else:
                await message.answer('ID можно найти в профле')
                return
        else:
            ikb= InlineKeyboardMarkup()
            ikb.add(InlineKeyboardButton(text='Удалить из друзей', callback_data='delete_friend')).add(InlineKeyboardButton(text='Удалить сообщение', callback_data='delete'))
            c.execute('select friend_id from friends where user_id=? and friend_name=? limit 1', (chat_id, mtext))
            info=c.fetchone()
            if info is None:
                await message.answer('Я не понимаю, попробуй воспользоватся кнопкми')
                return
            c.execute(f'select * from users where id={info[0]}')
            info=c.fetchone()
            await message.answer(f'''Профиль пользователя
            Ник: {info[2]}
            ID: {info[0]}

            ┌ Общая мощь :{info[10]}
            ├ Максимальная енергия: {int(info[11]/10)}
            ├ Сила: {info[5]}
            ├ Скорость: {info[6]}
            └ Реакция: {info[7]}

            Время путишествий: {info[9]}

            ┌ 👥 Друзья
            └ Количество: {len(get_friends(info[0]))}

            ┌ 🎈 Инвентарь
            └ Предметов: {info[4]}''', reply_markup=ikb)
            async with state.proxy() as data:
                data['last'] = 'friend_kb()'
        async with state.proxy() as data:
            data['last_message'] = f'{mtext}'
    elif info[3]=='edit_nik':
        if mtext=='Добавить' or len(mtext)>16:
            await message.answer('Не больше 16 символов')
            return
        c.execute('UPDATE users SET status = "menu", nik = ? WHERE id = ?', (mtext, chat_id))
        c.execute('update friends set friend_name =? where friend_id=?', (mtext, chat_id))
        connect.commit()
        await message.answer(f'Теперь ваш ник: {mtext}', reply_markup=setting_kb())
    elif info[3]=='invent':
        #i = mtext.rfind('(')#наверное можно в начало там где чат ид и месадж текст записывать згачние которе в скобках, тодько получать егл нк так а там ниже при покуппке и продаже естб норм вариант
        #message_text =mtext[:i].strip()
        #i = int(re.sub(r'\D', '', mtext.split()[1]))
        c.execute(
            f'select * from sklad')  # я жобавил "и чат ид" и лимит, хз может не нужно было
        q = c.fetchall()
        print(q)
        c.execute('select quantity from sklad where name=? and id=? limit 1', (name, chat_id))# я жобавил "и чат ид" и лимит, хз может не нужно было
        q=c.fetchone()
        if q is None:
            await message.answer('Такого предмета нету в вашем инвентаре')
            print(19)
            return
        print(28)
        c.execute('select * from items where name=? limit 1', (name, ))
        i=c.fetchone()
        ikb= InlineKeyboardMarkup()
        if i[3]=='Оружие':
               ikb.add(InlineKeyboardButton(text='Надеть', callback_data='up_weapon'))
        elif i[3]=='Одежда':
              ikb.add(InlineKeyboardButton(text='Надеть', callback_data='up_armor'))
        ikb.add(InlineKeyboardButton(text='Удалить сообщение', callback_data='delete'))
        await message.answer(f'''{i[1]}
Количество: {q[0]}     

***{i[2]}***''', reply_markup=ikb)
        async with state.proxy() as data:
            data['last_message'] = f'{mtext}'
    elif info[3]=='shop':
          async with state.proxy() as data:
                data['last'] = 'shop_kb()'
          c.execute(f'select * from shop')
          print(c.fetchall())
          if mtext=='Продать':
                c.execute('select name, quantity from sklad where id=?', (chat_id, ))
                q = c.fetchall()
                print(q)
                if not q:
                    await message.answer('netu', reply_markup=chat_kb())
                    return 
                q = sorted(q, key=lambda x: x[1])
                buttons = [KeyboardButton(f'{names} ({quantity})') for names, quantity in q]
                await message.answer('Выберите что хотите продать', reply_markup=chunks(buttons, 4))
                c.execute('update users set status="sell" where id=?', (chat_id, ))
                connect.commit()
                return
       #   elif mtext=='Аукцион':
          #      None
          #      return
          c.execute('SELECT DISTINCT name FROM shop where class=?', (mtext, ))
          q=c.fetchall()
          print(q)
          if not q :
              await message.answer('takogo ne prodaut')
              return
          buttons = [KeyboardButton(f'{names[0]}') for names in q]
          print(q, buttons)
          await message.answer(f'{mtext}', reply_markup=chunks(buttons, 4))
          c.execute('update users set status="search" where id=?', (chat_id, ))
          connect.commit()
    elif info[3]=='search':
          c.execute('SELECT quantity, price FROM shop WHERE name = ? ORDER BY price ASC LIMIT 4', (mtext,))

          q=c.fetchall()
          print(q, mtext)
          buttons = [KeyboardButton(f'{mtext} ({quantity}) - {price}') for quantity, price in q]
          await message.answer(f'Предмет (количество) - цена', reply_markup=chunks(buttons, 1))
          c.execute('update users set status="by" where id=?', (chat_id, ))
          connect.commit()
    elif info[3]=='by':
          async with state.proxy() as data:
                dat=data['last_message']
          name=dat.split(' (')[0]
          
          if dat=='':
                   print(name)
                   q=int(mtext.split(' (')[1].split(')')[0])
                   await message.answer(f'Ваедите количество от 1 до {q}', reply_markup=quant_kb(q))
                   print(8)
                   async with state.proxy() as data:
                       data['last_message'] = f'{mtext}'
          elif mtext.isdigit() and 0 < int(mtext) <= int(re.sub(r'\D', '', dat.split(')')[0])):
               c.execute('select money from users where id =? limit 1', (chat_id, ))
               money=c.fetchone()[0]
               if money<int(dat.split()[-1])*int(mtext):
                     await message.answer('У вас недостаточно средств')
                     return
               
               quantity=int(re.sub(r"\D", "", dat.split(")")[0]))
               c.execute('select id from shop where name = ? and quantity = ? and price = ? limit 1', (name, quantity, dat.split()[-1]))

               q=c.fetchone()
               print(q)
        
               if q is None:
                     await message.answer('×_× Уже продано', reply_markup=shop_kb())
                     c.execute('update users set status="shop" where id=?', (chat_id, ))
                     connect.commit()
                     async with state.proxy() as data:
                         data['last_message']= ''
                     return
               if quantity-int(mtext)>0:
                   c.execute('update shop set quantity = quantity-? where id = ?', (int(mtext), q[0]))
               else: 
                   c.execute('delete from shop where id=? and name =?', (q[0], name))
               c.execute('update users set money=money-?, status="shop" where id=?', (int(dat.split()[-1])*int(mtext), chat_id))
               print('-')
               c.execute('update users set money=money+? where id=?', (int(dat.split()[-1])*int(mtext), q[0]))
               print('+')
               connect.commit()
               add_sklad(chat_id, name, mtext)
               money=money-int(dat.split()[-1])*int(mtext)
               await message.answer(f'''Вы успешно приобрели {name}.
Осталось {money} монет''',  reply_markup=shop_kb())
          else:
               await message.answer('Попробуй еще раз') 
    elif info[3]=='sell':
          async with state.proxy() as data:
                dat=data['last_message']
          ms=mtext.split()
          #нужео месадж сплиь 0 в переменную
          if ms[0].isdigit() and  0 < int(mtext.split()[0]) <= int(re.sub(r'\D', '', dat)):
              if len(ms)!=2 or not ms[1].isdigit():
                  await message.answer('Попробуй еще раз ввести КОЛИЧЕСТВО и ЦЕНУ')
                  return
              name=dat.split(' (')[0]
              q=int(re.sub(r'\D', '', dat))
              if q-int(mtext.split()[0])== 0:
                    c.execute('delete from sklad where id = ? and name=?', (chat_id, name))
              else :
                    c.execute('update sklad set quantity=? where id= ? and name=?', (q-int(ms[0]), chat_id, name))
              connect.commit()
              c.execute('select quantity from shop where id = ? and name=?  limit 1', (chat_id, name))
              p=c.fetchone()
              print(name, 1)
              if p is None:
                    c.execute('select class from items where name=? limit 1', (name, ))
                    c.execute("INSERT INTO shop (id, name, quantity, class, price) VALUES (?, ?, ?, ?, ?)", (chat_id, name, ms[0], c.fetchone()[0], ms[1]))
              else:
                    c.execute('update shop set quantity=?, price = ? where id=? and name = ?', (p[0]+int(ms[0]), int(ms[1]), chat_id, name))
              connect.commit()
              await message.answer('Выставлено на продажу', reply_markup=shop_kb())
              c.execute(f'update users set status="shop" where id={chat_id}')
              connect.commit()
              async with state.proxy() as data:
                  data['last_message']= ''
                  
          else:
              c.execute('select quantity from sklad where id=? and name = ? limit 1', (chat_id, ms[0]))#тут наверное не склад, я хз, когда зашел в кож тут нп ыюла указана таблица,
              q=c.fetchone()
              if q is None:
                    await message.answer('Преdмет не найдено')
                    return
              await message.answer(f'''Введите количество и цену 
например: 1 25''', reply_markup=chat_kb())
              async with state.proxy() as data:
                  data['last_message']=mtext
    elif info[3]=='craft':
          async with state.proxy() as data:
                  dat=data['last_message']
          
          if mtext.isdigit() and len(mtext.split())==1 and dat!='':
                name=dat.split(",")[0]
                c.execute(f'select recept, result from craft where id=? and name=? limit 1', (chat_id, name))
                result=c.fetchone()
                print(result)
                recept = result[0]
                result=result[1]
                resources = [item.strip() for item in recept.split(',')]
                print(resources)
                c.execute("SELECT name, quantity FROM sklad WHERE id=?", (chat_id, ))
                inventory_items=c.fetchall()
                print(inventory_items)
                # Преобразование результатов запроса в словарь для удобства проверки
                inventory = {item[0]: item[1] for item in inventory_items}
                print(inventory)
                for resource in resources:
                    quantity, names = resource.split()
                    if names not in inventory or inventory[names] < int(quantity)*int(mtext):
                          await message.answer(f'Нехватает {names}')
                          break
                else:
                      
                      await Statess.do.set()
                      async with state.proxy() as data:
                         data['movie']='craft'
                      if chat_id not in tasks:
                          tasks[chat_id] = {
                              'coroutine': asyncio.create_task(coroutine5(chat_id, name, int(mtext), int(dat.split(',')[1]))),
                              'time': datetime.now() + timedelta(seconds=int(dat.split(',')[1])*int(mtext)),
                              'quant': f'0 {int(mtext)}'


}
                     # tasks[chat_id] = asyncio.create_task(coroutine5(chat_id, name, int(mtext), int(dat.split(',')[1])))
                      await message.answer(f'начали создание {name}', reply_markup=do_kb())
                      end=await tasks[chat_id]['coroutine']
                      print(end)
                      tasks.pop(chat_id)
                      if str(await state.get_state())== 'Statess:chatt':
                          await Statess.chatt.set()
                          q=chat_kb()
                      else:
                          await Statess.menu.set()
                          q=menu_kb()
                      async with state.proxy() as data:
                          data['last'] = 'menu_kb()'
                      await message.answer(f'Вы создали {end*int(result)} {name}', reply_markup=q)
                      add_sklad(chat_id, name, end*int(result))
          else:
                c.execute('select * from craft where id=? and name=? limit 1', (chat_id, mtext))
                q=c.fetchone()
                if q is None:
                      await message.answer('Такого навыка не найдено')
                      async with state.proxy() as data:
                          data['last_message']=''
                      return
                c.execute('select craft from duh where id=? limit 1', (chat_id, ))
                time=int(q[4]-q[4]*c.fetchone()[0]/100)
                async with state.proxy() as data:
                    data['last_message']=f'{mtext},{time}'
                time=f'{time//3600} часов, {time%3600//60} минут, {time%3600%60} секунд'
                
                await message.answer(f'''Предмет §{q[1]}
Расходники: {q[2]}
Количество: {q[3]}
Время создания: {time}

Введите сколько раз создать''')
                
# Проверка наличия и достаточности ресурсов в инвентаре
                

         
        #  q=c.fetchone()
        #  recept=recept.split(',')
        #  for i in recept.split():
             #   name=i.split()[0]
              #  quantity=int(i.split()[1])#это что бы не забыть что здесь вообще происходит
    else:
              await message.answer('''Я не понимаю, попробуй воспользоватся кнопкми''')

@dp.callback_query_handler(lambda c: c.data == 'ataka', state=Statess.battle)
async def cl_start(callback: types.callback_query):
    
    if tasks[callback.message.chat.id]['time_atak']<1:
          await callback.answer('подожите')
          return
    tasks[callback.message.chat.id]['mob_hp']-=20
    
    tasks[callback.message.chat.id]['time_atak']-=1
    await callback.answer('gg')
    await asyncio.sleep(5)
    
    tasks[callback.message.chat.id]['time_atak']+=1
    
@dp.callback_query_handler(lambda c: c.data == 'delete', state='*')
async def cl_start(callback: types.callback_query):
    print('del')
    chat_id = callback.message.chat.id
    message_id = callback.message.message_id
    await bot.delete_message(chat_id, message_id)
    await callback.answer('🗑')

@dp.callback_query_handler(lambda c: c.data == 'delete_friend', state='*')
async def cl_start(callback: types.callback_query, state: FSMContext):
    chat_id = callback.message.chat.id
    async with state.proxy() as data:
            remove_friend(chat_id, data['last_message'])
            data['last_message']=''      
    await bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='Грусть, печалька и котики', reply_markup=delete_ikb())

@dp.callback_query_handler(lambda c: c.data == 'up_weapon', state='*')
async def cl_start(callback: types.callback_query, state: FSMContext):
    print('up')
    chat_id = callback.message.chat.id
    mtext=callback.message.text.split('\n')[0]
    q=fid(chat_id)[0]
    if q[12]!='':
        add_sklad(chat_id, q[12], 1)
    c.execute('update users set weapon=? where id=?',(mtext, chat_id))
    c.execute("update sklad set quantity=quantity-1 WHERE id=? AND name=?", (chat_id, mtext))
    c.execute('select quantity from sklad where id=? and name=? limit 1', (chat_id, mtext))
    if c.fetchone()[0]==0:
        c.execute("DELETE FROM sklad WHERE id=? AND name=?", (chat_id, mtext))
    connect.commit()
    await bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text=f'Тепепь вы используете {mtext}', reply_markup=delete_ikb())
    c.execute('select name, quantity from sklad where id=?', (chat_id, ))
    info = c.fetchall()
    if not info:
        await bot.send_message(chat_id=chat_id,  text='Инвентарь', reply_markup=chat_kb())
        return 
    info = sorted(info, key=lambda x: x[1])
    buttons = [KeyboardButton(f'{name}  ({quantity})') for name, quantity in info]
    await bot.send_message(chat_id=chat_id, text='Инвентарь',  reply_markup=chunks(buttons, 4))
    
@dp.callback_query_handler(lambda c: c.data == 'delete_item', state='*')
async def cl_start(callback: types.callback_query, state: FSMContext):
    print('item')
    chat_id = callback.message.chat.id
    mtext=callback.message.text.split('\n')[0]
    
    c.execute("DELETE FROM sklad WHERE id=? AND name=?", (chat_id, mtext))

    c.execute('update users set status="invent" where id=?', (chat_id, ))
    connect.commit()
    await bot.edit_message_text(chat_id=chat_id, message_id=callback.message.message_id, text='''-_- 
Я реально думал что эту кнопку некогда не нажмут''', reply_markup=delete_ikb())
    async with state.proxy() as data:         
                data['last']= 'profile_kb()'
    c.execute('select name, quantity from sklad where id=?', (chat_id, ))
    info = c.fetchall()
    if not info:
        await bot.send_message(chat_id, 'netu', reply_markup=chat_kb())
        return 
    info = sorted(info, key=lambda x: x[1])
    buttons = [KeyboardButton(f'{name}  ({quantity})') for name, quantity in info]
    await bot.send_message(chat_id, 'invent', reply_markup=chunks(buttons, 4))
    
@dp.callback_query_handler(lambda c: c.data == '1')
async def cl_start(callback: types.callback_query):
    print(1)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Меню'))
    await bot.edit_message_text(text=' harakteristika', chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=None)
    await callback.answer('', reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == 'add_friend_yes', state='*')
async def callback_add_friend_yes(callback_query: types.CallbackQuery):
    info=fid(callback_query.from_user.id)
    friend_id = callback_query.message.text.split()[1]
    user_id = callback_query.from_user.id
    add_friend(user_id, friend_id, callback_query.message.text.split()[0])
    add_friend(friend_id, user_id, info[0][3])
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Вы приняли запрос', reply_markup=delete_ikb())
    await callback_query.answer('piz..')

@dp.callback_query_handler(lambda c: c.data == 'add_friend_no', state='*')
async def callback_add_friend_no(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Вы отклонили запрос', reply_markup=delete_ikb())
    await callback_query.answer('pidora otvet')

@dp.callback_query_handler( state='*')
async def process_callback_button(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Сообщение не актуально', reply_markup=delete_ikb())
    await callback_query.answer('пон')


if __name__ == '__main__' :
    executor.start_polling(dp, skip_updates=True)