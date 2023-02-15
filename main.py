import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from aiogram.filters import Command
from aiogram import Router, Bot, Dispatcher, types
# from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, JOIN_TRANSITION, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import ChatMemberUpdated
import asyncio
import writer
from sender import update_group, checker
from config import token_bot
bot = Bot(token=token_bot)
dp = Dispatcher()
num_of_curs = [1, 2, 3, 4, 5, 6]
users_write = {}    # Временное состояние пишуших юзеров


@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    if message.chat.type == 'private':
        if not checker(message.from_user.username):
            if message.from_user.id in users_write:
                await message.answer("Ты начал заполнять форму. Закончи её сначала.")
            else:
                await message.answer("Привет, я помогу найти нужную группу, но сначала мне надо записать тебя.\n"
                                     "Напиши своё ФИО в формате 'Фамилия Имя Отчество'.\nПример:\nИванов Иван Иванович")
                users_write[message.from_user.id] = 0
        else:
            await message.answer("Ты уже зарегистрирован, переходи в группу!")
    else:
        dog = await bot.get_me()
        await message.answer(f"Это сообщения для личного чата @{dog.username}")


@dp.message(Command(commands=["update_lists"]))
async def update_lists(message: types.Message):
    if message.chat.type == 'private':
        form_text = ""
        for i in update_group():
            form_text = form_text + f"\n{i}"
        await message.answer(form_text)


@dp.message(lambda message: message.text)
async def machine(message: types.Message):
    user_id = message.from_user.id
    if user_id in users_write:
        if users_write[user_id] == 0:
            users_write[user_id] = 1
            await writer.former(message)
        elif users_write[user_id] == 1:
            try:
                course = message.text.split("-")[1][0]
                if int(course) in num_of_curs:
                    await writer.group(message)
                    users_write.pop(user_id)
                else:
                    await message.answer("Я не знаю такого курса, попробуй написать правильно.\n"
                                         "Если ты старше 6 курса, то для тебя группы нету :(")
            except:
                print("Неправильный ввод группы")
                await message.answer("Написано неправильно!\nНапиши группу в формате ХХ-ХХХ.\nПримеры:\nАК-127\nП-123")


# Запуск бота
async def main():

    # await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


