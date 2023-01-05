import string
import json

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

from keyboards import keyboard_client
import settings


class TelegramBot:
    def __init__(self):

        # Инициализация имени бота
        self.name: str = settings.bot_name

        # Инициализация авторизующего токена в сети Телеграм
        self.authorization_token: str = settings.bot_authorization_token

        # Инициализация объекта Bot, импортируемого из aiogram
        # Принимаемый параметр - авторизующий токен в сети Телеграм
        self.bot = Bot(token=self.authorization_token)

        # Инициализация объекта Dispatcher (диспетчер), импортируемого из aiogram.dispatcher
        # Принимаемый параметр - инициализированный объект Bot
        self.dp = Dispatcher(self.bot)

        # Инициализация объекта executor, , импортируемого из aiogram.utils
        self.executor = executor

    def registrate_message_handler(self, function, commands=None):
        """
        Регистрация обработчика команд.
        :param function: Функция - обработчик, которая выполняется при написании команды в чате
        :param commands: Тип - список.
        Внутри списка перечислить команды, на которые должен реагировать обработчик
        Команды - тип str.
        При написании в чате команды, выполняется функция - обработчик
        :return:
        """
        if commands is None:
            commands = []
        if not commands:
            self.dp.register_message_handler(function)
        else:
            self.dp.register_message_handler(function, commands=commands)

    def registrate_message_handlers(self):
        """
        Функция - сборщик всех функций-обработчиков команд чата.
        Внимание! Функции обработчики должны быть асинхронными.
        :return: None
        """
        self.registrate_message_handler(self.handler_message_start, ['Start'])
        self.registrate_message_handler(self.handler_message_menu, ['Меню'])
        self.registrate_message_handler(self.handler_message_download, ['Загрузить_txt'])
        self.registrate_message_handler(self.handler_message_clear, ['Очистить_клавиатуру'])
        self.registrate_message_handler(self.censorship)

    async def censorship(self, message: types.Message):
        """
        Функция по поиску запрещенных слов, имеющихся в файле censored_words.json (расположен в той же папке, что и main)
        При нахождении запрещенного слова, выдает предупреждение и удаляет сообщение.
        :param message: Импортированный объект из aiogram
        :return: None
        """
        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(" ")} \
                .intersection(set(json.load(open("censored_words.json")))) != set():
            await message.answer('Маты запрещены')
            await message.delete()

    async def handler_message_start(self, message: types.Message):
        welcoming_message = f"Добро пожаловать на страничку бота '{self.name}'\n" \
                            f"Указанный бот создан с целью помощи в составлении речи государственного обвинителя " \
                            f" в прениях. (В настоящее время проект разрабатывается в свободное время. " \
                            f"Функционал далек от финального)."
        await message.answer(welcoming_message, reply_markup=keyboard_client)

    async def handler_message_menu(self, message: types.Message):
        msg = "Тест функции: меню"
        await message.answer(msg)

    async def handler_message_download(self, message: types.Message):
        msg = "Тест функции: загрузка"
        await message.answer(msg)

    async def handler_message_clear(self, message: types.Message):
        msg = "Тест функции: очистить клавиатуру"
        await message.answer(msg, reply_markup=ReplyKeyboardRemove())

    async def on_startup(self, _):
        print(f'Бот "{self.name}" вышел в онлайн')

    def start_polling(self):
        self.executor.start_polling(self.dp, skip_updates=True, on_startup=self.on_startup)

    def start_bot(self):
        self.registrate_message_handlers()
        self.start_polling()


if __name__ == '__main__':
    telegram_bot = TelegramBot()
    telegram_bot.start_bot()
