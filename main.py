import logging
from aiogram import Bot, Dispatcher, types, executor
import settings
from time import sleep

bot = Bot(token = settings.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

isActive = False

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("""Здравствуйте! Вас приветствует Система Автоматической Печати Файлов TelePrinter.

Правила использования TelePrinter:

1⃣ печатать, находясь в непосредственной близости от принтера;

2⃣ не злоупотреблять инфраструктурой;

3⃣ не совершать атаки;

4⃣ не трогать принтер руками (если возникла неполадка, отметьтесь в соответствующем разделе меню).

В случае выявления нарушений, виновник будет ограничен в данном сервисе. Продолжая, вы соглашаетесь с данными правилами.""")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    global isActive
    if message.document != None:
        if message.document.file_name.endswith(".pdf"):
            await message.answer("Скачиваю файл...")
            file = await message.document.download()
            if isActive:
                await message.answer("Ожидание, когда принтер станет доступным")
                while isActive:
                    pass
        else:
            return await message.answer("Неподдерживаемый формат!")
        isActive = True
        await message.answer("Печатаю файл...")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)