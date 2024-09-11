from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from pyrogram import Client, filters
import asyncio

API_TOKEN = '7112769984:AAGbuHwS0zry6MMo61SQIade8rlDmy33Vlc'
API_ID = '27785340'
API_HASH = 'cc6480b7fdc0d9561942c14ec989e731'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

pyrogram_client = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=API_TOKEN)

async def on_startup(dp):
    # Запуск клиента Pyrogram
    if not pyrogram_client.is_connected:
        await pyrogram_client.start()
    print("Pyrogram client started")

async def on_shutdown(dp):
    # Остановка клиента Pyrogram
    if pyrogram_client.is_connected:
        await pyrogram_client.stop()
    print("Pyrogram client stopped")

async def get_group_id(message: types.Message):
    chat_id = message.chat.id
    if chat_id > 0:
        return chat_id
    else:
        chat = await pyrogram_client.get_chat(chat_id)
        return chat.id
    
async def get_chat_members(chat_id):
    members = []
    async for member in pyrogram_client.get_chat_members(chat_id):
        members.append(member)
    return members
        
@dp.message(Command("start"))
async def send_welcome(message: Message):
    if message.chat.type == "private":
        keyboard = InlineKeyboardBuilder()
        bot_username = (await bot.get_me()).username  
        add_bot_url = f"https://t.me/{bot_username}?startgroup=true"  
        keyboard.button(text="Добавить бота в группу", url=add_bot_url)
        keyboard = keyboard.as_markup()

        await message.answer(
            "Привет! Нажми на кнопку ниже, чтобы добавить меня в свой чат:",
            reply_markup=keyboard
        )

@dp.message(Command("all"))
async def tag_all(message: types.Message):
    chat_id = await get_group_id(message)
    members = await get_chat_members(chat_id)
    
    mentions = []
    for member in members:
        user = member.user
        if not user.is_bot:
            mention = f"[{user.first_name}](tg://user?id={user.id})"
            mentions.append(mention)
    
    MAX_TAGS_PER_MESSAGE = 50
    for i in range(0, len(mentions), MAX_TAGS_PER_MESSAGE):
        text = " ".join(mentions[i:i + MAX_TAGS_PER_MESSAGE])
        await message.answer(text, parse_mode='Markdown')


@dp.message(Command("admins"))
async def tag_admins(message: Message):
    chat_id = message.chat.id
    admins = await bot.get_chat_administrators(chat_id)  

    bot_user = await bot.get_me()  
    mentions = []
    for admin in admins:
        if admin.user.id != bot_user.id and not admin.user.is_bot: 
            mention = f"<a href='tg://user?id={admin.user.id}'>{admin.user.first_name}</a>"
            mentions.append(mention)

   
    MAX_TAGS_PER_MESSAGE = 50
    for i in range(0, len(mentions), MAX_TAGS_PER_MESSAGE):
        text = " ".join(mentions[i:i + MAX_TAGS_PER_MESSAGE])
        await message.answer(text, parse_mode='HTML')  

async def main():
    await on_startup(dp)
    try:
        await dp.start_polling(bot)
    finally:
        await on_shutdown(dp)

if __name__ == "__main__":
    asyncio.run(main())
