# Car Wrapping Bot

Telegram бот для учета работ по оклейке автомобилей пленкой.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/antonkrm/car-wrapping-bot.git
   cd car-wrapping-bot
   ```

2. Создайте виртуальное окружение и активируйте его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # На Windows: venv\Scripts\activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `config.py` со следующим содержимым:
   ```python
   BOT_TOKEN = "ваш_токен_бота"
   ADMIN_PASSWORD = "ваш_пароль_администратора"
   ```

5. Инициализируйте базу данных:
   ```bash
   python init_db.py
   ```

6. Запустите бота:
   ```bash
   python bot.py
   ```

## Использование

После запуска бота, любой пользователь может отправлять отчеты в свободной форме.
Для получения доступа к админским функциям (просмотр отчетов, выгрузка фото) нужно авторизоваться командой `/admin` и ввести пароль администратора.
