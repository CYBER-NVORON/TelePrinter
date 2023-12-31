import os
import logging
import settings
import platform
from aiogram import Bot, Dispatcher, types, executor

bot = Bot(token = settings.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

isActive = False
printer_name = ""

@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer("""Здравствуйте! Вас приветствует Система Автоматической Печати Файлов TelePrinter.

Правила использования TelePrinter:

1⃣ печатать, находясь в непосредственной близости от принтера;

2⃣ не злоупотреблять инфраструктурой;

3⃣ не совершать атаки;

4⃣ не трогать принтер руками.

В случае выявления нарушений, виновник будет ограничен в данном сервисе. Продолжая, вы соглашаетесь с данными правилами.""")


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    global isActive
    
    if platform.system() not in ['Windows', 'Linux', 'Darwin']:
        return print("Неизвестная OS!")

    if message.document is None:
        return
    
    if not message.document.file_name.endswith(".pdf"):
        return await message.answer("Неподдерживаемый формат!")
    
    await message.answer("Скачиваю файл...")
    file = await message.document.download()
    
    if isActive:
        await message.answer("Ожидание, когда принтер станет доступным!")
        while isActive: pass
    
    isActive = True
    await message.answer("Печатаю файл...")

    if platform.system() == 'Windows':
        os.startfile(os.getcwd() + "/" + file.name, "print")
    elif platform.system() == 'Darwin' or platform.system() == 'Linux':
        os.system(f"lpr -P {printer_name} {os.getcwd() + '/' + file.name}")

    isActive = False
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
