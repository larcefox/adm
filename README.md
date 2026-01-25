# ADM

Веб‑приложение на Flask для управления 3D‑сценой и генерации данных, совместимых с Three.js.

## Возможности
- Библиотека `entity_class.py` для создания 3D‑сущностей и сериализации их в JSON.
- Веб‑интерфейс с аутентификацией и админ‑панелью.
- WebSocket сервер для обновления сцены в реальном времени.

## Установка
1. Создайте и активируйте виртуальное окружение.
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл `.env` и определите переменные окружения:
   ```
   APP_SETTINGS=config.DevelopmentConfig
   DATABASE_URL=postgresql://user:password@localhost/dbname
   DB_SCHEMA=adm
   WORLD_DB_SCHEMA=world
   ```
   Значения могут отличаться в зависимости от вашей среды.
4. Примените миграции базы данных (при необходимости):
   ```bash
   flask db upgrade
   ```

## Запуск
```bash
python manage.py run
```
Скрипт запускает Flask‑сервер и фоновый WebSocket‑поток.

## Лицензия
GPLv3 © Bac9l Xyer
