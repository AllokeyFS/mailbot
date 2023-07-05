from parsing import exchange_currency
from text import text_start
from database import Database
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN = ''

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row('Mailing', 'Admin')
keyboard.add('Currency')
keyboard_url = InlineKeyboardMarkup()
instagram_url = InlineKeyboardButton(text='Instagram',url='https://www.instagram.com/')
telegram_url = InlineKeyboardButton(text='Telegram',url='https://t.me/Xxxanderrrs')
keyboard_url.add(instagram_url,telegram_url)
inline_4 = InlineKeyboardButton(text='Рассылка',callback_data='mailing')
inline_5 = InlineKeyboardButton(text='Выборочная рассылка',callback_data='selective_mailing')
inline_6 = InlineKeyboardButton(text='Тех. поддержка',callback_data='support')
inline_7 = InlineKeyboardButton(text='Курсы валют',callback_data='exchange')
inline_8 = InlineKeyboardButton(text='Фото',callback_data='photo')
keyboard_url.row(inline_4,inline_5, inline_6, inline_7, inline_8)




@dp.message_handler(commands='start')
async def start_command(message: Message):
    db = Database()
    db.connect()
    db.create_user_table()
    first_name = message.from_user.first_name
    user_id = message.from_user.id
    check = db.check_user(user_id)
    if check:
        await bot.send_message(message.from_user.id, text='Привет, ты зарегистрирован', reply_markup=keyboard)
    else:
        db.insert_user(first_name, user_id)
        await bot.send_message(message.from_user.id, text='Привет, ты прошёл регистрацию', reply_markup=keyboard)
    
    db.close()



@dp.message_handler(commands='info')
async def info_bot(message: Message):
    class Mailing(StatesGroup):            #Машина состояния!!!
            mailing_text = State()
    db = Database()
    db.connect()
    user_list = db.mailing_message()
    if message.from_user.id == 573015206:
        await Mailing.mailing_text.set()
        await bot.send_message(message.from_user.id, 'Enter')

        @dp.message_handler(state=Mailing.mailing_text)
        async def mailing(message: Message, state: FSMContext):
            async with state.proxy() as data:
                data['mailing_text'] = message.text
                mailing_text = data['mailing_text']
                await state.finish()
            for item in user_list:
                try:
                    await bot.send_message(chat_id=item[0], text=mailing_text)
                except Exception:
                    continue
            await bot.send_message(message.from_user.id, text='Рассылка успешно отправлена') 
    else:
        await bot.send_message(message.from_user.id, text='Рассылка недоступна')
    db.close()


############# ВАРИАНТ ЭЛТУРАНА 
# @dp.message_handler(commands='info')
# async def info_bot(message: Message):
#     class MessageList(StatesGroup):
#         text = State()
#     db = Database()
#     db.connect()
#     user_list = db.mailing_message()
#     if message.from_user.id == 573015206:
#         await MessageList.text.set()
#         await message.answer('Enter the mailing text')
#         @dp.message_handler(state=MessageList.text)
#         async def messages(message: Message, state: FSMContext):
#             async with state.proxy() as data:
#                 data['text'] = message.text
#                 message_text = data['text']
#                 for item in user_list:
#                     try:
#                         await bot.send_message(item[0], message_text)
#                         await message.answer('Рассылка успешно отправлена', reply_markup=keyboard)
#                         await state.finish()
#                     except Exception:
#                         continue
                    
#     db.close()

@dp.message_handler(commands='admin')
async def admin_bot(message: Message):
    db = Database()
    db.connect()
    name_list = db.name_select()
    
    if message.from_user.id == 573015206:
        await message.reply('Привет админ')
        text = 'Все пользователи бота\n'

        for name in name_list:
            text += f'{name[0]}\n'
        await bot.send_message(message.from_user.id, text=text)
    else:
        await message.reply('Вы не админ')

@dp.callback_query_handler(lambda call: call.data == 'exchange')
async def exchange_cfunc(call):
    currency = exchange_currency()
    currency_list = []
    for key, value in currency.items():
        result = f'{key} - {value}'
        currency_list.append(result)
    text = '\n'.join(currency_list)
    await bot.send_message(call.from_user.id, text=f'Курсы валют\n\n{text}')

@dp.callback_query_handler(lambda call: call.data == 'support')
async def support_func(call):
    # Формируем ссылку на профиль пользователя
    user_id = call.from_user.id
    profile_link = f'tg://user?id={user_id}'

    # Формируем текст сообщения с ссылкой
    message_text = f'Обращаться, [{call.from_user.first_name}]({profile_link})'

    # Отправляем сообщение с ссылкой
    await bot.send_message(call.from_user.id, text=message_text, parse_mode='MarkdownV2')

@dp.message_handler(content_types=['text'])
async def message_text(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    msg = message.text
    with open('message_text.txt','a') as file:
        file.write(f' User: {first_name} - message: {msg}\n')
    if message.text == 'Тех. поддержка':
        await bot.send_message(user_id, text='Связаться с тех. поддержкой монжо по ссылке\n\nAllokey',reply_markup=keyboard_url)
    elif msg == 'Mailing':
        await info_bot(message)
    elif msg == 'Admin':
        await admin_bot(message)
    elif msg == 'Currency':
        currency = exchange_currency()
        currency_list = []
        for key, value in currency.items():
            result = f'{key} - {value}'
            currency_list.append(result)
        text = '\n'.join(currency_list)
        await bot.send_message(user_id,text=f'Курсы валют\n\n{text}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)