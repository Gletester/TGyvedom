# Spec Watcher Bot 🚀

Уведомление комплектатора о новой спецификации в Telegram.

## Как это работает

1. **Андрей** заходит на веб-страницу сервиса и загружает файл спецификации (или кладёт его в сетевую папку)
2. **Система** автоматически фиксирует появление нового документа
3. **Игорь** мгновенно получает уведомление в Telegram с названием файла и ссылкой
4. **Игорь** открывает спецификацию и приступает к закупке

## Быстрый старт — Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/...)

Или вручную:

```bash
# 1. Клонировать
git clone https://github.com/marblwood/TGyvedom.git
cd TGyvedom

# 2. Настроить переменные в Railway Dashboard:
#    BOT_TOKEN     — токен бота от @BotFather
#    IGOR_CHAT_ID  — ID чата Игоря (узнать у @userinfobot)
#    BASE_URL      — https://your-app.railway.app

# 3. Задеплоить через Railway CLI или GitHub
```

## Переменные окружения

| Переменная     | Описание                                  |
|---------------|-------------------------------------------|
| `BOT_TOKEN`   | Токен Telegram-бота (обязательно)         |
| `IGOR_CHAT_ID`| Chat ID Игоря в Telegram (обязательно)    |
| `WATCH_FOLDER`| Путь к папке со спецификациями (по умолч. ./uploads) |
| `BASE_URL`    | Публичный URL сервиса (для ссылок)        |
| `PORT`        | Порт сервера (по умолч. 8080)             |

## Локальный запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# заполнить .env
python app.py
```

Открыть http://localhost:8080

## Структура

```
spec-watcher/
├── app.py              # Flask-приложение
├── bot.py              # Telegram-уведомления
├── watcher.py          # Мониторинг папки
├── config.py           # Конфигурация
├── templates/
│   └── index.html      # Веб-интерфейс загрузки
├── uploads/            # Хранилище файлов
├── Dockerfile          # Docker-сборка
├── railway.json        # Конфиг Railway
└── requirements.txt
```

## Команды

- `/info` — информация о создателе
- `/nojail` — отключить режим джейлбрейка
- `/jailbreak` — активировать режим джейлбрейка
