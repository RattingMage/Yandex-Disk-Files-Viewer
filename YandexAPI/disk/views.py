import requests
import zipfile
import io
import json
import os 
from django.http import HttpResponse
from django.core.cache import cache
from django.http import JsonResponse
from django.middleware.csrf import get_token

# Константы для API Яндекс.Диска
YANDEX_DISK_API_URL = os.environ.get("YANDEX_DISK_API_URL")
YANDEX_DISK_DOWNLOAD_URL = os.environ.get("YANDEX_DISK_DOWNLOAD_URL")

def get_csrf_token(request):
    """
    Представление для получения CSRF-токена.
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})


def get_files(request):
    """
    Основное представление для отображения списка файлов с Яндекс.Диска.
    Поддерживает фильтрацию по типу файла и кэширование.
    """
    if request.method == 'POST':
        request_body = json.loads(request.body)
        public_key = request_body.get('public_key')
        file_type = request_body.get('file_type', 'all') 
        action = request_body.get('action', 'view_files') 

        cache_key = f'yandex_disk_files_{public_key}'

        # Если действие "Обновить файлы", очищаем кэш
        if action == 'refresh_files':
            cache.delete(cache_key)

        # Проверяем, есть ли данные в кэше
        cached_files = cache.get(cache_key)

        if cached_files:
            # Используем данные из кэша
            all_files = cached_files
        else:
            # Запрашиваем данные с API Яндекс.Диска
            response = requests.get(YANDEX_DISK_API_URL, params={'public_key': public_key})
            if response.status_code == 200:
                all_files = response.json().get('_embedded', {}).get('items', [])
                # Сохраняем данные в кэше на 5 минут
                cache.set(cache_key, all_files, timeout=300)
            else:
                return JsonResponse({'error': 'Не удалось получить список файлов'}, status=400)

        # Фильтрация файлов по типу
        if file_type != 'all':
            filtered_files = []
            for file in all_files:
                mime_type = file.get('mime_type', '')
                if file_type == 'image' and mime_type.startswith('image'):
                    filtered_files.append(file)
                elif file_type == 'document' and mime_type.startswith('application'):
                    filtered_files.append(file)
                elif file_type == 'audio' and mime_type.startswith('audio'):
                    filtered_files.append(file)
                elif file_type == 'video' and mime_type.startswith('video'):
                    filtered_files.append(file)
            files = filtered_files
        else:
            files = all_files

        return JsonResponse({
                'files': files,
                'public_key': public_key,
                'selected_file_type': file_type,
            })
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)


def download_file(request):
    """
    Представление для загрузки выбранных файлов с Яндекс.Диска.
    Поддерживает загрузку нескольких файлов в виде ZIP-архива.
    """
    if request.method == 'POST':
        request_body = json.loads(request.body)
        public_key = request_body.get('public_key')
        file_paths = request_body.get('file_paths')

        if not file_paths:
            return JsonResponse({'error': 'Выберите хотя бы один файл для загрузки'}, status=400)

        # Создаем ZIP-архив для выбранных файлов
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in file_paths:
                # Запрашиваем ссылку на скачифанние файла с API Яндекс.Диска
                response = requests.get(YANDEX_DISK_DOWNLOAD_URL, params={'public_key': public_key, 'path': file_path})
                if response.status_code == 200:
                    download_url = response.json().get('href')
                    # Скачиваем файл по полученной ссылке
                    file_response = requests.get(download_url)
                    if file_response.status_code == 200:
                        file_name = file_path.split("/")[-1]
                        # Записываем файл в ZIP-архив
                        zip_file.writestr(file_name, file_response.content)
                    else:
                        return JsonResponse({'error': f'Не удалось загрузить файл: {file_path}'}, status=400)   
                else:
                    return JsonResponse({'error': f'Не удалось получить ссылку для загрузки файла: {file_path}'}, status=400)

        # Возвращаем ZIP-архив пользователю
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'
        return response

    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)