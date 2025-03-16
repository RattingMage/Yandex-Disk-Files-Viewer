# Yandex Disk Files Viewer

Это веб-приложение, разработанное с использованием Django (бэкенд) и React (фронтенд), которое позволяет просматривать и загружать файлы с Яндекс.Диска по публичной ссылке. Приложение поддерживает фильтрацию файлов по типу (изображения, документы, аудио, видео) и возможность загрузки выбранных файлов в виде ZIP-архива.

## Основные функции

- Просмотр списка файлов по публичному ключу.
- Фильтрация файлов по типу (все файлы, изображения, документы, аудио, видео).
- Выбор нескольких файлов для загрузки.
- Загрузка выбранных файлов в виде ZIP-архива.

## Технологии

- **Бэкенд**: Django, Requests.
- **Фронтенд**: React, Axios, Bootstrap.
- **API**: Яндекс.Диск API.

## Установка и запуск

1. **Клонируйте репозиторий:**

    ```bash
    git clone https://github.com/RattingMage/Yandex-Disk-Files-Viewer.git
    cd Yandex-Disk-Files-Viewer
    ```

2. **Настройка бэкенда (Django):**

    ```bash
    python -m venv ~\venv
    .\venv\Scripts\activate
    cd YandexAPI
    pip install -r requirements.txt
    ```

3. **Запуск бэкенда (Django):**

    ```bash
    cd YandexAPI
    python manage.py runserver
    ```

4. **Настройка фронтенда (React):**

    ```bash
    cd yandex-disk-frontend
    npm install
    ```

5. **Запуск фронтенда (React):**

    ```bash
    cd yandex-disk-frontend
    npm start
    ```
