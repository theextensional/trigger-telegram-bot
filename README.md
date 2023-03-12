# Telegram триггер бот

Бот сравнивает присланное сообщение со словами триггерами из базы данных в GoogleSheets и присылает заготовленный ответ при совпадении.

## Подготовка

### Скачивание

```shell
git clone https://github.com/redboo/tgbot_trigger.git
cd tgbot_trigger/
```

### Установка и запуск виртуального окружения

```shell
python -m venv env && . ./env/bin/activate
```

### Установка зависимостей

#### для использования

```shell
pip install -r requirements/prod.txt
```

#### для разработки

```shell
pip install -r requirements/dev.txt
```

### Настройка переменных окружения

Все переменные окружения хранятся в файле `.env`. Пример: [`.env.example`](.env.example).

Создание файла:

```shell
cat > .env
```

Скопируйте и вставьте <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>V</kbd>:

```shell
# Файл для записи логов ошибок
ERROR_LOG_FILE=errors.log
# Файл для записи логов информации
INFO_LOG_FILE=info.log
# Уровень вывода сообщений логирования
# 50=CRITICAL, 40=ERROR, 30=WARNING, 20=INFO, 10=DEBUG, 0=NOTSET
LOG_LEVEL=30
```

Выход из режима записи <kbd>Ctrl</kbd> + <kbd>d</kbd>

#### Создание и настройка бота

Зайдите в приложение Telegram на вашем устройстве

Шаг 1. Найдите в телеграме бота с именем «@botfarther», он поможет вам в создании и управлении вашим ботом.

Шаг 2. Отправьте ему «/help», и вы увидите все возможные команды, которыми может управлять бот.

Шаг 3. Чтобы создать нового бота, отправьте «/newbot».

Следуйте инструкциям, которые он дал, и создайте новое имя для своего бота. Если вы создаете бота только для экспериментов, то имя должно быть уникальным, вы можете использовать пространство имен вашего бота, поместив свое имя перед ним в имени пользователя. Кстати, его псевдонимом может быть что угодно.

Шаг 4. Поздравляем! Вы только что создали своего бота Telegram. Вы увидите новый токен API, сгенерированный для него.

Скопируйте свой токен API и вставьте в файл `.env`:

```shell
echo 'BOT_TOKEN=123456:Your-TokEn_ExaMple' >> .env
```

#### Получение GoogleAPI ключей

[Статья - Как получить ключ Google API (для YouTube API, Google Sheets API и т.д.)](https://azzrael.ru/google-cloud-platform-create-app)

#### Создание таблицы для хранения данных

[Пример таблицы](https://docs.google.com/spreadsheets/d/1MG0OgjV30jcZ3Dlqh35_i5zr5WmCKvH9IGaGsQgiGfE/edit#gid=0)

#### Получение Imgur ключей

This tutorial demonstrates how to create an OAuth application for use with the imgur API. This tutorial covers both (i) creating your application; as well as (ii) retrieving your OAuth 2.0 client ID and client secret.

Steps to follow:

1. Sign in to imgur - <https://imgur.com/>
1. Navigate to the following page to register an OAuth application - <https://api.imgur.com/oauth2/addclient>
1. Fill the form with your application details
1. On the authorization callback URL section, register the following URL <https://int.bearer.sh/v2/auth/callback>
1. Click on "Save" and that's it!

Скопируйте и вставьте `Client ID` и `Client Secret` в файл `.env`:

```shell
echo 'IMGUR_API_ID=Your_Client_ID' >> .env
echo 'IMGUR_API_SECRET=Your_Client_Secret' >> .env
```

## Запуск

## Использование

Выполните команду, чтобы запустить бота:

```shell
env/bin/python bot.py
```

### Добавление триггера

Нажмите "ответить" на сообщение и далее наберите `+ название триггера`

### Добавление триггера в виде регулярного выражения

Нажмите "ответить" на сообщение и далее наберите `= название триггера`

### Редактирование триггеров

Достаточно открыть гугл-таблицу и предложить изменения в нём.
