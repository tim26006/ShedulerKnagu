import asyncio
from aiogram import Bot, Dispatcher, filters
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN, STIKER1_TOKEN
from parser import  parse_shedule_on_week
from aiogram import types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboard import reply_kb1, reply_kb2

pair_times = [
    "08:10 -09:40",
    "09:50 -11:20",
    "11:30 -13:00",
    "13:30 -15:00",
    "15:10 -16:40",
    "16:50 -18:20",
    "18:30 -20:00",
    "20:10 -21:40",
]

digits = [
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
]



async def get_start(message: Message, bot: Bot):
    await bot.send_sticker(message.chat.id, STIKER1_TOKEN)
    await message.answer("Привет! Я буду отправлять тебе расписание каждый день", reply_markup=reply_kb1, parse_mode="Markdown")

async def sending_schedule_on_next_day(bot: Bot, chat_id: int):
    schedule = parse_shedule_on_week()
    for day, lessons in schedule.items():
        text = f"<b>Привет! Расписание на завтра ({day})</b>\n\n"
        for i, lesson in enumerate(lessons, 1):
            if lesson['Предмет'] == "-":
                continue
            else:
                text += f"    <i>{digits[i - 1]} {pair_times[i - 1]}.\n    <b>{lesson['Предмет']}</b>: {lesson['Тип занятия']}</i>\n"
                text += f"    <i>Преподаватель: {lesson['Преподаватель']}</i>\n"
                text += f"    <i>Аудитория: {lesson['Аудитория']}</i>\n\n"
        await bot.send_message(chat_id, text=text, parse_mode="HTML")



async def start_sending_schedule(message: Message, bot: Bot):
    await message.answer("Отлично! Бот может автоматически отправлять расписание на следующий день. Выберете время, когда сообщать расписание", parse_mode="Markdown" , reply_markup=reply_kb2)

async def start_sending_schedule_on_time(message: Message, bot: Bot):
    time = str(message.text)[2:]
    hour = time.split(":")[0]
    minute = time.split(":")[1]
    sheduler = AsyncIOScheduler(timezone="Asia/Vladivostok")
    # Schedule the job with the bot and chat_id arguments
    sheduler.add_job(sending_schedule_on_next_day, trigger="cron", hour=int(hour), minute=int(minute), args=[bot, message.chat.id])
    sheduler.start()
    await message.answer(f"Хорошо! Теперь бот будет отправлять  расписание каждый день в {hour+':'+minute}", parse_mode="Markdown")

async def start():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.message.register(get_start, Command("start"))
    dp.message.register(start_sending_schedule, lambda message: message.text == "📝 Начать отправлять расписание")
    dp.message.register(start_sending_schedule_on_time, lambda message: message.text == "🕐 16:00")
    dp.message.register(start_sending_schedule_on_time, lambda message: message.text == "🕐 16:00")
    dp.message.register(start_sending_schedule_on_time, lambda message: message.text == "🕐 19:00")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())