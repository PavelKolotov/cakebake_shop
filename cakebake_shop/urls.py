from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from cake_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('catalog/<int:id>/', views.catalog_api, name='catalog')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
