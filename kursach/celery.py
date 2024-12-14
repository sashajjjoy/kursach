from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите настройки Django по умолчанию для приложения Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kursach.settings')

app = Celery('kursach')

# Используем namespace `CELERY_` для всех Celery-настроек в Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит задачи в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
