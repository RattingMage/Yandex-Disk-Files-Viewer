from django.contrib import admin
from django.urls import path
from disk import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_files/', views.get_files, name='index'),                      # Путь для представления отображения списка файлов с Яндекс.Диска
    path('download/', views.download_file, name='download_file'),           # Путь для представления загрузки выбранных файлов с Яндекс.Диска
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),   # Путь для представления получения CSRF-токена
]
