import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command # type: ignore
from config_reader import config
from json import load
from modules.data_comp import data_comp
import modules.messages as msg
from modules.parser_excel import parser_excel


# Загрузка файла json
def get_json(output_file):
    try:
        with open(output_file, "r") as file:
            return load(file)
    except:
        return parser_excel("./data/specialties.xlsx", "./data/spec.json")


json_data = get_json("./data/spec.json")

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


# # Хэндлер на команду /start
@dp.message(Command("start", "help", "data_update"))
async def cmd_start(message: types.Message):
    await message.answer(f"{msg.answer(message.text)}")


# Обработка данных, полученных от пользователя
@dp.message()
@dp.edited_message()
async def any_message(message: types.Message):
    string = message.text
    input_text = data_comp(string, json_data)
    output_text = msg.answer(input_text)
    await message.answer(f"{output_text}")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
