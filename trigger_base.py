from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import MY_ID
import logging
import sql_for_trig

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot('5655857800:AAHhpBb3m88xjwK-FkJrKiv3wngLjoKytGo')
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await sql_for_trig.db_conn()
    print('BD connected!')


class FSMAdminAdd_trigger(StatesGroup):
    name = State()
    text = State()


@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cansel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == MY_ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# FSM
@dp.message_handler(commands=['add_trigger'])
async def add_trigger(message: types.message):
    if message.from_user.id == MY_ID:
        await FSMAdminAdd_trigger.name.set()
        await message.answer('Вы хотите добавить триггер? Если да, то напиши его имя.'
                             '\nА если нет, то пиши "отмена"(можешь написать и после ввода имени 😉!)')


@dp.message_handler(state=FSMAdminAdd_trigger.name)
async def load_photo(message: types.Message, state: FSMContext):
    if message.chat.id == MY_ID:
        async with state.proxy() as data:
            data['name'] = message.text

        await message.answer('А теперь текст который будет срабатывать при вводе триггера.')
        await FSMAdminAdd_trigger.next()


@dp.message_handler(state=FSMAdminAdd_trigger.text)
async def load_photo(message: types.Message, state: FSMContext):
    if message.chat.id == MY_ID:
        async with state.proxy() as data:
            data['text'] = message.text

        await message.answer(f'Готово! Имя - {data["name"]}, сообщение - {data["text"]}')
        await sql_for_trig.inserts(name=data['name'], value=data['text'])
        await state.finish()


# Вывод доступных триггеров
@dp.message_handler(commands=['all_triggers'])
async def all_triggers(message: types.Message):
    uoi = await sql_for_trig.all_name('name_trigger')
    await message.reply('Это триггеры поставленные админом')
    await message.answer(str(uoi)
                         .replace('[', '').replace(']', '')
                         .replace('(', '').replace(')', '')
                         .replace(',', '\n').replace("'", '')
                         .replace('\n\n', '\n'))


# Проверка триггера
@dp.message_handler()
async def bot_know(message: types.Message):
    names = await sql_for_trig.all_name(string='name_trigger')
    print(names)
    for x in names:
        aoa = [*x]
        if message.text == aoa[0]:
            aoy = await sql_for_trig.value(string='value_trigger', name=aoa[0])
            await message.answer(*aoy[0])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)