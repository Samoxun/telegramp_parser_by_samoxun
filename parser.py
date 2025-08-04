# Telegram User Information Scraper
# Version: 2.2
# Date: 2025-08-04
# Coder : Samoxun

from telethon.sync import TelegramClient
from telethon.errors import AuthKeyUnregisteredError, SessionPasswordNeededError, ApiIdInvalidError
from tabulate import tabulate
import asyncio
import os

# Привет! Тут твои данные для входа в Telegram API
# Если что-то не работает, сходи на https://my.telegram.org, войди в аккаунт с номером телефона,
# который указан ниже, и возьми новые API_ID и API_HASH. Если ошибка "ApiIdInvalidError" вылезет,
# значит, эти ключи не катят. Просто создай новое приложение на сайте, скопируй новые ключи,
# вставь их сюда и удали файл session_name.session из папки, где лежит скрипт. И всё заработает!


API_ID = 'ВСТАВЬ'  # Сюда впиши свой API_ID с my.telegram.org
API_HASH = 'ВСТАВЬ'  # А сюда API_HASH
PHONE = 'ВСТАВЬ'  # Твой номер телефона, не забудь плюс в начале!
CHAT_ID = 'ВСТАВЬ'  # Название чата или его ID (типа @ChatName или -1001234567890)

# Тут будем хранить данные о людях из чата
users_data = []  # Список, чтобы всё шло по порядку

def save_to_file():
    """Сохраняем инфу о людях в красивую таблицу в файле users.txt"""
    headers = ["Имя", "Ссылка"]
    table_data = [user_info.split('\t') for user_info in users_data]
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    with open('users.txt', 'w', encoding='utf-8') as f:
        f.write(table + "\n")
    print("Всё готово! Данные лежат в users.txt в виде таблицы.")

async def main():
    # Подключаемся к Telegram
    session_file = 'session_name.session'
    async with TelegramClient('session_name', API_ID, API_HASH, device_model="Python Script", system_version="Windows") as client:
        try:
            # Проверяем, залогинены ли мы
            if not await client.is_user_authorized():
                print("Сессия протухла, надо залогиниться заново!")
                # Если есть старый файл сессии, грохнем его
                if os.path.exists(session_file):
                    os.remove(session_file)
                # Логинимся с номером телефона
                await client.start(phone=PHONE)
                print("Залогинились, всё ок!")

            # Находим чат, который будем парсить
            chat = await client.get_entity(CHAT_ID)

            # Собираем инфу о всех участниках чата
            async for user in client.iter_participants(chat):
                if user.bot:  # Ботов пропускаем, они нам не нужны
                    continue
                first_name = user.first_name or "Без имени"
                username = user.username or None

                # Формируем строчку для каждого человека
                if username:
                    user_info = f"{first_name}\tt.me/{username}"
                    users_data.append(user_info)
                else:
                    user_info = f"{first_name}\tНет ссылки"
                    users_data.append(user_info)

            # Записываем всё в файл
            save_to_file()
            print("Всё спарсили! Ищи результаты в users.txt")

            # Выходим из сессии, чтобы не вылетало на телефоне
            await client.log_out()
            print("Сессия закрыта, чтобы твой телефон не глючил.")

        except ApiIdInvalidError:
            print("Ой, беда! API_ID или API_HASH неправильные. Давай так:")
            print("1. Иди на https://my.telegram.org, влогинься с номером телефона.")
            print("2. Создай новое приложение в разделе 'API development tools'.")
            print("3. Скопируй новые API_ID и API_HASH и вставь их в код.")
            print("4. Удали session_name.session из папки и запусти скрипт заново.")
            return
        except AuthKeyUnregisteredError:
            print("Ключ авторизации не работает. Попробуй вот что:")
            print("1. Проверь API_ID и API_HASH на my.telegram.org.")
            print("2. Удали session_name.session и запусти скрипт снова.")
            print("3. Убедись, что твой аккаунт не забанили в Telegram.")
            return
        except Exception as e:
            print(f"Что-то пошло не так: {str(e)}")
            print("Попробуй перезапустить скрипт или проверь интернет.")
            return

if __name__ == '__main__':
    asyncio.run(main())