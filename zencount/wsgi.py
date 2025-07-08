import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zencount.settings')  # Замените 'zencount' на имя вашего проекта
application = get_wsgi_application()