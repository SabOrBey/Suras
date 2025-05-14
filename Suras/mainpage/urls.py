from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from .views import *

urlpatterns = [
    path('experiment', experiment, name='experiment'),
    path('<int:Sura_id>/', detail, name='detail'),
    path('', index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
